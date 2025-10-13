#!/usr/bin/env python3
"""
Quick authorization helper - generates the exact URL you need
"""

def main():
    print("🎵 Quick Spotify Authorization")
    print("=" * 50)
    
    # Direct URL to Spotify Console with your app ID
    console_url = "https://developer.spotify.com/console/get-available-devices/"
    
    print("📋 STEP 1: Go to Spotify Web API Console")
    print(f"URL: {console_url}")
    
    print("\n📋 STEP 2: On the console page:")
    print("   1. Click 'Get Token'")
    print("   2. Select these scopes:")
    print("      ✅ user-read-playback-state")
    print("      ✅ user-modify-playback-state") 
    print("      ✅ user-read-currently-playing")
    print("   3. Click 'Request Token'")
    print("   4. Log in and authorize")
    print("   5. Copy the OAuth Token that appears")
    
    print("\n📋 STEP 3: Make sure Spotify is ACTIVE on your iPhone")
    print("   - Open Spotify app")
    print("   - Play or pause a song (don't just close the app)")
    
    print("\n📋 STEP 4: Test the token")
    print("   - Paste the token in simple_bot.py")
    print("   - Run: python simple_bot.py")
    
    print(f"\n🌐 Opening console page...")
    import webbrowser
    try:
        webbrowser.open(console_url)
    except:
        print("❌ Could not open browser")

if __name__ == "__main__":
    main()
