# Growth Leak Score Analyzer - Setup Guide

## Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `groq` - Official Groq API SDK for LLM calls
- `streamlit` - Web UI framework
- `requests` + `beautifulsoup4` - Web scraping
- `pydantic` - Data validation
- `python-dotenv` - Environment configuration

### Step 2: Get Your Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy your API key

### Step 3: Configure Your API Key

Edit the `.env` file in the project root and replace `your_groq_api_key_here` with your actual key:

```bash
GROQ_API_KEY=gsk_your_actual_api_key_here
```

## Running the Application

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## Testing Individual Components

### Test the Scraper (no API key needed)

```bash
python scraper.py
```

This will test scraping against 3 real websites and show what data is extracted.

### Test the Scorer (requires API key)

```bash
python scorer.py
```

This will run a full analysis with sample data to verify Groq API integration.

## Troubleshooting

### "GROQ_API_KEY not found"
- Make sure you created a `.env` file (not `.env.example`)
- Ensure the key is on the line: `GROQ_API_KEY=your_key`
- No quotes needed around the key value

### "ModuleNotFoundError"
- Run `pip install -r requirements.txt` again
- Verify you're using Python 3.11 or higher: `python --version`

### "Connection timeout" when scraping
- Check your internet connection
- Some websites may block scrapers - this is expected
- The app will gracefully degrade and score based on questionnaire only

### Groq API errors
- Verify your API key is valid at console.groq.com
- Check if you have remaining API credits (free tier available)
- The model name is `llama-3.3-70b-versatile` - if this changes, update `config.py`

## Project Structure

```
project/
├── app.py              # Main Streamlit UI - run this
├── scraper.py          # Web scraping logic
├── scorer.py           # Groq LLM analysis
├── rubric.py           # Scoring rubric (8 categories)
├── models.py           # Pydantic validation models
├── config.py           # Loads .env variables
├── requirements.txt    # Dependencies
├── .env               # Your API key (YOU MUST CREATE THIS)
├── .env.example       # Template for .env
└── README.md          # Project documentation
```

## How It Works

1. **User Input**: Company website URL + 5-6 business questions
2. **Scraping**: `scraper.py` extracts title, content, marketing signals (forms, chat, tracking pixels, etc.)
3. **Analysis**: `scorer.py` sends data to Groq LLM with structured scoring rubric
4. **Scoring**: LLM returns JSON with 8 category scores + reasoning
5. **Calculation**: App recomputes total score and identifies biggest leak
6. **Recommendation**: Second LLM call generates specific action plan
7. **Display**: Beautiful Streamlit UI shows results with color-coded scores

## Key Features

✅ **Graceful Degradation**: Works even if website scraping fails
✅ **Structured Output**: Uses Groq's JSON mode for reliable parsing
✅ **No Database**: Everything runs in-memory (single session)
✅ **Fast**: Total analysis takes 10-15 seconds
✅ **Production-Ready**: Error handling, retries, validation

## Next Steps After Setup

1. Test with your own business website
2. Customize the rubric in `rubric.py` if needed
3. Adjust scoring prompts in `scorer.py`
4. Style the Streamlit UI in `app.py`
5. Deploy to Streamlit Cloud for public access (optional)

## Support

- Groq Documentation: [console.groq.com/docs](https://console.groq.com/docs)
- Streamlit Documentation: [docs.streamlit.io](https://docs.streamlit.io)
- Issues: Open a GitHub issue

---

**Ready to analyze some businesses? Run `streamlit run app.py` and go! 🚀**
