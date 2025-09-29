const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 8888;

// YOUR CREDENTIALS
const CLIENT_ID = '479b522c097b419cb15a02a04956d5f9';
const CLIENT_SECRET = 'YOUR_CLIENT_SECRET_HERE'; // Add your client secret
const REDIRECT_URI = `http://localhost:${PORT}/callback`;

// Scopes - add or remove based on what you need
const SCOPES = [
  'user-read-private',
  'user-read-email',
  'playlist-read-private',
  'user-top-read',
  'user-read-recently-played',
  'user-library-read'
].join('%20');

// Step 1: Start authorization
app.get('/login', (req, res) => {
  const authURL = `https://accounts.spotify.com/authorize?client_id=${CLIENT_ID}&response_type=code&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&scope=${SCOPES}`;
  res.redirect(authURL);
});

// Step 2: Handle callback and get refresh token
app.get('/callback', async (req, res) => {
  const code = req.query.code;

  if (!code) {
    return res.send('Error: No authorization code received');
  }

  try {
    const response = await axios.post(
      'https://accounts.spotify.com/api/token',
      new URLSearchParams({
        grant_type: 'authorization_code',
        code: code,
        redirect_uri: REDIRECT_URI,
        client_id: CLIENT_ID,
        client_secret: CLIENT_SECRET
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    );

    const { access_token, refresh_token } = response.data;

    res.send(`
      <html>
        <body style="font-family: Arial; padding: 40px; background: #1DB954; color: white;">
          <h1>✅ Success!</h1>
          <h2>Your Refresh Token:</h2>
          <p style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; word-break: break-all; font-family: monospace;">
            ${refresh_token}
          </p>
          <h3>Add this to your .env file:</h3>
          <pre style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px;">
SPOTIFY_CLIENT_ID=${CLIENT_ID}
SPOTIFY_CLIENT_SECRET=${CLIENT_SECRET}
SPOTIFY_REFRESH_TOKEN=${refresh_token}
          </pre>
          <p>You can close this window now.</p>
        </body>
      </html>
    `);

    console.log('\n=================================');
    console.log('SPOTIFY_REFRESH_TOKEN=' + refresh_token);
    console.log('=================================\n');

  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
    res.send('Error getting token. Check console for details.');
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`\n🎵 Spotify Token Generator`);
  console.log(`\n1. Make sure you added this Redirect URI in your Spotify Dashboard:`);
  console.log(`   ${REDIRECT_URI}`);
  console.log(`\n2. Open this URL in your browser:`);
  console.log(`   http://localhost:${PORT}/login`);
  console.log(`\n3. Log in and authorize the app`);
  console.log(`\n4. Your refresh token will be displayed!\n`);
});