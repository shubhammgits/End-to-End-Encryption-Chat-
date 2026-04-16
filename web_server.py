import logging
import os
import secrets

from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', secrets.token_urlsafe(32))
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory storage for clients and their public keys
# sid -> publicKeyString (base64 SPKI)
clients = {}

# Serve the web client
@app.route('/')
def index():
    return send_from_directory('.', 'web_client.html')

def send_keys_update():
    """Send updated list of public keys to each connected client (excluding itself)."""
    for sid in list(clients.keys()):
        other_keys = {other_sid: key for other_sid, key in clients.items() if other_sid != sid}
        socketio.emit('keys_update', {'keys': other_keys}, room=sid)


# SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    logger.info("New connection established")


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in clients:
        clients.pop(sid, None)
        send_keys_update()
    logger.info("Client disconnected")


@socketio.on('register_client')
def handle_register_client(data):
    sid = request.sid
    key = (data or {}).get('key')
    if not isinstance(key, str) or not key:
        emit('error', {'message': 'Missing public key'}, room=sid)
        return

    clients[sid] = key
    logger.info("Registered client public key")
    send_keys_update()


@socketio.on('encrypted_message')
def handle_encrypted_message(data):
    sid = request.sid
    message = (data or {}).get('message')
    to_sid = (data or {}).get('to')

    if not isinstance(message, str) or not message:
        emit('error', {'message': 'Missing message'}, room=sid)
        return
    if not isinstance(to_sid, str) or not to_sid:
        emit('error', {'message': 'Missing recipient'}, room=sid)
        return
    if to_sid not in clients:
        emit('error', {'message': 'Recipient not connected'}, room=sid)
        return

    emit('encrypted_message', {'message': message, 'from': sid}, room=to_sid)


if __name__ == '__main__':
    # Start Flask server
    port = int(os.environ.get('PORT', '5000'))
    logger.info(f"Starting web server on http://0.0.0.0:{port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)