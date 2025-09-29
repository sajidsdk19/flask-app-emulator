#!/usr/bin/env python3
"""
Helper script to obtain a Spotify refresh token through OAuth flow.
Run this once to get your refresh token, then use it with the main bot.
"""

import base64
import urllib.parse
import webbrowser
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

# Your app credentials
CLIENT_ID = "479b522c097b419cb15a02a04956d5f9"
CLIENT_SECRET = "85aab30221f84db785c5c83c10119ded"
REDIRECT_URI = "http://localhost:8888/callback"

# Spotify URLs
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

# Required scopes for the bot
SCOPES = [
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing"
]

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/callback'):
            # Parse the authorization code from the callback
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            
            if 'code' in params:
                auth_code = params['code'][0]
                self.server.auth_code = auth_code
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'''
                <html>
                <body>
                    <h1>Authorization Successful!</h1>
                    <p>You can close this window and return to the terminal.</p>
                </body>
                </html>
                ''')
            else:
                # Send error response
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                error = params.get('error', ['Unknown error'])[0]
                self.wfile.write(f'<h1>Authorization Failed</h1><p>Error: {error}</p>'.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def get_refresh_token():
    print("🎵 Spotify Refresh Token Generator")
    print("=" * 40)
    
    # Step 1: Build authorization URL
    auth_params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': ' '.join(SCOPES),
        'show_dialog': 'true'
    }
    
    auth_url = f"{AUTH_URL}?" + urllib.parse.urlencode(auth_params)
    
    print(f"1. Opening browser for Spotify authorization...")
    print(f"   If browser doesn't open, visit: {auth_url}")
    
    # Step 2: Start local server to receive callback
    server = HTTPServer(('localhost', 8888), CallbackHandler)
    server.auth_code = None
    
    # Start server in background thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Open browser
    webbrowser.open(auth_url)
    
    print("2. Waiting for authorization...")
    print("   Please log in to Spotify and authorize the application.")
    
    # Wait for authorization code
    timeout = 120  # 2 minutes timeout
    start_time = time.time()
    
    while server.auth_code is None and (time.time() - start_time) < timeout:
        time.sleep(1)
    
    server.shutdown()
    
    if server.auth_code is None:
        print("❌ Authorization timed out or failed.")
        return None
    
    print("3. Authorization code received! Exchanging for tokens...")
    
    # Step 3: Exchange authorization code for tokens
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    
    token_data = {
        'grant_type': 'authorization_code',
        'code': server.auth_code,
        'redirect_uri': REDIRECT_URI
    }
    
    token_headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        response = requests.post(TOKEN_URL, data=token_data, headers=token_headers)
        response.raise_for_status()
        
        tokens = response.json()
        refresh_token = tokens.get('refresh_token')
        
        if refresh_token:
            print("✅ Success! Your refresh token:")
            print("=" * 50)
            print(refresh_token)
            print("=" * 50)
            print("\n📝 Next steps:")
            print("1. Copy the refresh token above")
            print("2. Set it as environment variable: SPOTIFY_REFRESH_TOKEN")
            print("   OR add it directly to the main script")
            print("\n💡 To set environment variable:")
            print(f'   set SPOTIFY_REFRESH_TOKEN={refresh_token}')
            
            return refresh_token
        else:
            print("❌ No refresh token in response:", tokens)
            return None
            
    except requests.RequestException as e:
        print(f"❌ Token exchange failed: {e}")
        return None

if __name__ == "__main__":
    get_refresh_token()
