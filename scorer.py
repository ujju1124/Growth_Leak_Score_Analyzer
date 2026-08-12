"""Groq LLM analysis and scoring logic."""
import json
from typing import Dict
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
from models import AnalysisResult, CategoryScore
from rubric import RUBRIC, get_rubric_summary


def analyze_business(scraped_data: Dict, answers: Dict) -> AnalysisResult:
    """
    Analyze business using Groq LLM and calculate Growth Leak Score.
    
    Args:
        scraped_data: Dictionary of scraped website data
        answers: Dictionary of questionnaire answers
        
    Returns:
        AnalysisResult with scores, leak identification, and recommendation
    """
    client = Groq(api_key=GROQ_API_KEY)
    
    # Build the scoring system prompt with embedded rubric
    scoring_system_prompt = f"""You are a growth marketing expert analyzing a business website and questionnaire.

{get_rubric_summary()}

Your task is to score each category based on the website data and questionnaire answers provided.

For website-dependent categories (1-6), if the website could not be scraped, mark reasoning as "Could not verify from website" and score conservatively (50% of max).

Return ONLY a valid JSON object with this exact structure:
{{
  "categories": [
    {{
      "name": "Value Proposition Clarity",
      "score": 12.5,
      "max_score": 15,
      "reasoning": "One clear sentence explaining the score"
    }},
    ... (all 8 categories)
  ]
}}

Do NOT include a "total_score" field - it will be calculated separately.
Be specific in your reasoning. Reference actual observations from the data."""

    # Build user prompt with scraped data and answers
    website_section = ""
    if 'error' in scraped_data:
        website_section = f"⚠️ Website scraping failed: {scraped_data['error']}\n\n"
        website_section += "Score website-dependent categories conservatively based on questionnaire alone.\n"
    else:
        website_section = f"""WEBSITE DATA:
URL: {scraped_data.get('url', 'N/A')}
Title: {scraped_data.get('title', 'N/A')}
Meta Description: {scraped_data.get('meta_description', 'None found')}

DETECTED FEATURES:
- Contact Form: {scraped_data.get('has_contact_form', False)}
- Pricing Page: {scraped_data.get('has_pricing', False)}
- Live Chat: {scraped_data.get('has_live_chat', False)}
- Email Contact: {scraped_data.get('has_email', False)}
- Phone Contact: {scraped_data.get('has_phone', False)}
- Analytics/Tracking: {scraped_data.get('has_tracking', False)}
- Testimonials/Social Proof: {scraped_data.get('has_testimonials', False)}
- Blog/Content Section: {scraped_data.get('has_blog', False)}
- CTA Count: {scraped_data.get('cta_count', 0)} strong CTAs detected
- Trust Badges/Security: {scraped_data.get('has_trust_badges', False)}

BODY TEXT PREVIEW:
{scraped_data.get('body_text', 'N/A')[:1500]}...
"""

    questionnaire_section = f"""
QUESTIONNAIRE ANSWERS:
- Industry: {answers.get('industry', 'Not provided')}
- Average Customer Value: ${answers.get('avg_customer_value', 'Not provided')}
- Main Marketing Channel: {answers.get('main_channel', 'Not provided')}
- Estimated Monthly Traffic: {answers.get('monthly_traffic', 'Not provided')}
- Known Conversion Rate: {answers.get('conversion_rate', 'Not provided')}
- Biggest Challenge: {answers.get('biggest_challenge', 'Not provided')}
"""

    user_prompt = website_section + questionnaire_section
    
    # Call Groq API for scoring with retry logic
    max_retries = 2
    for attempt in range(max_retries):
        try:
            completion = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": scoring_system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
            )
            
            # Parse response
            response_text = completion.choices[0].message.content
            parsed_json = json.loads(response_text)
            
            # Validate categories
            categories = [CategoryScore(**cat) for cat in parsed_json["categories"]]
            
            # Ensure we have all 8 categories
            if len(categories) != 8:
                raise ValueError(f"Expected 8 categories, got {len(categories)}")
            
            break  # Success!
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            if attempt == max_retries - 1:
                raise RuntimeError(f"Failed to parse LLM response after {max_retries} attempts: {e}")
            continue
    
    # Recompute total score (never trust the LLM's math)
    total_score = sum(cat.score for cat in categories)
    
    # Identify biggest leak (lowest score/max_score ratio)
    biggest_leak = min(categories, key=lambda c: c.score / c.max_score if c.max_score > 0 else 0)
    
    # Generate focused recommendation with second Groq call
    recommendation_prompt = f"""This business scored {biggest_leak.score:.1f} out of {biggest_leak.max_score} in the "{biggest_leak.name}" category.

Reasoning: {biggest_leak.reasoning}

Write a 2-3 sentence specific, actionable recommendation to fix this weakness. Be concrete and tactical - what should they do first?"""

    rec_completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are a growth marketing consultant providing actionable recommendations."},
            {"role": "user", "content": recommendation_prompt},
        ],
        temperature=0.5,
        max_tokens=200,
    )
    
    recommendation = rec_completion.choices[0].message.content.strip()
    
    # Build and return final result
    return AnalysisResult(
        categories=categories,
        total_score=round(total_score, 1),
        biggest_leak_category=biggest_leak.name,
        recommendation=recommendation
    )


if __name__ == "__main__":
    # Test with hardcoded data
    test_scraped = {
        'success': True,
        'url': 'https://example.com',
        'title': 'Example Business - We Help Companies Grow',
        'meta_description': 'Professional services for growing businesses',
        'body_text': 'We help companies scale. Our proven methodology delivers results. Contact us today for a free consultation.',
        'has_contact_form': True,
        'has_pricing': False,
        'has_live_chat': False,
        'has_tracking': True,
        'has_testimonials': False,
        'has_blog': True,
    }
    
    test_answers = {
        'industry': 'B2B SaaS',
        'avg_customer_value': 5000,
        'main_channel': 'LinkedIn ads',
        'monthly_traffic': '2000',
        'conversion_rate': '1.5%',
        'biggest_challenge': 'Not enough qualified leads'
    }
    
    print("Testing scorer with sample data...")
    try:
        result = analyze_business(test_scraped, test_answers)
        print(f"\n✅ Total Score: {result.total_score}/100")
        print(f"\n📊 Category Breakdown:")
        for cat in result.categories:
            print(f"  {cat.name}: {cat.score}/{cat.max_score} - {cat.reasoning}")
        print(f"\n🚨 Biggest Leak: {result.biggest_leak_category}")
        print(f"\n💡 Recommendation: {result.recommendation}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
