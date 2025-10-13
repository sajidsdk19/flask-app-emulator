"""
Test Spotify API access
"""
import os
from dotenv import load_dotenv
from spotify_api import get_available_devices, get_current_playback

# Load environment variables
load_dotenv()

# Get access token from environment
TOKEN = os.getenv('SPOTIFY_ACCESS_TOKEN')

if not TOKEN:
    print("❌ Error: No access token found. Please set SPOTIFY_ACCESS_TOKEN in .env")
    exit(1)

print("🔍 Testing Spotify API access...")

# Test getting available devices
print("\n📱 Checking available devices...")
devices = get_available_devices(TOKEN)
if devices and 'devices' in devices:
    print(f"✅ Found {len(devices['devices'])} device(s):")
    for i, device in enumerate(devices['devices'], 1):
        print(f"{i}. {device['name']} ({device['type']}) - {'Active' if device['is_active'] else 'Inactive'}")
else:
    print("❌ Could not retrieve devices. The token might be invalid or lack permissions.")

# Test getting current playback
print("\n🎵 Checking current playback...")
playback = get_current_playback(TOKEN)
if playback and 'item' in playback:
    track = playback['item']
    print(f"✅ Now playing: {track['name']} by {', '.join(a['name'] for a in track['artists'])}")
    print(f"   On: {playback['device']['name']} ({playback['device']['type']})")
else:
    print("❌ No active playback or couldn't retrieve playback info.")
    print("   Make sure Spotify is playing on one of your devices.")
