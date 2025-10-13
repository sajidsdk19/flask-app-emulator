"""
Spotify OAuth Authentication
This script helps you get an access token with the required permissions.
"""
import os
import webbrowser
import requests
from urllib.parse import urlencode
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Spotify API configuration
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8888/callback'  # Must match your app's redirect URI
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Required scopes for the bot
SCOPES = [
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing'
]

def get_auth_url():
    """Generate the authorization URL"""
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': ' '.join(SCOPES),
        'show_dialog': 'true'  # Force approval dialog
    }
    return f"{AUTH_URL}?{urlencode(params)}"

def get_access_token(auth_code):
    """Exchange authorization code for access token"""
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    
    headers = {
        'Authorization': f'Basic {auth_base64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }
    
    try:
        response = requests.post(TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting access token: {e}")
        if hasattr(e, 'response') and e.response.text:
            print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ Error: Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET in .env file")
        exit(1)
    
    # Step 1: Get authorization URL and open in browser
    auth_url = get_auth_url()
    print("🔑 Please authorize this application in your browser...")
    print(f"If the browser doesn't open, visit this URL manually:\n{auth_url}")
    webbrowser.open(auth_url)
    
    # Step 2: Get the authorization code from the redirect URL
    print("\nAfter authorizing, you'll be redirected to a localhost URL.")
    print("Paste the full URL you were redirected to below:")
    redirect_url = input("> ").strip()
    
    # Extract the authorization code from the URL
    try:
        from urllib.parse import parse_qs, urlparse
        query = parse_qs(urlparse(redirect_url).query)
        auth_code = query.get('code', [''])[0]
        
        if not auth_code:
            print("❌ No authorization code found in the URL")
            exit(1)
            
        # Step 3: Exchange the code for an access token
        print("\n🔑 Exchanging authorization code for access token...")
        token_data = get_access_token(auth_code)
        
        if token_data:
            print("\n✅ Success! Here are your tokens:")
            print(f"Access Token: {token_data.get('access_token')}")
            print(f"Refresh Token: {token_data.get('refresh_token')}")
            print(f"Expires In: {token_data.get('expires_in')} seconds")
            
            # Save tokens to .env file
            with open('.env', 'a') as f:
                f.write(f"\n# Spotify Tokens (generated on {time.strftime('%Y-%m-%d %H:%M:%S')})\n")
                f.write(f"SPOTIFY_ACCESS_TOKEN={token_data.get('access_token')}\n")
                f.write(f"SPOTIFY_REFRESH_TOKEN={token_data.get('refresh_token')}")
                
            print("\n🔒 Tokens have been saved to your .env file")
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")
