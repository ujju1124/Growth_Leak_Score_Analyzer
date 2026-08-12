# Growth Leak Score Analyzer - Usage Examples

## Example Analysis Flow

### Input Example

**Website URL:**
```
https://www.yourcompany.com
```

**Questionnaire Answers:**
- **Industry:** B2B SaaS
- **Average Customer Value:** $5,000
- **Main Marketing Channel:** LinkedIn Ads
- **Monthly Traffic:** 2,000 visitors/month
- **Conversion Rate:** 1.5%
- **Biggest Challenge:** Not getting enough qualified leads

### Expected Output

#### Overall Score
```
65/100 ⚠️ Room for Improvement
```

#### Category Breakdown

1. **Value Proposition Clarity: 12/15 (80%)**
   - "Homepage clearly states target audience (B2B companies) and core benefit (automation), but the specific outcome could be more quantified."

2. **Call-to-Action Strength: 10/15 (67%)**
   - "Primary CTA exists ('Book a Demo') but competes with secondary CTAs for attention. Button could be more prominent."

3. **Lead Capture Mechanism: 8/15 (53%)**
   - "Contact form present but no live chat. Phone number buried in footer. Missing multiple capture points."

4. **Trust & Social Proof: 4/10 (40%)**
   - "No testimonials or case studies visible on homepage. Missing social proof elements that build credibility."

5. **SEO & Content Basics: 7/10 (70%)**
   - "Meta description exists but generic. Blog section present but no recent posts visible."

6. **Tracking & Follow-up Readiness: 8/10 (80%)**
   - "Google Analytics detected but no retargeting pixels found. Missing ability to follow up with anonymous visitors."

7. **Marketing Channel Effectiveness: 7/12 (58%)**
   - "Single channel dependence (LinkedIn Ads) creates risk. No clear diversification strategy mentioned."

8. **Conversion Health: 9/13 (69%)**
   - "1.5% conversion rate is below industry average (2-5% for B2B SaaS). Customer value is solid but funnel optimization needed."

#### Biggest Growth Leak
```
🚨 Trust & Social Proof (40%)
Missing testimonials or case studies visible on homepage. No social proof elements that build credibility.
```

#### Recommendation
```
💡 Add a testimonial section above the fold with 3-4 specific customer success stories, 
including company logos and quantified results (e.g., "Reduced processing time by 60%"). 
Consider adding a rotating customer quote widget and link to a dedicated case studies page. 
This immediately builds credibility with first-time visitors and can boost conversion rates by 20-30%.
```

---

## Command-Line Testing Examples

### Test the Scraper Only

```bash
python scraper.py
```

**Output:**
```
============================================================
Testing: https://www.example.com
============================================================
✅ Success!
Title: Example Domain
Meta: ...
Body preview: Example Domain This domain is for use...
Signals:
  Contact Form: False
  Pricing: False
  Live Chat: False
  Tracking: False
  Testimonials: False
  Blog: False
```

### Test the Full Scorer (Requires API Key)

```bash
python scorer.py
```

**Output:**
```
Testing scorer with sample data...

✅ Total Score: 67.5/100

📊 Category Breakdown:
  Value Proposition Clarity: 12.0/15 - Clear headline but could be more specific
  Call-to-Action Strength: 11.5/15 - Primary CTA visible but not prominent
  ...

🚨 Biggest Leak: Trust & Social Proof

💡 Recommendation: Add customer testimonials with specific results...
```

### Run Integration Tests

```bash
python test_integration.py
```

**Output:**
```
🧪 Testing Growth Leak Score Analyzer Integration...

1️⃣ Testing imports...
   ✅ All modules imported successfully

2️⃣ Testing rubric...
   ✅ Rubric sums to 100 points

3️⃣ Testing scraper...
   ✅ Scraped successfully

4️⃣ Testing configuration...
   ✅ API key loaded

5️⃣ Testing data models...
   ✅ Pydantic models working correctly

✅ All integration tests passed!
```

---

## Streamlit App Usage

### Starting the App

```bash
streamlit run app.py
```

### UI Walkthrough

1. **Homepage loads** - Shows title and description
2. **Enter URL** - Paste target company website
3. **Fill questionnaire** - 6 quick questions about the business
4. **Click "Analyze My Business"** - Shows spinner for 10-15 seconds
5. **Results page** - See:
   - Large colored score (red/yellow/green)
   - Expandable category breakdown
   - Highlighted biggest leak
   - Specific recommendation
6. **Click "Analyze Another Business"** - Reset and start over

### Browser Access

After starting the app, it opens automatically at:
```
http://localhost:8501
```

If it doesn't open automatically, copy that URL into your browser.

---

## Customization Examples

### Change the Scoring Model

Edit `config.py`:

```python
GROQ_MODEL = "mixtral-8x7b-32768"  # Faster, lower cost
# or
GROQ_MODEL = "llama-3.3-70b-versatile"  # Default, best quality
```

### Modify Rubric Categories

Edit `rubric.py`:

```python
RUBRIC = [
    {
        "name": "Value Proposition Clarity",
        "max_score": 20,  # Changed from 15
        "description": "Updated description..."
    },
    # ... adjust other categories so total = 100
]
```

### Adjust Scraping Timeout

Edit `scraper.py`:

```python
response = requests.get(url, headers=headers, timeout=20)  # Changed from 10
```

### Customize UI Colors

Edit `app.py`:

```python
def get_score_color(score: float) -> str:
    if score < 50:  # Changed thresholds
        return "#cc0000"  # Darker red
    elif score < 75:
        return "#ff8800"  # More orange
    else:
        return "#00cc00"  # Darker green
```

---

## API Usage Notes

### Groq API Limits (Free Tier)

- **Requests per minute:** 30
- **Requests per day:** 14,400
- **Tokens per minute:** 7,000

Each analysis uses approximately:
- **First call (scoring):** ~3,000 tokens
- **Second call (recommendation):** ~500 tokens
- **Total per analysis:** ~3,500 tokens

**Free tier capacity:** ~120 analyses per hour

### Error Handling

The app gracefully handles:
- Website scraping failures → Falls back to questionnaire-only scoring
- API timeout → Shows friendly error, suggests retry
- Invalid URL → Validates before scraping
- Missing API key → Clear error message with setup instructions

---

## Real-World Use Cases

### 1. Sales Lead Qualification
Run analysis before sales calls to identify specific pain points to address.

### 2. Onboarding Tool
Give to new clients as first step in agency engagement to baseline their current state.

### 3. Cold Outreach
Include personalized analysis in cold emails: "I analyzed your website and found..."

### 4. Webinar/Workshop
Live analyze attendee websites during presentations for engagement.

### 5. Content Marketing
Create case studies showing before/after scores for client work.

---

## Deployment Options

### Option 1: Local Only
Keep running `streamlit run app.py` on your machine for internal use.

### Option 2: Streamlit Cloud (Free)
1. Push code to GitHub
2. Connect Streamlit Cloud account
3. Add GROQ_API_KEY as secret
4. Deploy with one click
5. Get public URL like `yourapp.streamlit.app`

### Option 3: Docker
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

---

**Ready to start analyzing? Run `streamlit run app.py` and go! 🚀**
