from flask import Flask, redirect, url_for, session, render_template, request
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
import requests
import os
import pytz
from datetime import datetime

app = Flask(__name__)
app.secret_key = '8hX9m!pL2$kQ5@zR7v_3nJ1eW4rT9yU6iO0pA5sD3fG8hJ2kL6mN1bV4cX7zR5tY'  # Change this!

# Google OAuth Config
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# Load credentials
flow = Flow.from_client_secrets_file(
    'credentials.json',
    scopes=SCOPES,
    redirect_uri='http://localhost:5000/callback'
)

def get_india_time():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    return now.strftime("%d %B %Y, %I:%M:%S %p IST")

def generate_diamond(n):
    text = "FORMULAQSOLUTIONS"
    length = len(text)

    # Make height odd to match the example patterns
    height = n if n % 2 != 0 else n + 1
    mid = height // 2

    def char_at(idx):
        return text[idx % length]

    result = []

    for i in range(height):
        spaces = abs(mid - i)
        width = height - 2 * spaces
        line = " " * spaces  # preserve exact indentation

        # Top/bottom row: single letter
        if i == 0 or i == height - 1:
            line += char_at(i).upper()
        # Odd rows: letters at edges with dashes
        elif i % 2 == 1:
            line += char_at(i).upper()
            if width > 1:
                line += "-" * (width - 2)
                line += char_at(i + width - 1).upper()
        # Even rows: consecutive letters
        else:
            for j in range(width):
                line += char_at(i + j).upper()

        result.append(line)

    return "\n".join(result)

@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'google_user' not in session:
        return '''
        <h1 style="text-align:center; margin-top:100px; font-family:Arial">
            Welcome! Please sign in
        </h1>
        <div style="text-align:center; margin-top:30px;">
            <a href="/login">
                <button style="padding:15px 30px; font-size:18px; background:#4285F4; color:white; border:none; border-radius:5px; cursor:pointer;">
                    <img src="https://developers.google.com/identity/images/g-logo.png" width="20" height="20" style="vertical-align:middle; margin-right:10px;">
                    Sign in with Google
                </button>
            </a>
        </div>
        '''

    user = session['google_user']
    design = None
    lines = None

    if request.method == 'POST':
        try:
            lines = int(request.form['lines'])
            if 1 <= lines <= 100:
                design = generate_diamond(lines)
            else:
                design = "Please enter a number between 1 and 100"
        except:
            design = "Invalid input!"

    return render_template('home.html',
                           name=user['name'],
                           email=user['email'],
                           picture=user.get('picture'),
                           india_time=get_india_time(),
                           design=design,
                           lines=lines)

@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='select_account'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session.get('state') or session['state'] != request.args.get('state'):
        return "State mismatch!", 400

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        credentials.id_token,
        token_request,
        flow.client_config['client_id']
    )

    session['google_user'] = {
        'name': id_info.get('name'),
        'email': id_info.get('email'),
        'picture': id_info.get('picture')
    }
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)