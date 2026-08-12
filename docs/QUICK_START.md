# 🚀 Quick Start - Growth Leak Score Analyzer

## Get Running in 3 Minutes

### Step 1: Install (30 seconds)
```bash
pip install -r requirements.txt
```

### Step 2: Configure (1 minute)
1. Get free API key: [console.groq.com](https://console.groq.com)
2. Edit `.env` file:
```bash
GROQ_API_KEY=gsk_your_actual_key_here
```

### Step 3: Run (30 seconds)
```bash
streamlit run app.py
```

**That's it!** Your browser will open automatically. 🎉

---

## Test Everything Works

```bash
python test_integration.py
```

Should show: ✅ All integration tests passed!

---

## File Overview

| File | Purpose | When to Edit |
|------|---------|--------------|
| `app.py` | UI/Interface | Customize look & feel |
| `scraper.py` | Website extraction | Add detection patterns |
| `scorer.py` | LLM analysis | Adjust prompts |
| `rubric.py` | Scoring categories | Change point values |
| `config.py` | Settings | Change model name |
| `.env` | Your API key | Add your key here! |

---

## What It Does

1. **Input:** Company URL + 6 questions
2. **Scrapes:** Homepage for marketing signals
3. **Analyzes:** Sends to Groq AI with rubric
4. **Scores:** 8 categories, identifies biggest leak
5. **Recommends:** Specific action to fix the leak

**Total time:** 10-15 seconds per analysis

---

## Troubleshooting

### Error: "GROQ_API_KEY not found"
➜ Edit `.env` and add your key (no quotes needed)

### Error: "ModuleNotFoundError"
➜ Run `pip install -r requirements.txt` again

### Website scraping fails
➜ Normal! App will still work with questionnaire only

### "Connection timeout"
➜ Check internet connection, some sites block scrapers

---

## Example Input/Output

**Input:**
- URL: `https://www.yourcompany.com`
- Industry: B2B SaaS
- Customer Value: $5,000
- Main Channel: LinkedIn Ads

**Output:**
```
Score: 65/100 ⚠️

Biggest Leak: Trust & Social Proof (40%)

Recommendation: Add 3-4 customer testimonials with 
specific results above the fold. Include company 
logos and quantified outcomes to build credibility.
```

---

## Ready for More?

- **Full Setup Guide:** See `SETUP_GUIDE.md`
- **Usage Examples:** See `USAGE_EXAMPLES.md`
- **Project Details:** See `PROJECT_SUMMARY.md`
- **Main Docs:** See `README.md`

---

**Now go analyze some businesses! 🎯**

```bash
streamlit run app.py
```
