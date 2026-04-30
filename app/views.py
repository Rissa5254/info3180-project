"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db, login_manager
from datetime import date, datetime, timedelta, timezone
from flask import render_template, request, jsonify, session, send_file
from sqlalchemy import or_
import os
from app.models import User, Location, Interest, User_Interest, Match, Message, Favourite, Notification 

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


# 1. User Authentication and Profile Management


# 2. Matching System


# 3. User Connections and Messaging
@app.route('/api/messages', methods=['POST'])
def send_message():
    data = request.get_json()
    sender_id = session.get('user_id')

    receiver_id = data.get('receiver_id')
    content = data.get('content')

    if not is_matched(sender_id, receiver_id):
        return jsonify({"error": "Users not matched"}), 403

    message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
        timestamp=datetime.now(timezone.utc)
    )

    db.session.add(message)
    db.session.commit()

    return jsonify({"message": "Message sent"}), 201

@app.route('/api/messages/<int:user_id>', methods=['GET'])
def get_messages(user_id):
    current_user = session.get('user_id')

    messages = Message.query.filter(
        ((Message.sender_id == current_user) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user))
    ).order_by(Message.timestamp.asc()).all()

    return jsonify([
        {
            "sender_id": m.sender_id,
            "receiver_id": m.receiver_id,
            "content": m.content,
            "timestamp": m.timestamp
        }
        for m in messages
    ])

@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    current_user = session.get('user_id')

    messages = Message.query.filter(
        (Message.sender_id == current_user) |
        (Message.receiver_id == current_user)
    ).all()

    users = set()
    for m in messages:
        if m.sender_id != current_user:
            users.add(m.sender_id)
        if m.receiver_id != current_user:
            users.add(m.receiver_id)

    return jsonify(list(users))


# 4. Search & Discovery
@app.route('/api/users/search', methods=['GET'])
def search_users():
    query = User.query
    
    # Query parameters
    search_word = request.args.get("q")
    min_age = request.args.get("min_age", type=int)
    max_age = request.args.get("min_age", type=int)
    cities = request.args.get('city')
    countries = request.args.get('country')
    selected_interests = request.args.get('interests')
    requested_gender = request.args.get('gender')
    sort_by = request.args.get('sort', default='newest')
    
    # Searching
    if search_word:
        query = query.filter(
            or_(
                User.first_name.ilike(f"%{search_word}%"),
                User.last_name.ilike(f"%{search_word}%"),
                User.bio.ilike(f"%{search_word}%")
            )
        )
    
    # Filtering location by city or country
    if cities or countries:
        query = query.join(Location)
    
        if cities:
            query = query.filter(Location.city.ilike(f"%{cities}%"))
        if countries:
            query = query.filter(Location.country.ilike(f"%{countries}%"))
    
    # Age Range 
    today = date.today()
    
    if min_age:
        max_dob = today - timedelta(days=min_age * 365)
        query = query.filter(User.date_of_birth >= max_dob)
    
    if max_age:
        min_dob = today - timedelta(days=max_age * 365)
        query = query.filter(User.date_of_birth >= min_dob)
        
    # Filtering by Interests
    if selected_interests:
        interest_ids = [int(i) for i in interest_ids.split(',')]
        query = query.join(User_Interest).filter(User_Interest.interestID.in_(interest_ids))
    
    # Additional Criteria (gender & profile visibility)
    if requested_gender:
        query = query.filter(User.gender == requested_gender)
    
    query = query.filter(User.profile_visibility == 'public')
        
    # Sorting
    if sort_by == "newest":
        query = query.order_by(User.created_at.desc())
    elif sort_by == "oldest":
        query = query.order_by(User.created_at.asc())
    elif sort_by == "similiar":
        query = query.outerjoin(User_Interest) \
            .group_by(User.userID) \
            .order_by(db.func.count(User_Interest.interestID).desc())
    
    # Execute query 
    users = query.all()
    
    def calculate_age(dob):
        if not dob:
            return None 
        return today.year - dob.year - (
            (today.month, today.day) < (dob.moth, dob.day)
        )

    return jsonify([
        {
            "id": u.userID,
            "name": f"{u.first_name} {u.last_name}",
            "bio": u.bio,
            "age": calculate_age(u.date_of_birth)
        } for u in users
    ]) 
    

@app.route('/api/favourites', methods=['POST'])
def favourite_profile():
    data = request.json
    
    favourite = Favourite(
        user_id=data["userID"],
        saved_user_id=data["saved_user_id"]
    )
    db.session.add(favourite)
    db.session.commit()
    
    return jsonify({"message": "Favourite profiles saved."}), 201

@app.route('/api/favourites/<int:userID>', methods=['GET'])
def get_favourite(user_id):
    favourites = Favourite.query.filter_by(userID=user_id).all()
    
    results = [
        {
        "saved_user_id": f.saved_user_id
        }
        for f in favourites 
    ]
    
    return jsonify(results)  
    
   
###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404