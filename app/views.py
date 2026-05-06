"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
from app import app, db
from datetime import date, datetime, timezone, timedelta
from flask import flash, current_app, render_template, request, session, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from app.models import User, Location, Interest, User_Interest, Match, Message, Favourite, Notification


###
# Routing for your application.
###
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


# 1. User Authentication and Profile Management
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username', '').strip()
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    date_of_birth = data.get('date_of_birth')
    gender = data.get('gender')
    looking_for = data.get('looking_for')

    if not username or not email or not password:
        return jsonify({
            "error": "Username, email, and password are required."
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must be at least 8 characters."
        }), 400

    if User.query.filter_by(username=username).first():
        return jsonify({
            "error": "Username already exists."
        }), 409

    if User.query.filter_by(email=email).first():
        return jsonify({
            "error": "Email already exists."
        }), 409

    dob_value = None

    if date_of_birth:
        try:
            dob_value = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({
                "error": "Date of birth must be in YYYY-MM-DD format."
            }), 400

    user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        date_of_birth=dob_value,
        gender=gender,
        looking_for=looking_for,
        bio=None,
        locationID=None,
        preferred_radius=None,
        profile_picture=None,
        profile_visibility=True
    )

    db.session.add(user)
    db.session.commit()

    login_user(user)

    session['user_id'] = user.userID

    return jsonify({
        "message": "Registration successful.",
        "user": {
            "userID": user.userID,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }
    }), 201
    
    
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({
            "error": "Email and password are required."
        }), 400

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return jsonify({
            "error": "Invalid email or password."
        }), 401

    login_user(user)

    session['user_id'] = user.userID

    return jsonify({
        "message": "Login successful.",
        "user": {
            "userID": user.userID,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }
    }), 200


@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)

    return jsonify({
        "message": "Logout successful."
    }), 200
    
    
@app.route('/api/auth/check', methods=['GET'])
def check_auth():
    if not current_user.is_authenticated:
        return jsonify({
            "authenticated": False,
            "user": None
        }), 401

    return jsonify({
        "authenticated": True,
        "user": {
            "userID": current_user.userID,
            "username": current_user.username,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "email": current_user.email
        }
    }), 200
    
    
@app.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    user = current_user

    user_interests = Interest.query \
        .join(User_Interest, Interest.interestID == User_Interest.interestID) \
        .filter(User_Interest.userID == user.userID) \
        .all()

    return jsonify({
        "userID": user.userID,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
        "gender": user.gender,
        "looking_for": user.looking_for,
        "bio": user.bio,
        "profile_visibility": user.profile_visibility,
        "preferred_radius": user.preferred_radius,
        "profile_picture": user.profile_picture,
        "interests": [
            interest.interest_name for interest in user_interests
        ]
    }), 200
    
    
@app.route('/api/profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json()

    current_user.first_name = data.get('first_name', current_user.first_name)
    current_user.last_name = data.get('last_name', current_user.last_name)
    current_user.bio = data.get('bio', current_user.bio)
    current_user.gender = data.get('gender', current_user.gender)
    current_user.looking_for = data.get('looking_for', current_user.looking_for)
    current_user.preferred_radius = data.get('preferred_radius', current_user.preferred_radius)

    if 'profile_visibility' in data:
        current_user.profile_visibility = bool(data.get('profile_visibility'))

    if data.get('date_of_birth'):
        try:
            current_user.date_of_birth = datetime.strptime(
                data.get('date_of_birth'),
                "%Y-%m-%d"
            ).date()
        except ValueError:
            return jsonify({
                "error": "Date of birth must be in YYYY-MM-DD format."
            }), 400

    interests = data.get('interests', None)

    if interests is not None:
        cleaned_interests = []

        for interest_name in interests:
            interest_name = interest_name.strip().lower()

            if interest_name and interest_name not in cleaned_interests:
                cleaned_interests.append(interest_name)

        if len(cleaned_interests) < 3:
            return jsonify({
                "error": "Please enter at least 3 interests."
            }), 400

        User_Interest.query.filter_by(userID=current_user.userID).delete()

        for interest_name in cleaned_interests:
            interest = Interest.query.filter_by(interest_name=interest_name).first()

            if interest is None:
                interest = Interest(interest_name=interest_name)
                db.session.add(interest)
                db.session.flush()

            user_interest = User_Interest(
                userID=current_user.userID,
                interestID=interest.interestID
            )

            db.session.add(user_interest)

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully."
    }), 200
    
    
@app.route('/api/users/browse', methods=['GET'])
@login_required
def browse_users():
    users = User.query.filter(
        User.userID != current_user.userID,
        User.profile_visibility == True
    ).order_by(User.created_at.desc()).all()

    today = date.today()

    def calculate_age(dob):
        if not dob:
            return None

        return today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day)
        )

    results = []

    for user in users:
        interests = Interest.query \
            .join(User_Interest, Interest.interestID == User_Interest.interestID) \
            .filter(User_Interest.userID == user.userID) \
            .all()

        results.append({
            "userID": user.userID,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": calculate_age(user.date_of_birth),
            "gender": user.gender,
            "looking_for": user.looking_for,
            "bio": user.bio,
            "profile_picture": user.profile_picture,
            "interests": [interest.interest_name for interest in interests]
        })

    return jsonify(results), 200
     
    
@app.route('/api/profile/picture', methods=['POST'])
@login_required
def upload_profile_picture():
    if 'profile_picture' not in request.files:
        return jsonify({"error": "No profile picture uploaded."}), 400

    file = request.files['profile_picture']

    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only png, jpg, jpeg, and webp files are allowed."}), 400

    filename = secure_filename(file.filename)

    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    current_user.profile_picture = filename
    db.session.commit()

    return jsonify({
        "message": "Profile picture uploaded successfully.",
        "profile_picture": filename
    }), 200
    
    
# 2. Matching System






# 3. User Connections and Messaging
@app.route('/api/messages', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()

    receiver_id = data.get('receiver_id')
    content = data.get('content', '').strip()

    if not receiver_id:
        return jsonify({"error": "Receiver ID required"}), 400

    if not content:
        return jsonify({"error": "Empty message"}), 400

    receiver = User.query.get(receiver_id)
    if not receiver:
        return jsonify({"error": "User not found"}), 404

    match = Match.query.filter(
        ((Match.user1_id == current_user.userID) & (Match.user2_id == receiver_id)) |
        ((Match.user1_id == receiver_id) & (Match.user2_id == current_user.userID))
    ).first()

    if not match:
        return jsonify({"error": "No match"}), 403

    msg = Message(
        matchID=match.matchID,
        senderID=current_user.userID,
        content=content
    )

    db.session.add(msg)
    db.session.commit()

    return jsonify({"message": "Sent"}), 201

@app.route('/api/messages/<int:receiver_id>', methods=['GET'])
@login_required
def get_messages(receiver_id):

    receiver = User.query.get(receiver_id)
    if not receiver:
        return jsonify({"error": "User not found"}), 404

    match = Match.query.filter(
        ((Match.user1_id == current_user.userID) & (Match.user2_id == receiver_id)) |
        ((Match.user1_id == receiver_id) & (Match.user2_id == current_user.userID))
    ).first()

    if not match:
        return jsonify({"error": "No match"}), 403

    msgs = Message.query \
        .filter_by(matchID=match.matchID) \
        .order_by(Message.timestamp.asc()) \
        .all()

    return jsonify([
        {
            "messageID": m.messageID,
            "senderID": m.senderID,
            "content": m.content,
            "timestamp": m.timestamp.isoformat()
        }
        for m in msgs
    ]), 200

@app.route('/api/conversations', methods=['GET'])
@login_required
def get_conversations():

    matches = Match.query.filter(
        (Match.user1_id == current_user.userID) |
        (Match.user2_id == current_user.userID)
    ).all()

    conversations = []

    for m in matches:
        other_user_id = (
            m.user2_id if m.user1_id == current_user.userID
            else m.user1_id
        )

        other_user = User.query.get(other_user_id)

        last_message = Message.query \
            .filter_by(matchID=m.matchID) \
            .order_by(Message.timestamp.desc()) \
            .first()

        conversations.append({
            "userID": other_user.userID,
            "username": other_user.username,
            "profile_picture": other_user.profile_picture,
            "last_message": last_message.content if last_message else None,
            "timestamp": last_message.timestamp.isoformat() if last_message else None
        })

    return jsonify(conversations), 200

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
    
    query = query.filter(User.profile_visibility == True)
        
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
            (today.month, today.day) < (dob.month, dob.day)
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
def get_favourite(userID):
    favourites = Favourite.query.filter_by(userID=userID).all()
    
    results = [
        {
        "saved_user_id": f.saved_user_id
        }
        for f in favourites 
    ]
    
    return jsonify(results)  
    

# 5. Notification
@app.route('/api/notifications', methods=['GET'])
@login_required

#Return all notifications for logged in user (newest first)
def get_notifications():
    notifications = Notification.query.filter_by(userID=current_user.userID) \
        .order_by(Notification.created_at.desc()) \
        .all()

    results = []

    for notification in notifications:
        results.append({
            "notificationID": notification.notificationID,
            "type": notification.type,
            "content": notification.content,
            "is_read": notification.is_read,
            "created_at": notification.created_at.isoformat() if notification.created_at else None
        })

    return jsonify(results), 200


@app.route('/api/notifications/<int:notification_id>/read', methods=['PUT'])
@login_required

#Marks notifications as read
def mark_notification_read(notification_id):
    notification = Notification.query.filter_by(
        notificationID=notification_id,
        userID=current_user.userID
    ).first()

    # Checking if Notification exists
    if not notification:
        return jsonify({"error": "Notification not found."}), 404

    notification.is_read = True
    db.session.commit()

    return jsonify({"message": "Notification marked as read."}), 200
   

# 6. Block User
@app.route('/api/users/<int:user_id>/block', methods=['POST'])
@login_required

#Blocks user and prevents them from appear in browse results
def block_user(user_id):

    #Prevents a user from blocking themself
    if user_id == current_user.userID:
        return jsonify({"error": "You cannot block yourself."}), 400

    user_to_block = User.query.get(user_id)

    #Checking if a user exists
    if not user_to_block:
        return jsonify({"error": "User not found."}), 404

    existing_block = Block.query.filter_by(
        blockerID=current_user.userID,
        blockedID=user_id
    ).first()
 
    #Checking if a user is already blocked
    if existing_block:
        return jsonify({"error": "User already blocked."}), 409

    block = Block(
        blockerID=current_user.userID,
        blockedID=user_id
    )

    db.session.add(block)
    db.session.commit()

    return jsonify({"message": "User blocked successfully."}), 201


# View Blocked List
@app.route('/api/users/blocked', methods=['GET'])
@login_required
def get_blocked_users():
    blocks = Block.query.filter_by(blockerID=current_user.userID).all()

    results = []

    for block in blocks:
        user = User.query.get(block.blockedID)
        if user:
            results.append({
                "userID": user.userID,
                "username": user.username,
                "email": user.email
            })

    return jsonify(results), 200


# Unblock User
@app.route('/api/users/<int:user_id>/unblock', methods=['DELETE'])
@login_required

#Unblocks user so they appear in your browse results again
def unblock_user(user_id):
    block = Block.query.filter_by(
        blockerID=current_user.userID,
        blockedID=user_id
    ).first()

    #Checks if user wasn't blocked
    if not block:
        return jsonify({"error": "User not blocked."}), 404

    db.session.delete(block)
    db.session.commit()

    return jsonify({"message": "User unblocked successfully."}), 200


# 7. Report User
@app.route('/api/users/<int:user_id>/report', methods=['POST'])
@login_required

# Allows a user to report another with a reason
def report_user(user_id):

    #Prevents a user from reporting themself
    if user_id == current_user.userID:
        return jsonify({"error": "You cannot report yourself."}), 400

    user_to_report = User.query.get(user_id)

    #Checks if user exists
    if not user_to_report:
        return jsonify({"error": "User not found."}), 404

    data = request.get_json()
    reason = data.get("reason", "").strip()

    # Required check
    if not reason:
        return jsonify({"error": "Reason is required."}), 400

    # Length validation
    if len(reason) < 5:
        return jsonify({"error": "Reason too short."}), 400

    # Duplicate report prevention
    existing_report = Report.query.filter_by(
        reporterID=current_user.userID,
        reportedID=user_id
    ).first()

    if existing_report:
        return jsonify({"error": "User already reported."}), 409

    report = Report(
        reporterID=current_user.userID,
        reportedID=user_id,
        reason=reason
    )

    db.session.add(report)
    db.session.commit()

    return jsonify({"message": "User reported successfully."}), 201


   
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

