from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def messages():
    return "welcome to chatterbox"

@app.route('/messages', methods=['GET'])
def get_messages():
    # Retrieve all messages from the database and return them as JSON
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.serialize() for message in messages])

@app.route('/messages/<int:id>', methods=['GET'])
def get_message_by_id(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'message': 'Message not found'}), 404
    return jsonify(message.serialize())

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.serialize()), 201

# @app.route('/messages/<int:id>', methods=['PATCH'])
# def update_message(id):
#     message = Message.query.get(id)
#     if not message:
#         return jsonify({'message': 'Message not found'}), 404
#     data = request.get_json()
#     message.body = data['body']
#     db.session.commit()
#     return jsonify(message.serialize())
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'message': 'Message not found'}), 404
    
    data = request.get_json()
    new_username = data.get('username')  # Get the new username from the request
    
    # Update the username if it's provided in the request
    if new_username is not None:
        message.username = new_username
    
    db.session.commit()
    return jsonify(message.serialize())
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'message': 'Message not found'}), 404
    db.session.delete(message)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(port=5555)