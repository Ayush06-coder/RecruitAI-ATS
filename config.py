import os
from dotenv import load_dotenv

load_dotenv()

# FastAPI always runs on port 8000 (locally and on Render internally)
# Do NOT set API_URL to your public Render URL — set it to http://localhost:8000
API_URL = os.getenv("API_URL", "http://localhost:8000")