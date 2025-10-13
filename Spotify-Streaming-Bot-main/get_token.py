"""
Get a Spotify access token using Client Credentials flow
"""
import base64
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Spotify API credentials
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
TOKEN_URL = 'https://accounts.spotify.com/api/token'

def get_access_token():
    """Get access token using Client Credentials flow"""
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ Error: Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env file")
        return None
    
    # Create the authorization header
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    
    headers = {
        'Authorization': f'Basic {auth_base64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'client_credentials'
    }
    
    try:
        response = requests.post(TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        
        # Print the token information
        print("✅ Successfully obtained access token!")
        print(f"\nAccess Token: {token_data.get('access_token')}")
        print(f"Token Type: {token_data.get('token_type')}")
        print(f"Expires In: {token_data.get('expires_in')} seconds")
        
        # Save to .env file
        with open('.env', 'a') as f:
            f.write(f"\n# Spotify Access Token\nSPOTIFY_ACCESS_TOKEN={token_data.get('access_token')}")
        
        return token_data.get('access_token')
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting access token: {e}")
        if hasattr(e, 'response') and e.response.text:
            print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    get_access_token()
