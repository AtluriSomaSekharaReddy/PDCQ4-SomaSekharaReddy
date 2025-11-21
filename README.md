# Google OAuth Login with Flask

A fully functional Flask web application that implements **Google Sign-In using OAuth 2.0**.

After successful login, it displays:
- Your full name
- Your email address
- Your Google profile picture
- Current **India Standard Time (IST)**
- A working **Sign out** link

Works perfectly on **all browsers** (Chrome, Firefox, Edge, Safari, Mobile)


### Final Output (After Login)

Hello USER [Sign out]
You are signed in with the email user@example.comm
[Your Google Profile Picture]
Current India Time: 21 November 2025, 11:59:59 PM IST
Sign out


---

### Features
- Official Google OAuth 2.0 authentication
- Clean, modern, responsive UI
- Real-time India timezone clock (Asia/Kolkata)
- Secure session management
- Full Sign Out functionality
- Profile picture with fallback for testing/demo

---

#### 1. Clone the repository

git clone https://github.com/AtluriSomaSekharaReddy/PDCQ4-SomaSekharaReddy.git
cd PDCQ4-SomaSekharaReddy
cd google-login-flask


#### 2. Install dependencies

pip install -r requirements.txt


#### 3. Setup Google OAuth Credentials (One-Time)
1. Go to → https://console.cloud.google.com/
2. Create a new project (or use existing)
3. Go to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **OAuth client ID** → **Web application**
5. Under **Authorized redirect URIs**, add:
   
   http://localhost:5000/callback
   
6. Click **Create** → **Download JSON**
7. Rename the file to `credentials.json`
8. Place it in the project root (same folder as `app.py`)

**Note**: `credentials.json` is **never uploaded** to GitHub (blocked by via `.gitignore`)

#### 4. Run the app
python app.py

#### 5. Open in browser
Visit: http://localhost:5000

Click **"Sign in with Google"** → Login → Done!

---

### Project Structure

PDCQ4-SomaSekharaReddy/google-login-flask
├── app.py                  Main Flask application
├── requirements.txt        Python dependencies
├── credentials.example.json Safe template
├── templates/
│   └── home.html           Success page with profile & time
├── .gitignore              Blocks real credentials
└── README.md               This file


**Submitted by**: Atluri Soma Sekhara Reddy  

Thank you!
