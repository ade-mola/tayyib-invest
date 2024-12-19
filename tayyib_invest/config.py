import os

from dotenv import load_dotenv


load_dotenv()
FMP_API_KEY = os.getenv("FMP_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
