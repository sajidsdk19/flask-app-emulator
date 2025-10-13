#!/usr/bin/env python3
"""
Simple script to exchange authorization code for refresh token
"""
import requests
import base64

CLIENT_ID = "479b522c097b419cb15a02a04956d5f9"
CLIENT_SECRET = "85aab30221f84db785c5c83c10119ded"
REDIRECT_URI = "http://localhost:8888/callback"

def get_refresh_token(auth_code):
    # Encode credentials
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }
    
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"\n✅ SUCCESS! Your refresh token is:")
        print(f"🔑 REFRESH_TOKEN: {token_data['refresh_token']}")
        print(f"\n💾 Save this token - you'll need it to run the bot!")
        return token_data['refresh_token']
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        return None

if __name__ == "__main__":
    print("🎵 Spotify Token Exchange")
    print("=" * 50)
    print("\n1. Go to this URL:")
    print("https://accounts.spotify.com/authorize?client_id=479b522c097b419cb15a02a04956d5f9&response_type=code&redirect_uri=http://localhost:8888/callback&scope=user-read-playback-state%20user-modify-playback-state%20user-read-currently-playing")
    print("\n2. After authorization, copy the 'code' parameter from the redirect URL")
    
    auth_code = input("\n📋 Paste the authorization code here: ").strip()
    
    if auth_code:
        get_refresh_token(auth_code)
    else:
        print("❌ No authorization code provided")
