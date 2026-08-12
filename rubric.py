"""Scoring rubric definition for the Growth Leak Score Analyzer."""

# The rubric categories must sum to 100 points total
RUBRIC = [
    {
        "name": "Value Proposition Clarity",
        "max_score": 15,
        "description": "Is it obvious within seconds what the business sells and to whom? Clear headline, subheadline, and messaging that communicates value."
    },
    {
        "name": "Call-to-Action Strength",
        "max_score": 15,
        "description": "Is there one clear, visible primary action (Book a call, Buy now, Sign up)? CTA should be prominent and action-oriented."
    },
    {
        "name": "Lead Capture Mechanism",
        "max_score": 15,
        "description": "Ways to capture a visitor's contact info - contact form, live chat, phone number, email address. Multiple capture points increase score."
    },
    {
        "name": "Trust & Social Proof",
        "max_score": 10,
        "description": "Presence of testimonials, case studies, client logos, reviews, or success stories that build credibility and trust."
    },
    {
        "name": "SEO & Content Basics",
        "max_score": 10,
        "description": "Meta description quality, blog/content presence, title tag clarity. Foundation for organic discovery."
    },
    {
        "name": "Tracking & Follow-up Readiness",
        "max_score": 10,
        "description": "Presence of analytics or ad pixel tags (Google Analytics, Facebook Pixel, etc.) indicating ability to retarget and follow up with visitors."
    },
    {
        "name": "Marketing Channel Effectiveness",
        "max_score": 12,
        "description": "From questionnaire: which marketing channels they use and how well those channels are performing. Diversification and effectiveness matter."
    },
    {
        "name": "Conversion Health",
        "max_score": 13,
        "description": "From questionnaire: conversion rate, average customer value, and self-identified challenges. Overall conversion funnel performance."
    },
]

# Verify the rubric sums to 100
assert sum(cat["max_score"] for cat in RUBRIC) == 100, "Rubric categories must sum to 100 points"


def get_rubric_summary() -> str:
    """Return a formatted string summary of the rubric for use in prompts."""
    summary = "SCORING RUBRIC (Total: 100 points)\n\n"
    for i, cat in enumerate(RUBRIC, 1):
        summary += f"{i}. {cat['name']} ({cat['max_score']} points)\n"
        summary += f"   {cat['description']}\n\n"
    return summary
