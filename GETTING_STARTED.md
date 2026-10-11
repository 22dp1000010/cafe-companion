# Getting Started with Café Companion

## 5-Minute Quick Start (No Firebase)

Perfect for trying the chat and UI without cloud setup.

```bash
# 1. Navigate to backend
cd backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Get a free Gemini API key (2 minutes)
#    Visit: https://ai.google.dev
#    Click "Get API Key" → Create new API key
#    Copy it

# 4. Create .env and add your key
echo "GEMINI_API_KEY=your_key_here" > .env

# 5. Run the server
uvicorn app.main:app --reload

# 6. Open browser
#    Visit: http://localhost:8000
```

You can now:
- ✅ Chat with the Gemini-powered assistant
- ✅ Get menu recommendations
- ✅ Try placing orders (stored in memory)
- ⚠️ See "Firebase not configured" for wait time and matching

---

## 30-Minute Setup (With Firebase + Firestore)

Use this once you have a Google Cloud project.

### Step 1: Set Up Firebase
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Select your project (create one if needed)
- Enable these APIs:
  - Firestore
  - Firebase Cloud Messaging (FCM)

### Step 2: Create a Service Account
- Go to **Service Accounts** in Cloud Console
- Click "Create Service Account"
- Name it "cafe-companion"
- Grant it **Editor** role
- Create a JSON key and download it
- Move it to `backend/service-account.json`

### Step 3: Update .env
```bash
# In backend/.env, add:
FIREBASE_PROJECT_ID=your_project_id_here
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json
```

### Step 4: Seed Data (Optional)
```bash
cd backend
python -m app.seed_data
```

This creates:
- A sample menu (espresso, latte, cappuccino, etc.)
- Demo users (Alice, Bob, Carol) with interests
- Sample matches based on shared interests

### Step 5: Restart and Test
```bash
uvicorn app.main:app --reload
```

Now you can:
- ✅ Chat with recommendations powered by your Firestore order history
- ✅ See real-time wait-time estimates
- ✅ Opt-in to interest matching and see matches with other users

---

## Testing Without Running the Server

```bash
cd backend

# Run pure logic tests (no Firebase/API needed)
pytest

# Tests cover:
# - Wait time calculation
# - Interest tag overlap scoring
```

---

## Troubleshooting

### "Gemini not configured"
- Did you add `GEMINI_API_KEY` to `.env`?
- Did you restart the server after adding it?

### "Firebase not configured"
- Did you add `FIREBASE_PROJECT_ID` and point `GOOGLE_APPLICATION_CREDENTIALS` to your service account JSON?
- Is the JSON file in the right place (`backend/service-account.json`)?
- Did you restart the server?

### "Service account file not found"
- Check that `service-account.json` is in the `backend/` directory
- Run `ls backend/service-account.json` to confirm

### "permission denied" on seed_data
- Make sure your service account has **Editor** role in the Google Cloud project
- Firestore database must be created (Cloud Console → Firestore → Create Database)

---

## Next Steps

1. **Try the UI**: Open http://localhost:8000 and play with chat
2. **Test the API**: Use curl to hit endpoints
   ```bash
   curl http://localhost:8000/api/wait-time
   curl -X POST http://localhost:8000/api/chat \
     -H "Content-Type: application/json" \
     -d '{"user_id":"user_001","message":"I want a latte"}'
   ```
3. **Explore the code**: See [plan file](../.claude/plans/pasted-content-id-5e17-the-synthetic-falcon.md)
4. **Deploy later**: Follow README.md → "Deploying to Cloud Run"

---

## Project IDs and Credentials to Provide Later

When you're ready to deploy or wire in real Firebase:
- **Google Cloud Project ID**: (you'll provide this)
- **Firebase Service Account JSON**: (download from Cloud Console)
- **Gemini API Key**: (from https://ai.google.dev)

Until then, the app runs fine locally with just the Gemini key! 🚀
