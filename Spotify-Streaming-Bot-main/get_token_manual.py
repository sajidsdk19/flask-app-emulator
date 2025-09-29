#!/usr/bin/env python3
"""
Manual method to get Spotify refresh token.
This method doesn't require setting up redirect URIs in your Spotify app.
"""

import base64
import urllib.parse
import requests

# Your app credentials
CLIENT_ID = "479b522c097b419cb15a02a04956d5f9"
CLIENT_SECRET = "85aab30221f84db785c5c83c10119ded"

# Use a simple redirect URI that doesn't require server setup
REDIRECT_URI = "https://example.com/callback"

# Spotify URLs
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

# Required scopes
SCOPES = [
    "user-read-playback-state",
    "user-modify-playback-state", 
    "user-read-currently-playing"
]

def get_authorization_url():
    """Generate the authorization URL for manual process."""
    auth_params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': ' '.join(SCOPES),
        'show_dialog': 'true'
    }
    
    return f"{AUTH_URL}?" + urllib.parse.urlencode(auth_params)

def exchange_code_for_token(auth_code):
    """Exchange authorization code for refresh token."""
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    
    token_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
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
        return tokens.get('refresh_token')
        
    except requests.RequestException as e:
        print(f"❌ Token exchange failed: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

def main():
    print("🎵 Spotify Refresh Token - Manual Method")
    print("=" * 50)
    
    # Step 1: Show authorization URL
    auth_url = get_authorization_url()
    print("\n📋 STEP 1: Copy and paste this URL into your browser:")
    print("-" * 60)
    print(auth_url)
    print("-" * 60)
    
    print("\n📋 STEP 2: After logging in and authorizing:")
    print("1. You'll be redirected to example.com (this will show an error page)")
    print("2. Look at the URL in your browser address bar")
    print("3. Copy the 'code' parameter from the URL")
    print("   Example: https://example.com/callback?code=COPY_THIS_PART")
    
    print("\n📋 STEP 3: Enter the authorization code below:")
    auth_code = input("Paste the authorization code here: ").strip()
    
    if not auth_code:
        print("❌ No authorization code provided.")
        return
    
    print("\n🔄 Exchanging code for refresh token...")
    refresh_token = exchange_code_for_token(auth_code)
    
    if refresh_token:
        print("\n✅ SUCCESS! Your refresh token:")
        print("=" * 60)
        print(refresh_token)
        print("=" * 60)
        print("\n📝 Save this refresh token - you'll need it to run the bot!")
        
        # Offer to add it directly to the main script
        add_to_script = input("\nWould you like me to add this to your bot script automatically? (y/n): ").strip().lower()
        if add_to_script in ['y', 'yes']:
            try:
                # Read the main script
                with open('spotify-bots.py', 'r') as f:
                    content = f.read()
                
                # Add the refresh token
                if 'DEFAULT_CLIENT_SECRET' in content:
                    new_content = content.replace(
                        'DEFAULT_CLIENT_SECRET = "85aab30221f84db785c5c83c10119ded"',
                        f'DEFAULT_CLIENT_SECRET = "85aab30221f84db785c5c83c10119ded"\nDEFAULT_REFRESH_TOKEN = "{refresh_token}"'
                    )
                    
                    # Update the main function to use the default refresh token
                    new_content = new_content.replace(
                        'refresh_token = require_env("SPOTIFY_REFRESH_TOKEN")',
                        'refresh_token = require_env("SPOTIFY_REFRESH_TOKEN", DEFAULT_REFRESH_TOKEN)'
                    )
                    
                    # Write back to file
                    with open('spotify-bots.py', 'w') as f:
                        f.write(new_content)
                    
                    print("✅ Refresh token added to spotify-bots.py!")
                    print("🚀 You can now run: python spotify-bots.py --list-devices")
                else:
                    print("❌ Could not automatically add to script. Please add manually.")
                    
            except Exception as e:
                print(f"❌ Error updating script: {e}")
                print("Please add the refresh token manually.")
    else:
        print("❌ Failed to get refresh token.")

if __name__ == "__main__":
    main()
