"""
Spotify Web API wrapper
"""
import json
import requests
from typing import Optional, Dict, Any

def fetch_web_api(token: str, endpoint: str, method: str = 'GET', body: Optional[Dict] = None) -> Optional[Dict]:
    """
    Make an authenticated request to the Spotify Web API
    
    Args:
        token: Spotify access token
        endpoint: API endpoint (e.g., 'v1/me/player/devices')
        method: HTTP method (GET, POST, PUT, DELETE)
        body: Request body for POST/PUT requests
        
    Returns:
        dict: JSON response from the API or None if request failed
    """
    url = f"https://api.spotify.com/{endpoint}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=body)
        elif method.upper() == 'PUT':
            response = requests.put(url, headers=headers, json=body)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            print(f"❌ Unsupported HTTP method: {method}")
            return None
            
        response.raise_for_status()
        return response.json() if response.text else {}
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        if hasattr(e, 'response') and e.response.text:
            print(f"Error details: {e.response.text}")
        return None

def get_available_devices(token: str) -> Optional[Dict]:
    """Get list of available Spotify devices"""
    return fetch_web_api(token, 'v1/me/player/devices')

def get_current_playback(token: str) -> Optional[Dict]:
    """Get information about current playback"""
    return fetch_web_api(token, 'v1/me/player')

def start_playback(token: str, device_id: str = None, context_uri: str = None, uris: list = None) -> bool:
    """Start or resume playback"""
    data = {}
    if context_uri:
        data['context_uri'] = context_uri
    if uris:
        data['uris'] = uris
    
    endpoint = 'v1/me/player/play'
    if device_id:
        endpoint += f'?device_id={device_id}'
    
    result = fetch_web_api(token, endpoint, 'PUT', data if data else None)
    return result is not None

def pause_playback(token: str, device_id: str = None) -> bool:
    """Pause playback"""
    endpoint = 'v1/me/player/pause'
    if device_id:
        endpoint += f'?device_id={device_id}'
    result = fetch_web_api(token, endpoint, 'PUT')
    return result is not None
