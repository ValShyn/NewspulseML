import os
from dotenv import load_dotenv


load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./news_data.db")

if not NEWS_API_KEY:
    raise ValueError("Cannot find api key")
