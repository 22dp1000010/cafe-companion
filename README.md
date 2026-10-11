# ☕ Café Companion — AI-Powered Café Experience

A conversational AI agent that combines personalized ordering, wait-time prediction, and customer matching to create a smarter café experience.

## Features

### 1. **Conversational Ordering & Recommendations** 💬
- Chat with a Gemini-powered agent that remembers your preferences
- Get personalized menu recommendations based on your order history
- Natural language ordering with structured intent recognition
- Orders are validated against the real menu and saved to Firestore

### 2. **Wait Time Prediction** ⏱️
- Real-time queue-based wait-time estimates
- Heuristic algorithm: prep time of queued items ÷ available baristas
- Updates automatically as orders move through the queue

### 3. **Interest-Based Customer Matching** 💬
- Opt-in to share your interests (hiking, coding, photography, etc.)
- Automatic tag-overlap matching finds fellow café lovers with shared interests
- Matches scored by similarity and stored in Firestore
- Ready for FCM push notifications (wired but awaiting FCM config)

## Tech Stack

- **Backend**: Python + FastAPI
- **AI**: Google Gemini API (free tier via `google-generativeai` SDK)
- **Database**: Firebase Firestore
- **Notifications**: Firebase Cloud Messaging (FCM)
- **Frontend**: Vanilla HTML/CSS/JavaScript (no build tools)
- **Hosting**: Cloud Run (Dockerfile included)

## Quick Start

### Prerequisites

- Python 3.11+
- A Google account (for Gemini API key)
- A Google Cloud project with Firestore (optional for local testing)

### Installation

1. **Clone and navigate to the backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up environment variables** (copy from `.env.example` to `.env`):
   ```bash
   cp .env.example .env
   ```

3. **Add your Gemini API key** (required for chat):
   - Get a free Gemini API key at [https://ai.google.dev](https://ai.google.dev)
   - Add it to your `.env`:
     ```
     GEMINI_API_KEY=your_key_here
     ```

4. **Run the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Open in browser**: Navigate to `http://localhost:8000`

---

## Wiring in Firebase (Firestore + FCM)

Once you have a Google Cloud project:

1. **Generate a service account JSON**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/) → Your Project → Service Accounts
   - Create a new service account with **Editor** role
   - Download the JSON key and save as `service-account.json` in the `backend/` directory

2. **Update `.env`**:
   ```
   FIREBASE_PROJECT_ID=your_project_id
   GOOGLE_APPLICATION_CREDENTIALS=./service-account.json
   ```

3. **Seed sample data** (optional, creates a demo menu + users):
   ```bash
   python -m app.seed_data
   ```

4. **Restart the server** — Firestore endpoints will now work.

### Without Firebase
- The app runs fine without Firebase configured
- Chat still works (powered by Gemini alone)
- Firestore-dependent endpoints return HTTP 503 with a clear message
- Once you add credentials, they light up automatically

---

## API Endpoints

### Chat
**POST** `/api/chat`
```json
{
  "user_id": "user_001",
  "message": "I'd like a latte, please"
}
```
Response includes conversational reply, optional order intent, and recommendations.

### Wait Time
**GET** `/api/wait-time`

Returns estimated wait in minutes, current queue size, and available baristas.

### Interest Matching
**POST** `/api/interests`
```json
{
  "user_id": "user_001",
  "interests": ["hiking", "photography", "coding"]
}
```
Matches against other opted-in users and stores matches in Firestore.

**GET** `/api/matches/{user_id}`

Retrieves all matches for a user.

### Health Check
**GET** `/health`

Returns app status, Firebase configuration, and Gemini setup.

---

## Project Structure

```
backend/
  ├── app/
  │   ├── main.py              # FastAPI app entry point
  │   ├── config.py            # Environment settings
  │   ├── firebase.py          # Firestore + FCM client (lazy init)
  │   ├── gemini.py            # Gemini chat client
  │   ├── seed_data.py         # Script to populate Firestore
  │   ├── models/
  │   │   └── schemas.py       # Pydantic models
  │   └── routers/
  │       ├── chat.py          # Ordering + recommendations
  │       ├── wait_time.py     # Queue estimation
  │       └── matching.py      # Interest-based matching
  ├── requirements.txt
  └── .env.example
frontend/
  ├── index.html               # Single-page app UI
  ├── app.js                   # Chat logic + API calls
  └── styles.css               # Styling (coffee-themed)
Dockerfile                     # Cloud Run packaging
README.md                       # This file
.gitignore
```

---

## Demo Data

When you run `python -m app.seed_data`, the following is created:

- **Menu**: 12 items (espresso, latte, cappuccino, cold brew, matcha latte, chai latte, pastries, sandwich)
- **Demo Users**:
  - Alice Johnson (prefers lattes, interested in reading/photography/hiking)
  - Bob Smith (prefers espresso, interested in hiking/coding/music)
  - Carol Davis (prefers tea, interested in yoga/photography/cooking)

Alice and Carol match on "photography", Alice and Bob match on "hiking".

---

## Testing

### Pure logic (no Firebase/Gemini needed)
```bash
pytest  # Tests wait-time formula and interest tag-overlap scoring
```

### Manual testing
1. Start the server: `uvicorn app.main:app --reload`
2. Open `http://localhost:8000` in a browser
3. Test chat, wait time, and interest matching
4. Try switching user IDs to see different order history and matches

### With Firebase
1. Add credentials (service account JSON + project ID)
2. Run `python -m app.seed_data` to populate Firestore
3. Test endpoints via the UI or curl:
   ```bash
   curl http://localhost:8000/api/wait-time
   ```

---

## Deploying to Cloud Run

Once you have a Google Cloud project with credentials:

1. **Authenticate**:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Build and push** (Cloud Build handles it):
   ```bash
   gcloud run deploy cafe-companion \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

3. **Set environment variables** in the Cloud Run service:
   - `GEMINI_API_KEY`
   - `FIREBASE_PROJECT_ID`
   - `GOOGLE_APPLICATION_CREDENTIALS` (Cloud Run uses service account automatically)

4. Your app will be live at `https://cafe-companion-<random>.a.run.app`

---

## Future Enhancements

- **FCM Notifications**: Wire up Firebase Cloud Messaging to push notifications when matches are found
- **User Profiles**: Add a user management UI (profile editor, order history viewer)
- **Menu Analytics**: Track popular items and seasonal trends
- **Advanced Matching**: Use embeddings (Vertex AI) for semantic interest matching
- **Mobile App**: Native iOS/Android via React Native

---

## Support

For issues, feature requests, or questions:
1. Check the `/health` endpoint to verify all services are configured
2. Review `.env` settings and Firestore permissions
3. Ensure your Gemini API key has quota available

---

**Built for the Café Companion challenge with ❤️ and lots of ☕**
