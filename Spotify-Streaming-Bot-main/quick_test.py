#!/usr/bin/env python3
"""
Quick test to check Spotify API connection
"""
import requests

# Your access token
ACCESS_TOKEN = "BQBzoGq3gNGBmTi0dcBa4Fe7dNnxuyrxU6yQTYyLBFP_wDfUX4oh2oTf2m6F8ONrgkCKXOXsMVO0Q_GofMsVoaz4wGjPV0DCC_JRCP3riNPRx-o6GfvlLZq2yiG51Z-NK4aKTRHpVpwZy6PviOM1qZKily16TRi2mACSDKdAnxYWrHTaIoO-sfci4v02cFtjplOUwGbTQu6bZ64vVkC5aHCP2bLWzelWhFsiUQH4csn3DA9_Fm10PRRDCsc65WJH7m180FsPd4Z-x3RCU7ywDVhYP-6fnxJPbbS8FWvLl3BtljrWFn1U22t6g-GagqqNA90F"

def test_token():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    print("🧪 Testing Spotify API connection...")
    
    try:
        # Test user profile
        response = requests.get("https://api.spotify.com/v1/me", headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS! Connected as: {data.get('display_name', 'Unknown')}")
            print(f"📧 Email: {data.get('email', 'N/A')}")
            print(f"🎵 Product: {data.get('product', 'N/A')}")
            
            # Test devices
            device_response = requests.get("https://api.spotify.com/v1/me/player/devices", headers=headers, timeout=10)
            if device_response.status_code == 200:
                devices = device_response.json().get("devices", [])
                print(f"\n📱 Found {len(devices)} device(s):")
                for device in devices:
                    status = "🟢 ACTIVE" if device['is_active'] else "⚪ INACTIVE"
                    print(f"  - {device['name']} ({device['type']}) - {status}")
            else:
                print(f"⚠️  Devices check failed: {device_response.status_code}")
                
        elif response.status_code == 401:
            print("❌ Token expired or invalid. Need a new access token.")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_token()
