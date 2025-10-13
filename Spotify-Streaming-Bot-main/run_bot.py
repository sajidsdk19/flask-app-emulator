#!/usr/bin/env python3
"""
Quick runner for the Spotify bot using your access token
"""
import os
import subprocess
import sys

# Your access token
ACCESS_TOKEN = "BQBzoGq3gNGBmTi0dcBa4Fe7dNnxuyrxU6yQTYyLBFP_wDfUX4oh2oTf2m6F8ONrgkCKXOXsMVO0Q_GofMsVoaz4wGjPV0DCC_JRCP3riNPRx-o6GfvlLZq2yiG51Z-NK4aKTRHpVpwZy6PviOM1qZKily16TRi2mACSDKdAnxYWrHTaIoO-sfci4v02cFtjplOUwGbTQu6bZ64vVkC5aHCP2bLWzelWhFsiUQH4csn3DA9_Fm10PRRDCsc65WJH7m180FsPd4Z-x3RCU7ywDVhYP-6fnxJPbbS8FWvLl3BtljrWFn1U22t6g-GagqqNA90F"

def setup_environment():
    """Set up environment variables"""
    os.environ["SPOTIFY_CLIENT_ID"] = "479b522c097b419cb15a02a04956d5f9"
    os.environ["SPOTIFY_CLIENT_SECRET"] = "85aab30221f84db785c5c83c10119ded"
    # Use access token as refresh token temporarily (will need refresh for long-term use)
    os.environ["SPOTIFY_REFRESH_TOKEN"] = ACCESS_TOKEN
    print("✅ Environment variables set")

def list_devices():
    """List available Spotify devices"""
    print("🔍 Listing available devices...")
    try:
        result = subprocess.run([
            sys.executable, "spotify-bots.py", "--list-devices"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("📱 Available devices:")
            print(result.stdout)
        else:
            print(f"❌ Error listing devices: {result.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_bot_session():
    """Run a test session"""
    print("\n🎵 Starting bot session...")
    print("Options:")
    print("1. List devices first")
    print("2. Run with a playlist (need device ID)")
    print("3. Run with specific tracks")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    if choice == "1":
        list_devices()
    elif choice == "2":
        device_id = input("Enter device ID: ").strip()
        playlist_uri = input("Enter playlist URI (or press Enter for default): ").strip()
        if not playlist_uri:
            playlist_uri = "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M"  # Today's Top Hits
        
        duration = input("Duration in seconds (default 300): ").strip()
        if not duration:
            duration = "300"
        
        cmd = [
            sys.executable, "spotify-bots.py",
            "--device-id", device_id,
            "--context-uri", playlist_uri,
            "--duration", duration,
            "--shuffle", "on"
        ]
        
        print(f"🚀 Running: {' '.join(cmd)}")
        subprocess.run(cmd)
    
    elif choice == "3":
        track_uris = input("Enter track URIs (comma-separated): ").strip()
        duration = input("Duration in seconds (default 180): ").strip()
        if not duration:
            duration = "180"
        
        cmd = [
            sys.executable, "spotify-bots.py",
            "--uris", track_uris,
            "--duration", duration
        ]
        
        print(f"🚀 Running: {' '.join(cmd)}")
        subprocess.run(cmd)

if __name__ == "__main__":
    print("🎵 Spotify Bot Runner")
    print("=" * 50)
    
    setup_environment()
    run_bot_session()
