"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db, login_manager
from datetime import datetime, timezone
from flask import render_template, request, jsonify, session, send_file
import os
from app.models import User, Location, Interest, Match, Message, Favourite, Notification 

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")




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