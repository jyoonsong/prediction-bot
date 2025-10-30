import os
from openai import OpenAI
import dotenv

dotenv.load_dotenv()

# -----------------------------------------------------------------------------
# Global Configuration
# -----------------------------------------------------------------------------

MODEL_NAME = "gpt-5-nano-2025-08-07"
NUM_QUERIES = 6
NUM_URLS = 5
MAX_QUERY_WORDS = 7

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")

# Clients
client = OpenAI(organization=OPENAI_ORG_ID, api_key=OPENAI_API_KEY)
