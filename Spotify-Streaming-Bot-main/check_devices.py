import requests
import json

# Spotify API Base URL
API_BASE = "https://api.spotify.com/v1"

def get_devices(access_token):
    """
    Fetch the list of available Spotify devices with better error handling
    """
    url = f"{API_BASE}/me/player/devices"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Try to parse JSON response
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            response_data = {}
            
        # Check for HTTP errors
        if response.status_code == 200:
            return response_data
        elif response.status_code == 204:
            print(" No active device found. Please make sure Spotify is open on one of your devices.")
            return None
        else:
            print(f" Error {response.status_code}: {response.reason}")
            if response_data.get('error'):
                print(f"Message: {response_data['error'].get('message', 'No error message')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f" Request failed: {e}")
        return None

def get_user_profile(access_token):
    """
    Fetch the current user's profile to verify authentication
    """
    url = f"{API_BASE}/me"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f" Failed to fetch user profile: {e}")
        return None

if __name__ == "__main__":
    # Get the access token from simple_bot.py
    try:
        from simple_bot import ACCESS_TOKEN
    except (ImportError, AttributeError):
        print(" Could not import ACCESS_TOKEN from simple_bot.py")
        print("   Please make sure the token is properly set in simple_bot.py")
        exit(1)
    
    print(" Verifying authentication...")
    user_profile = get_user_profile(ACCESS_TOKEN)
    
    if user_profile and 'id' in user_profile:
        print(f" Authenticated as: {user_profile.get('display_name', 'Unknown User')}")
        print(f"   User ID: {user_profile['id']}")
        print(f"   Email: {user_profile.get('email', 'Not available')}")
        
        print("\n Fetching your Spotify devices...")
        result = get_devices(ACCESS_TOKEN)
        
        if result and 'devices' in result and result['devices']:
            print("\n Available devices:")
            for i, device in enumerate(result['devices'], 1):
                print(f"\n{i}. {device['name']} ({device['type']})")
                print(f"   ID: {device['id']}")
                print(f"   Active: {' Yes' if device['is_active'] else ' No'}")
                print(f"   Volume: {device.get('volume_percent', 'N/A')}%")
        else:
            print("\n No active devices found. Please make sure:")
            print("   1. Spotify is open on at least one device")
            print("   2. The device is connected to the internet")
            print("   3. You're using a Premium account")
    else:
        print(" Authentication failed. Please check your access token in simple_bot.py")
        print("   Make sure the token is valid and has the required scopes:")
        print("   - user-read-playback-state")
        print("   - user-modify-playback-state")
        print("   - user-read-currently-playing")
        print("\n   You can get a new token by running: python get_client_token.py")
