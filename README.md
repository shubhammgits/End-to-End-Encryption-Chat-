# End-to-End Encryption Chat Application

This is a secure chat application with end-to-end encryption that can be hosted for free using tunneling services.

## Features
- End-to-end encryption using RSA keys
- Secure messaging between multiple users
- Modern GUI with CustomTkinter
- Cross-platform compatibility

## Setup Instructions

### Prerequisites
1. Python 3.8 or higher
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

### Running the Application Locally

1. Start the server:
   ```
   python server.py
   ```

2. Start clients (in separate terminals):
   ```
   python client.py
   ```

### Hosting Options for Free Public Access

#### Option 1: Using ngrok (Recommended)
Ngrok provides a free tier that allows you to expose your local server to the internet.

1. Install ngrok from https://ngrok.com/
2. Sign up for a free account and get your auth token
3. Authenticate ngrok:
   ```
   ngrok authtoken YOUR_AUTH_TOKEN
   ```
4. Start your chat server:
   ```
   python server.py
   ```
5. In a new terminal, start ngrok:
   ```
   ngrok tcp 65432
   ```
6. Share the ngrok URL with others (it will look like `tcp://0.tcp.ngrok.io:12345`)

#### Option 2: Using localhost.run
This is a simpler alternative to ngrok with no registration required.

1. Start your chat server:
   ```
   python server.py
   ```
2. In a new terminal, run:
   ```
   ssh -R 80:localhost:65432 nokey@localhost.run
   ```
3. Share the provided URL with others

#### Option 3: Using Cloudflare Tunnel (free tier)
Cloudflare Tunnel (formerly Argo Tunnel) offers a free tier for personal use.

1. Install cloudflared from https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
2. Start your chat server:
   ```
   python server.py
   ```
3. Create a tunnel:
   ```
   cloudflared tunnel --hostname your-subdomain.your-domain.com --url tcp://localhost:65432
   ```
4. Share the URL with others

### Connecting from Other Devices

When running on a local network, other devices can connect using:
```
python client.py YOUR_LOCAL_IP_ADDRESS 65432
```

Replace `YOUR_LOCAL_IP_ADDRESS` with the IP address of the machine running the server.

## Security Notes

- All messages are end-to-end encrypted using RSA keys
- Each client generates its own key pair
- Public keys are exchanged through the server
- Private keys never leave the client device
- Messages are encrypted with recipient's public key and can only be decrypted with their private key

## Troubleshooting

1. If clients can't connect, ensure the server machine's firewall allows connections on port 65432
2. For internet hosting, make sure your router's firewall allows incoming connections on the tunnel port
3. Some antivirus software may block incoming connections; you may need to add an exception