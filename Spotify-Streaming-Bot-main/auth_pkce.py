"""
Spotify Authorization Code with PKCE Flow
"""
import os
import base64
import hashlib
import requests
import webbrowser
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
from urllib.parse import parse_qs
import threading

# Your Spotify App Credentials
CLIENT_ID = "479b522c097b419cb15a02a04956d5f9"
REDIRECT_URI = "http://localhost:8888/callback"

# Generate code verifier and challenge
def generate_code_verifier(length=128):
    # Generate a random string of specified length
    import random
    import string
    chars = string.ascii_letters + string.digits + '-._~'
    return ''.join(random.choice(chars) for _ in range(length))

def generate_code_challenge(code_verifier):
    # Generate the code challenge using SHA-256
    hashed = hashlib.sha256(code_verifier.encode('ascii')).digest()
    # Base64 URL-safe encode the hash and remove padding
    return base64.urlsafe_b64encode(hashed).decode('ascii').replace('=', '')

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Parse the URL and query parameters
        parsed_url = urlparse.urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        if 'code' in query_params:
            code = query_params['code'][0]
            self.wfile.write(b"""
                <html>
                    <body>
                        <h2>Success!</h2>
                        <p>You can close this window and return to the terminal.</p>
                        <script>window.close();</script>
                    </body>
                </html>
            """)
            
            # Exchange the authorization code for an access token
            token_url = 'https://accounts.spotify.com/api/token'
            payload = {
                'client_id': CLIENT_ID,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': REDIRECT_URI,
                'code_verifier': self.server.code_verifier
            }
            
            response = requests.post(token_url, data=payload)
            token_data = response.json()
            
            if 'access_token' in token_data:
                print("\n✅ Successfully obtained access token!")
                print("\nAccess Token:")
                print("-" * 50)
                print(token_data['access_token'])
                print("-" * 50)
                print("\nRefresh Token:")
                print(token_data.get('refresh_token', 'No refresh token provided'))
                print("\nExpires in:", token_data.get('expires_in', 'Unknown'), "seconds")
                
                # Save to .env file
                with open('.env', 'a') as f:
                    f.write(f"\n# Spotify Access Token\nSPOTIFY_ACCESS_TOKEN={token_data['access_token']}")
                print("\n✅ Token saved to .env file as SPOTIFY_ACCESS_TOKEN")
            else:
                print("\n❌ Error getting access token:")
                print(json.dumps(token_data, indent=2))
            
            # Stop the server
            threading.Thread(target=self.server.shutdown, daemon=True).start()
        else:
            self.wfile.write(b"Error: No authorization code found in the callback URL")

def start_auth_flow():
    # Generate PKCE code verifier and challenge
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    
    # Start the web server in a separate thread
    server = HTTPServer(('localhost', 8888), CallbackHandler)
    server.code_verifier = code_verifier  # Store the verifier for later use
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Generate the authorization URL
    auth_url = (
        f"https://accounts.spotify.com/authorize?"
        f"client_id={CLIENT_ID}&"
        "response_type=code&"
        f"redirect_uri={REDIRECT_URI}&"
        "scope=user-read-playback-state user-modify-playback-state streaming&"
        f"code_challenge_method=S256&"
        f"code_challenge={code_challenge}"
    )
    
    print("🔗 Opening Spotify authorization in your browser...")
    print("Please log in with your Spotify account and grant the requested permissions.")
    print("\nIf the browser doesn't open automatically, visit this URL:")
    print("-" * 50)
    print(auth_url)
    print("-" * 50)
    
    # Open the authorization URL in the default web browser
    webbrowser.open(auth_url)
    
    # Wait for the server to be stopped by the callback
    server_thread.join()

if __name__ == "__main__":
    print("🚀 Starting Spotify PKCE Authorization Flow...")
    start_auth_flow()
