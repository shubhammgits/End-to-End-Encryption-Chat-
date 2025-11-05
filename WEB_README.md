# Web-Based Secure Chat Application

This is a web version of your end-to-end encrypted chat application that works like WhatsApp - no complex setup required!

## Features

- End-to-end encryption using RSA keys (same as your desktop version)
- Modern web interface that works on any device with a browser
- No installation required for users (just open a web page)
- Secure messaging between multiple users
- Works on mobile and desktop browsers

## How to Run

1. Make sure you have Python installed (3.8 or higher)
2. Run the application:
   ```
   python run_web_app.py
   ```
3. Open your browser and go to http://localhost:5000
4. Share the URL with others on your network:
   - Find your IP address: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
   - Others can access via: `http://YOUR_IP_ADDRESS:5000`

## How It Works

1. When you open the web page, the browser automatically generates RSA encryption keys
2. Your public key is sent to the server
3. When others connect, they get your public key
4. Messages are encrypted with the recipient's public key
5. Only the recipient can decrypt messages with their private key
6. All encryption/decryption happens in the browser - keys never leave your device

## Deployment Options

### Local Network (Easiest)
- Run the server on one computer
- Others connect using the IP address of that computer

### Internet Access (Free Options)
1. **Using ngrok**:
   - Install ngrok: https://ngrok.com/
   - Run: `ngrok http 5000`
   - Share the provided URL

2. **Using localhost.run**:
   - Run: `ssh -R 80:localhost:5000 nokey@localhost.run`
   - Share the provided URL

## Security Notes

- All messages are end-to-end encrypted
- Private keys are generated and stored only in your browser
- Keys are never sent to the server
- Server only facilitates key exchange and message routing
- Messages are encrypted before being sent over the network

## Troubleshooting

1. If the web page doesn't load, make sure the server is running
2. If others can't connect, check your firewall settings
3. For internet access, you may need to configure port forwarding on your router