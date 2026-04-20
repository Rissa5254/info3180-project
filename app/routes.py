from flask import request, jsonify, session
from app import app, db
from models import Message
from datetime import datetime

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
        timestamp=datetime.utcnow()
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