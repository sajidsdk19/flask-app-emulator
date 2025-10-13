#!/usr/bin/env python3
"""
Simple Spotify bot that works directly with access tokens
"""
import requests
import time
import json

# Spotify API Configuration
API_BASE = "https://api.spotify.com/v1"

# Access Token - Replace this with a new one if it expires
ACCESS_TOKEN = "BQD-jnfMar7O15TFKiV87BlC1DLN9SlW3X9ONamA0E8S6gUKN4d5J6frKpDJn-RKTnXnpszETE7nwbbNmp26z7-ufNjPPOfrAY3bwJVfIWptSzWDJOy9TN1cxp16ZPP6vLQK6cXqcbcvu2QYUrPKvw_eRPCvKjUoGMOzJeB8w5PnqCee07CgJk8PUn5QowltXVw5zFHbwRpqh0EykmhVlH4UleW2c0vpP41Nm0PnVRQF9JoDAAPWZG4QSj1eD2HtaKpkQ4Tr0FqxKhcpiXEAFdWLrFkfwPOPSPkPd_FxIeVLUSdQQ9d30TMkZl621X-U4Dxm"

# Required scopes for the bot
REQUIRED_SCOPES = [
    'user-read-playback-state',
    'user-modify-playback-state'
]

def check_token_scopes():
    """Check if the current token has the required scopes"""
    try:
        response = requests.get(
            f"{API_BASE}/me",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        if response.status_code == 200:
            return True, "Token is valid and has required scopes"
        else:
            return False, f"Token error: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"Error checking token: {str(e)}"

def make_request(endpoint, method="GET", data=None):
    """Make a request to Spotify API with enhanced error handling"""
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    url = f"{API_BASE}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            print(f"❌ Unsupported HTTP method: {method}")
            return None
            
        # Debug output
        print(f"\n🔍 Request: {method} {endpoint}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201, 202, 204]:
            return response.json() if response.text else {}
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
            # Check for common issues
            if response.status_code == 401:
                print("⚠️  Token might be expired or have insufficient scopes")
                print("    Try getting a new token with the required scopes:")
                print("    user-read-playback-state, user-modify-playback-state")
            
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON response: {str(e)}")
        return None

def get_user_profile():
    """Get current user profile"""
    print("👤 Getting user profile...")
    profile = make_request("/me")
    if profile:
        print(f"✅ User: {profile.get('display_name', 'Unknown')}")
        print(f"📧 Email: {profile.get('email', 'N/A')}")
        print(f"🎵 Subscription: {profile.get('product', 'N/A')}")
        return profile
    return None

def get_devices():
    """Get available devices"""
    print("\n📱 Getting available devices...")
    devices_data = make_request("/me/player/devices")
    if devices_data:
        devices = devices_data.get("devices", [])
        print(f"Found {len(devices)} device(s):")
        for i, device in enumerate(devices):
            status = "🟢 ACTIVE" if device['is_active'] else "⚪ INACTIVE"
            print(f"  {i+1}. {device['name']} ({device['type']}) - {status}")
            print(f"     ID: {device['id']}")
        return devices
    return []

def get_top_tracks():
    """Get user's top tracks"""
    print("\n🎵 Getting your top tracks...")
    tracks_data = make_request("/me/top/tracks?limit=5")
    if tracks_data:
        tracks = tracks_data.get("items", [])
        print("Your top tracks:")
        for i, track in enumerate(tracks, 1):
            artists = ", ".join([artist['name'] for artist in track['artists']])
            print(f"  {i}. {track['name']} by {artists}")
        return tracks
    return []

def start_playback(device_id=None, context_uri=None, uris=None):
    """Start playback"""
    endpoint = "/me/player/play"
    if device_id:
        endpoint += f"?device_id={device_id}"
    
    data = {}
    if context_uri:
        data["context_uri"] = context_uri
    if uris:
        data["uris"] = uris
    
    print(f"\n▶️  Starting playback...")
    result = make_request(endpoint, "PUT", data)
    if result is not None:
        print("✅ Playback started!")
        return True
    return False

def pause_playback(device_id=None):
    """Pause playback"""
    endpoint = "/me/player/pause"
    if device_id:
        endpoint += f"?device_id={device_id}"
    
    print("⏸️  Pausing playback...")
    result = make_request(endpoint, "PUT")
    if result is not None:
        print("✅ Playback paused!")
        return True
    return False

def set_shuffle(device_id, state=True):
    """Set shuffle mode"""
    endpoint = f"/me/player/shuffle?state={str(state).lower()}"
    if device_id:
        endpoint += f"&device_id={device_id}"
    
    print(f"🔀 Setting shuffle to {state}...")
    result = make_request(endpoint, "PUT")
    if result is not None:
        print("✅ Shuffle updated!")
        return True
    return False

def run_session():
    """Run an interactive session"""
    print("🎵 Spotify Bot - Interactive Session")
    print("=" * 50)
    
    # Get user profile
    profile = get_user_profile()
    if not profile:
        print("❌ Failed to get user profile. Check your token.")
        return
    
    # Get devices
    devices = get_devices()
    if not devices:
        print("⚠️  No devices found. Please open Spotify on a device first!")
        return
    
    # Get top tracks
    get_top_tracks()
    
    print("\n" + "=" * 50)
    print("🎮 What would you like to do?")
    print("1. Play a playlist")
    print("2. Play specific tracks")
    print("3. Just test playback controls")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        # Play playlist
        device_idx = input(f"\nSelect device (1-{len(devices)}): ").strip()
        try:
            device_id = devices[int(device_idx)-1]['id']
            playlist_uri = input("Enter playlist URI (or press Enter for Today's Top Hits): ").strip()
            if not playlist_uri:
                playlist_uri = "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M"
            
            # Set shuffle
            set_shuffle(device_id, True)
            
            # Start playback
            if start_playback(device_id, context_uri=playlist_uri):
                duration = input("How long to play? (seconds, default 60): ").strip()
                duration = int(duration) if duration else 60
                
                print(f"🎵 Playing for {duration} seconds...")
                time.sleep(duration)
                
                pause_playback(device_id)
        except (ValueError, IndexError):
            print("❌ Invalid device selection")
    
    elif choice == "2":
        # Play specific tracks
        print("Enter track URIs (comma-separated):")
        print("Example: spotify:track:4iV5W9uYEdYUVa79Axb7Rh,spotify:track:1301WleyT98MSxVHPZCA6M")
        uris_input = input("Track URIs: ").strip()
        
        if uris_input:
            uris = [uri.strip() for uri in uris_input.split(",")]
            device_idx = input(f"\nSelect device (1-{len(devices)}): ").strip()
            try:
                device_id = devices[int(device_idx)-1]['id']
                
                if start_playback(device_id, uris=uris):
                    duration = input("How long to play? (seconds, default 30): ").strip()
                    duration = int(duration) if duration else 30
                    
                    print(f"🎵 Playing for {duration} seconds...")
                    time.sleep(duration)
                    
                    pause_playback(device_id)
            except (ValueError, IndexError):
                print("❌ Invalid device selection")
    
    elif choice == "3":
        # Test controls
        device_idx = input(f"\nSelect device (1-{len(devices)}): ").strip()
        try:
            device_id = devices[int(device_idx)-1]['id']
            
            print("Testing playback controls...")
            start_playback(device_id, context_uri="spotify:playlist:37i9dQZF1DXcBWIGoYBM5M")
            time.sleep(5)
            
            set_shuffle(device_id, True)
            time.sleep(3)
            
            pause_playback(device_id)
            print("✅ Test completed!")
            
        except (ValueError, IndexError):
            print("❌ Invalid device selection")
    
    elif choice == "4":
        print("👋 Goodbye!")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    print("🔍 Checking token permissions...")
    is_valid, message = check_token_scopes()
    print(f"🔑 Token status: {'✅' if is_valid else '❌'} {message}")
    
    if is_valid:
        print("\n🎵 Starting Spotify Bot...")
        run_session()
    else:
        print("\n❌ Please fix the token issues before continuing.")
        print("   Get a new token with these scopes:")
        print("   - user-read-playback-state")
        print("   - user-modify-playback-state")
        print("\n   Use this URL to get a new token (replace CLIENT_ID with your actual client ID):")
        print(f"   https://accounts.spotify.com/authorize?client_id=YOUR_CLIENT_ID&response_type=token&redirect_uri=http://localhost:8888/callback&scope=user-read-playback-state%20user-modify-playback-state&show_dialog=true")
