"""
Generate Spotify authorization URL with required scopes
"""

# Your Spotify App Credentials
CLIENT_ID = "479b522c097b419cb15a02a04956d5f9"
REDIRECT_URI = "http://localhost:8888/callback"

# Required scopes for the bot
SCOPES = [
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing',
    'streaming',
    'app-remote-control'
]

# Generate the authorization URL
auth_url = (
    f"https://accounts.spotify.com/authorize?"
    f"client_id={CLIENT_ID}&"
    f"response_type=token&"
    f"redirect_uri={REDIRECT_URI}&"
    f"scope={'%20'.join(SCOPES)}&"
    "show_dialog=true"
)

print("🔗 Here's your authorization URL. Open this in your browser:")
print("\n" + "="*80)
print(auth_url)
print("="*80)
print("\nAfter authorizing, you'll be redirected to a localhost URL.")
print("Copy the entire URL and paste it here so I can extract the access token.")
