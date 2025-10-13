#!/usr/bin/env python3
"""
Test the provided access token and help get a refresh token
"""
import requests
import os

# Your access token
ACCESS_TOKEN = "BQBt-1mFW6V7uqoV7MHernuApj5sejOOI4JkN5XZH7F2zenZOk1W0ryG2e-T6-GOlXVMR-KpQHMqYSYXIEigKE3frUmVsAYMEPrPoFB8nfnaWRXJy9ts7l5m7aRvhS_5CLKvC2rrvEih73qfb7lNJBq19zFR69rUsTj0dbY06iFbbk2cMJtdiQRTuG3ihiKJy7WUQjpICYP6Pg52_d0SLK7eDqyFzD7q3kUXWalXgz5nUyTctVjeleoChnmim2kmircpyTrEVMjYDZ87FAgOh4Jcgrab0kOG43Epwb76tHaCfxJMCiUk-ZbjfwSAUVj9qba7"

def test_access_token():
    """Test if the access token works"""
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    print("🧪 Testing access token...")
    
    # Test user profile
    try:
        response = requests.get("https://api.spotify.com/v1/me", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Token works! User: {user_data.get('display_name', 'Unknown')}")
            print(f"📧 Email: {user_data.get('email', 'N/A')}")
            print(f"🎵 Subscription: {user_data.get('product', 'N/A')}")
            return True
        else:
            print(f"❌ Token failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing token: {e}")
        return False

def test_playback_control():
    """Test if we can control playback"""
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    print("\n🎮 Testing playback control...")
    
    # Get devices
    try:
        response = requests.get("https://api.spotify.com/v1/me/player/devices", headers=headers)
        if response.status_code == 200:
            devices = response.json().get("devices", [])
            print(f"📱 Found {len(devices)} device(s):")
            for device in devices:
                print(f"   - {device['name']} ({device['type']}) - Active: {device['is_active']}")
            return devices
        else:
            print(f"❌ Cannot get devices: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting devices: {e}")
        return []

def run_quick_test():
    """Run a quick test with the current access token"""
    print("🎵 Spotify Bot - Quick Test")
    print("=" * 50)
    
    if test_access_token():
        devices = test_playback_control()
        
        if devices:
            print(f"\n✅ Your token works! You can run the bot with:")
            print(f"   python spotify-bots.py --list-devices")
            print(f"\n⚠️  NOTE: This is an ACCESS TOKEN (expires in 1 hour)")
            print(f"   For long-term use, you need a REFRESH TOKEN")
            
            # Set temporary environment variable
            os.environ["SPOTIFY_REFRESH_TOKEN"] = "temp_access_token_" + ACCESS_TOKEN
            return True
        else:
            print(f"\n⚠️  Token works but no devices found.")
            print(f"   Make sure Spotify is open on a device!")
    
    return False

if __name__ == "__main__":
    run_quick_test()
