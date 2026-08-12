"""Configuration management for the Growth Leak Score Analyzer."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try to get API key from environment first, then Streamlit secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# If not in environment, try Streamlit secrets
if not GROQ_API_KEY:
    try:
        import streamlit as st
        GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
    except:
        pass

GROQ_MODEL = "llama-3.3-70b-versatile"

# Validate configuration
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. "
        "Please add it to .env file (local) or Streamlit secrets (cloud)."
    )
