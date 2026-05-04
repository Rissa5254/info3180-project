"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, jsonify, send_file
import os
from app.models import User, Location, Interest, Match, Message, Favourite, Notification 
from flask_login import current_user

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


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

from flask_login import current_user

@app.route('/api/messages/<int:receiver_id>', methods=['GET'])
def get_messages(receiver_id):
    # Find the match between current user and receiver
    match = Match.query.filter(
        ((Match.user1_id == current_user.userID) & (Match.user2_id == receiver_id)) |
        ((Match.user1_id == receiver_id) & (Match.user2_id == current_user.userID))
    ).first()

    if not match:
        return jsonify([])

    msgs = Message.query.filter_by(matchID=match.matchID).order_by(Message.timestamp).all()
    return jsonify([
        {
            'messageID': m.messageID,
            'senderID': m.senderID,
            'content': m.content,
            'timestamp': m.timestamp.isoformat()
        } for m in msgs
    ])

@app.route('/api/messages', methods=['POST'])
def send_message():
    data = request.get_json()
    receiver_id = data.get('receiver_id')
    content = data.get('content')

    match = Match.query.filter(
        ((Match.user1_id == current_user.userID) & (Match.user2_id == receiver_id)) |
        ((Match.user1_id == receiver_id) & (Match.user2_id == current_user.userID))
    ).first()

    if not match:
        return jsonify({'error': 'No match found'}), 404

    msg = Message(matchID=match.matchID, senderID=current_user.userID, content=content)
    db.session.add(msg)
    db.session.commit()

    return jsonify({'message': 'Sent'}), 201

