import json
import logging
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory storage for clients and their public keys
clients = {}  # sid -> {'public_key': key}

# Serve the web client
@app.route('/')
def index():
    return send_from_directory('.', 'web_client.html')

# SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    logger.info(f"New connection established")

@socketio.on('disconnect')
def handle_disconnect():
    logger.info("Client disconnected")

@socketio.on('register_client')
def handle_register_client(data):
    logger.info(f"Registered client with public key")
    # Send updated keys list to all clients
    send_keys_update()

@socketio.on('encrypted_message')
def handle_encrypted_message(data):
    logger.info(f"Received encrypted message")

def send_keys_update():
    """Send updated list of public keys to all connected clients"""
    logger.info("Sending keys update")

if __name__ == '__main__':
    # Start Flask server
    logger.info("Starting web server on http://0.0.0.0:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)