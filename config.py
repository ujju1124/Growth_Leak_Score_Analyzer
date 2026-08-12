"""Configuration management for the Growth Leak Score Analyzer."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Groq API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

# Validate configuration
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in environment variables. "
        "Please create a .env file with your Groq API key."
    )
