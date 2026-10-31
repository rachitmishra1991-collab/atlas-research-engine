# PROJECT ATLAS — Research Engine Starter

This is the first working dashboard foundation for ATLAS Mission 001.

## What this version does
- Creates a research mission specification.
- Shows a session-based mission queue.
- Displays 10 specialist departments (100 logical specialist roles).
- Provides an editable register of 20 candidate businesses.
- Exports the candidate register to CSV.

## Important limitation
This starter does **not** perform live web research, call an AI model, or verify market facts yet. It deliberately labels research as pending instead of pretending the work is complete. The next implementation step is to connect a web-search provider and an AI model using protected secrets.

## Run locally (computer)
1. Install Python 3.11 or newer.
2. Extract this ZIP.
3. Open a terminal in the extracted `atlas_research_engine` folder.
4. Run:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
5. Open the local URL printed in the terminal.

## Deploy online (recommended for Android access)
1. Create/sign in to a GitHub account.
2. Create a new repository named `atlas-research-engine`.
3. Upload `app.py` and `requirements.txt` from this folder to the repository root.
4. Visit https://share.streamlit.io and sign in with GitHub.
5. Choose **Create app**, select the repository, branch `main`, and file `app.py`.
6. Deploy. Streamlit will provide a `*.streamlit.app` web address.

Official guide: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app

## Security
- Never paste API keys into `app.py` or commit them to GitHub.
- When API integrations are added, enter credentials using Streamlit's app Secrets settings.
- Do not upload confidential customer or employer data to the public starter app.
