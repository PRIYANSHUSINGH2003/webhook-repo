# webhook-repo

This repository contains a Flask app that receives GitHub webhook events, stores them in MongoDB, and serves a modern UI that polls for updates every 15 seconds.

## Setup

1. Clone this repository.
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your MongoDB URI:
   ```
   cp .env.example .env
   # Edit .env and set MONGO_URI
   ```
5. Run the Flask app:
   ```
   python app.py
   ```
6. Open [http://localhost:5000](http://localhost:5000) in your browser to view the UI.

## Webhook Endpoint
- POST events to `/webhook` in the following JSON format:
  ```json
  {
    "request_id": "<commit_hash_or_pr_id>",
    "author": "<author_name>",
    "action": "PUSH" | "PULL_REQUEST" | "MERGE",
    "from_branch": "<from_branch>",
    "to_branch": "<to_branch>",
    "timestamp": "<datetime string>"  // optional, will be set automatically if omitted
  }
  ```

## UI
- The UI polls the backend every 15 seconds and displays the latest events in a modern, responsive layout.

---
