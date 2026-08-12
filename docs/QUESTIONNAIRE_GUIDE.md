# 📋 Business Questionnaire - Purpose & Usage Guide

## 🎯 Why We Need the Questionnaire

The questionnaire captures **internal business intelligence** that can't be seen by just looking at a website. This makes the analysis more accurate and personalized.

---

## 📊 How Each Question is Used

### 1️⃣ **Industry / Niche**
**Example:** "B2B SaaS", "E-commerce", "Coaching"

**How it's used:**
- Sets context for what's "normal" in your industry
- Affects scoring expectations (e.g., B2B SaaS should have longer forms, E-commerce needs shopping cart)
- Helps generate industry-specific recommendations
- Influences what conversion rate is considered good

**Impact on scoring:**
- Value Proposition Clarity (15 pts)
- Call-to-Action Strength (15 pts)
- Conversion Health (13 pts)

**Example reasoning:**
> "For a B2B SaaS company, the 'Book a Demo' CTA is appropriate, but should be more prominent above the fold."

---

### 2️⃣ **Average Customer Value**
**Example:** $500, $5,000, $50,000

**How it's used:**
- Validates if your website matches your price point
- High-value businesses ($10k+) should have more trust signals
- Low-value businesses ($100-$500) need friction-free checkouts
- Affects whether you need sales calls vs. self-serve

**Impact on scoring:**
- Call-to-Action Strength (15 pts) - High value = "Book a call", Low value = "Buy now"
- Trust & Social Proof (10 pts) - Higher value needs more proof
- Lead Capture Mechanism (15 pts) - Appropriate for price point
- Conversion Health (13 pts) - Context for conversion rate

**Example reasoning:**
> "With a $5,000 customer value, the lack of social proof is critical - prospects need validation before high-value purchases."

---

### 3️⃣ **Main Marketing Channel**
**Example:** "Google Ads", "LinkedIn", "SEO", "Referrals", "Facebook"

**How it's used:**
- Identifies single-channel dependency risk
- Validates if tracking pixels match the channel (e.g., using Facebook ads but no Facebook Pixel)
- Assesses channel/website alignment
- Checks if landing page matches channel expectations

**Impact on scoring:**
- Marketing Channel Effectiveness (12 pts) ⭐ **DIRECT IMPACT**
- Tracking & Follow-up Readiness (10 pts) - Should have appropriate pixels
- SEO & Content Basics (10 pts) - If SEO is main channel, content is critical

**Example reasoning:**
> "Single-channel dependence on LinkedIn Ads creates risk. No diversification into organic content or email marketing."

---

### 4️⃣ **Estimated Monthly Traffic** (Optional)
**Example:** "1,000 visitors/month", "50k/month", "Not sure"

**How it's used:**
- Context for conversion rate calculation
- Identifies if traffic is the problem vs. conversion
- Helps prioritize: get more traffic or convert better?
- Validates if marketing channel is working

**Impact on scoring:**
- Marketing Channel Effectiveness (12 pts) ⭐ **DIRECT IMPACT**
- Conversion Health (13 pts) - Traffic volume affects strategy

**Example reasoning:**
> "With only 1,000 monthly visitors, the priority should be traffic generation before optimization."

---

### 5️⃣ **Known Conversion Rate** (Optional)
**Example:** "1.5%", "5%", "Not tracking"

**How it's used:**
- **CRITICAL METRIC** - Compares to industry benchmarks
- Identifies if the website is the bottleneck
- Validates if CTA/forms are working
- Prioritizes fixes (low conversion = website problem, high conversion = traffic problem)

**Impact on scoring:**
- Conversion Health (13 pts) ⭐ **MAJOR IMPACT**
- Call-to-Action Strength (15 pts) - Low conversion suggests weak CTAs
- Lead Capture Mechanism (15 pts) - Friction in capture process

**Industry Benchmarks:**
- E-commerce: 2-3%
- B2B SaaS: 2-5%
- Lead generation: 5-15%
- Coaching/Consulting: 3-8%

**Example reasoning:**
> "1.5% conversion rate is below the 2-5% B2B SaaS average, indicating website optimization should be the top priority."

---

### 6️⃣ **Biggest Challenge Right Now**
**Example:** "Not enough leads", "Low conversion", "Traffic is expensive", "Can't scale"

**How it's used:**
- Validates what the AI analysis discovers
- Prioritizes recommendations around their pain point
- Provides context for what they've already tried
- Makes recommendations more actionable and relevant

**Impact on scoring:**
- Conversion Health (13 pts) ⭐ **DIRECT IMPACT**
- Influences recommendation focus across all categories

**Example reasoning:**
> "Challenge aligns with analysis: 'Not enough qualified leads' correlates with missing lead capture mechanisms and weak social proof."

---

## 🔄 How Website Data + Questionnaire Work Together

### Scoring Flow:

```
1. Website Scraping (Categories 1-6)
   ├─ Value Proposition Clarity (15 pts) ← Title, meta, body text
   ├─ Call-to-Action Strength (15 pts) ← Body text analysis
   ├─ Lead Capture Mechanism (15 pts) ← Forms, chat, phone detected
   ├─ Trust & Social Proof (10 pts) ← Testimonials detected
   ├─ SEO & Content Basics (10 pts) ← Meta tags, blog presence
   └─ Tracking & Follow-up (10 pts) ← Pixels detected

2. Questionnaire (Categories 7-8)
   ├─ Marketing Channel Effectiveness (12 pts)
   │  ├─ Main Channel (from Q3)
   │  ├─ Traffic Volume (from Q4)
   │  └─ Industry Context (from Q1)
   │
   └─ Conversion Health (13 pts)
      ├─ Conversion Rate (from Q5) ⭐ CRITICAL
      ├─ Customer Value (from Q2)
      ├─ Industry Benchmarks (from Q1)
      └─ Self-reported Challenge (from Q6)

3. Combined Analysis
   ├─ AI validates consistency between website and answers
   ├─ Identifies biggest gap (leak)
   └─ Generates specific recommendation
```

---

## 💡 Real-World Example

### Input:
**Website:** Basic landing page, no testimonials, simple form
**Questionnaire:**
- Industry: `B2B SaaS`
- Avg Customer Value: `$12,000/year`
- Main Channel: `LinkedIn Ads`
- Traffic: `3,000/month`
- Conversion Rate: `0.8%`
- Challenge: `Leads don't convert to sales calls`

### Analysis:
```
📊 Scores:
- Trust & Social Proof: 2/10 ⚠️ (missing testimonials)
- Conversion Health: 4/13 ⚠️ (0.8% is way below 2-5% benchmark)
- Lead Capture: 8/15 (form exists but basic)

🚨 Biggest Leak: Conversion Health (31% of max)

💡 Recommendation:
"Your 0.8% conversion rate is 60% below the B2B SaaS average of 2-5%. 
Given your $12,000 customer value and LinkedIn Ads focus, immediately add 
3-4 customer testimonials with specific ROI results (e.g., 'Saved 40 hours/week'). 
Then test a two-step form (email first, then book call) to reduce friction. 
This combination typically lifts enterprise SaaS conversions by 30-50%."
```

**Why this is powerful:**
- Without the conversion rate (0.8%), we'd just see "no testimonials"
- With it, we know the LOW CONVERSION is the real problem
- The recommendation is specific to their $12k price point and LinkedIn audience
- Actionable steps, not vague advice

---

## 🎯 Summary: Why Each Question Matters

| Question | Critical For | If You Skip It |
|----------|--------------|----------------|
| **Industry** | Context setting | Generic recommendations |
| **Customer Value** | Trust signals needed | Wrong CTA type suggested |
| **Main Channel** | Channel diversification | Missing tracking issues |
| **Traffic** | Prioritization | Can't assess if traffic or conversion is the problem |
| **Conversion Rate** | **MOST IMPORTANT** | Can't measure website effectiveness |
| **Challenge** | Relevant recommendations | Recommendations may not match pain points |

---

## ✅ Best Practices for Filling Out the Questionnaire

### ✅ DO:
- Be honest (the AI can tell if answers don't match the website)
- Provide conversion rate if you track it (makes analysis 10x better)
- Describe your actual biggest challenge
- Use specific numbers where possible

### ❌ DON'T:
- Inflate numbers to look good (you'll get wrong recommendations)
- Leave everything blank (reduces analysis accuracy)
- Provide competitor info instead of your own
- Guess wildly if you don't know (say "not sure" instead)

---

## 🔧 Technical Implementation

The questionnaire data is sent to the AI alongside the scraped website data:

```python
QUESTIONNAIRE ANSWERS:
- Industry: B2B SaaS
- Average Customer Value: $5,000
- Main Marketing Channel: LinkedIn Ads
- Estimated Monthly Traffic: 2,000 visitors/month
- Known Conversion Rate: 1.5%
- Biggest Challenge: Not enough qualified leads
```

The AI then scores all 8 categories considering BOTH the website and the answers, identifying misalignments and opportunities.

---

**Bottom Line:** The questionnaire transforms this from a "website audit" into a "business growth analysis." It's what makes the recommendations actually useful! 🚀
