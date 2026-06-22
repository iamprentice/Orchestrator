import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "ComplaintMiner/1.0")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output")
MAX_COMPLAINTS = int(os.getenv("MAX_COMPLAINTS", "10"))
MAX_OPPORTUNITIES = int(os.getenv("MAX_OPPORTUNITIES", "5"))

DEFAULT_MODEL = "claude-opus-4-8"

REDDIT_ENABLED = bool(REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET)
