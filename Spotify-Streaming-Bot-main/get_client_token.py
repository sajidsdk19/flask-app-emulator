"""
Get a Spotify access token using Client Credentials flow
"""
import base64
import requests

# Your Spotify App Credentials
CLIENT_ID = "479b522c097b419cb15a02a04956d5f9"
CLIENT_SECRET = "85aab30221f84db785c5c83c10119ded"
TOKEN_URL = 'https://accounts.spotify.com/api/token'

def get_client_credentials_token():
    """Get access token using Client Credentials flow"""
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
        
        print("✅ Successfully obtained access token!")
        print(f"\nAccess Token: {token_data.get('access_token')}")
        print(f"Token Type: {token_data.get('token_type')}")
        print(f"Expires In: {token_data.get('expires_in')} seconds")
        
        # Copy this token to your simple_bot.py file
        print("\n🔑 Copy the access token above and update the ACCESS_TOKEN in simple_bot.py")
        
        return token_data.get('access_token')
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting access token: {e}")
        if hasattr(e, 'response') and e.response.text:
            print(f"Error details: {e.response.text}")
        return None

if __name__ == "__main__":
    get_client_credentials_token()
