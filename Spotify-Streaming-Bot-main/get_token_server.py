"""
Simple HTTP server to handle Spotify OAuth callback
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
from urllib.parse import parse_qs
import webbrowser
import threading
import json

# Your Spotify App Credentials
CLIENT_ID = "479b522c097b419cb15a02a04956d5f9"
REDIRECT_URI = "http://localhost:8888/callback"

# Required scopes
SCOPES = [
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing',
    'streaming',
    'app-remote-control'
]

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL and query parameters
        parsed_url = urlparse.urlparse(self.path)
        query_params = parse_qs(parsed_url.fragment)  # Use fragment for implicit grant
        
        # Check if we have an access token in the callback
        if 'access_token' in query_params:
            access_token = query_params['access_token'][0]
            token_type = query_params.get('token_type', ['Bearer'])[0]
            expires_in = query_params.get('expires_in', [3600])[0]
            
            # Send response to the browser
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Create a simple response page
            response = f"""
            <html>
                <body>
                    <h2>Authentication Successful!</h2>
                    <p>You can now close this window and return to the terminal.</p>
                    <script>
                        // Close the window after 3 seconds
                        setTimeout(window.close, 3000);
                    </script>
                </body>
            </html>
            """
            self.wfile.write(response.encode())
            
            # Print the token information
            print("\n✅ Successfully obtained access token!")
            print("\nHere's your access token (copy this to simple_bot.py):")
            print("-" * 50)
            print(access_token)
            print("-" * 50)
            print("\nThis token will expire in", expires_in, "seconds.")
            
            # Stop the server
            threading.Thread(target=self.server.shutdown, daemon=True).start()
        else:
            # If no token in the URL, show an error
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Error: No access token found in the callback URL')

def start_auth_flow():
    # Start the web server in a separate thread
    server = HTTPServer(('localhost', 8888), CallbackHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Generate the authorization URL
    auth_url = (
        f"https://accounts.spotify.com/authorize?"
        f"client_id={CLIENT_ID}&"
        f"response_type=token&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope={'%20'.join(SCOPES)}&"
        "show_dialog=true"
    )
    
    print("🔗 Opening Spotify authorization in your browser...")
    print("Please log in with your Spotify account and grant the requested permissions.")
    print("\nIf the browser doesn't open automatically, visit this URL:")
    print("-" * 50)
    print(auth_url)
    print("-" * 50)
    
    # Open the authorization URL in the default web browser
    webbrowser.open(auth_url)
    
    # Wait for the server to be stopped by the callback
    server_thread.join()
    print("\n✅ Done! You can now use the access token in simple_bot.py")

if __name__ == "__main__":
    print("🚀 Starting Spotify OAuth flow...")
    start_auth_flow()
