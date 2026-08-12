"""Streamlit UI for the Growth Leak Score Analyzer."""
import streamlit as st
import re
from scraper import scrape_website
from scraper_selenium import scrape_website_smart
from scorer import analyze_business
from rubric import RUBRIC
from pdf_generator import generate_pdf_report


# Page config
st.set_page_config(
    page_title="Growth Leak Score Analyzer",
    page_icon="📊",
    layout="centered"
)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'result' not in st.session_state:
    st.session_state.result = None


def reset_analysis():
    """Reset the analysis state to allow a new submission."""
    st.session_state.analysis_complete = False
    st.session_state.result = None


def validate_url(url: str) -> bool:
    """Validate that URL starts with http:// or https://."""
    return bool(re.match(r'^https?://', url, re.IGNORECASE))


def get_score_color(score: float) -> str:
    """Return color based on score range."""
    if score < 40:
        return "#ff4444"  # Red
    elif score < 70:
        return "#ffaa00"  # Yellow/Orange
    else:
        return "#44ff44"  # Green


# Main UI
st.title("📊 Growth Leak Score Analyzer")
st.markdown(
    "A free diagnostic tool that analyzes your website and business to identify "
    "your biggest growth leak and provide an actionable fix."
)

if not st.session_state.analysis_complete:
    # Input form
    st.markdown("---")
    st.subheader("🌐 Website Information")
    
    website_url = st.text_input(
        "Company Website URL",
        placeholder="https://www.yourcompany.com",
        help="Enter your full website URL including https://"
    )
    
    # Advanced option for JavaScript-heavy sites
    use_selenium = st.checkbox(
        "🤖 Use advanced scraping (for JavaScript-heavy sites)",
        value=False,
        help="Enable this if the site uses React, Vue, or loads content dynamically. Takes 5-10 seconds longer."
    )
    
    st.markdown("---")
    st.subheader("📋 Business Questionnaire")
    st.markdown("*Help us understand your business better (5-6 quick questions)*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        industry = st.text_input(
            "Industry / Niche",
            placeholder="e.g., B2B SaaS, E-commerce, Coaching"
        )
        
        avg_customer_value = st.number_input(
            "Average Customer Value ($)",
            min_value=0,
            step=100,
            help="Average revenue per customer"
        )
        
        main_channel = st.text_input(
            "Main Marketing Channel",
            placeholder="e.g., Google Ads, SEO, LinkedIn"
        )
    
    with col2:
        monthly_traffic = st.text_input(
            "Estimated Monthly Traffic",
            placeholder="e.g., 5,000 visitors/month",
            help="Optional - approximate is fine"
        )
        
        conversion_rate = st.text_input(
            "Known Conversion Rate",
            placeholder="e.g., 2.5%",
            help="Optional - if you track this"
        )
    
    biggest_challenge = st.text_area(
        "What's your biggest challenge right now?",
        placeholder="e.g., Not enough qualified leads, low conversion rate, high customer acquisition cost...",
        height=100
    )
    
    st.markdown("---")
    
    # Submit button
    if st.button("🔍 Analyze My Business", type="primary", use_container_width=True):
        # Validation
        if not website_url:
            st.error("Please enter your website URL")
        elif not validate_url(website_url):
            st.error("Please enter a valid URL starting with http:// or https://")
        elif not industry or not main_channel:
            st.error("Please fill in at least Industry and Main Marketing Channel")
        else:
            # Run analysis
            with st.spinner("🔍 Analyzing your website and business..."):
                try:
                    # Scrape website (smart method chooses best approach)
                    if use_selenium:
                        st.info("🤖 Using advanced browser rendering...")
                    scraped_data = scrape_website_smart(website_url, use_selenium=use_selenium)
                    
                    # Show scraping status for debugging
                    if 'error' in scraped_data:
                        st.warning(f"⚠️ Scraping issue: {scraped_data['error']}")
                        st.info("Continuing with questionnaire-based analysis...")
                    
                    # Prepare answers
                    answers = {
                        'industry': industry,
                        'avg_customer_value': avg_customer_value,
                        'main_channel': main_channel,
                        'monthly_traffic': monthly_traffic if monthly_traffic else 'Not provided',
                        'conversion_rate': conversion_rate if conversion_rate else 'Not provided',
                        'biggest_challenge': biggest_challenge if biggest_challenge else 'Not provided'
                    }
                    
                    # Store in session state for PDF generation
                    st.session_state.website_url = website_url
                    st.session_state.industry = industry
                    st.session_state.avg_customer_value = avg_customer_value
                    st.session_state.main_channel = main_channel
                    st.session_state.monthly_traffic = monthly_traffic if monthly_traffic else 'Not provided'
                    st.session_state.conversion_rate = conversion_rate if conversion_rate else 'Not provided'
                    
                    # Analyze
                    result = analyze_business(scraped_data, answers)
                    
                    # Store in session state
                    st.session_state.result = result
                    st.session_state.analysis_complete = True
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
                    st.info("Please check your internet connection and API key configuration.")

else:
    # Display results
    result = st.session_state.result
    
    st.markdown("---")
    st.markdown("## 📈 Your Growth Leak Analysis")
    
    # Total score with color
    score_color = get_score_color(result.total_score)
    st.markdown(
        f"<h1 style='text-align: center; color: {score_color}; font-size: 72px;'>"
        f"{result.total_score:.0f}<span style='font-size: 36px;'>/100</span></h1>",
        unsafe_allow_html=True
    )
    
    # Score interpretation
    if result.total_score >= 70:
        st.success("✅ **Strong Foundation** - Your website and marketing are performing well!")
    elif result.total_score >= 40:
        st.warning("⚠️ **Room for Improvement** - Some key areas need attention")
    else:
        st.error("🚨 **Critical Issues** - Significant growth opportunities are being missed")
    
    st.markdown("---")
    
    # Category breakdown
    st.subheader("📊 Category Breakdown")
    
    for cat in result.categories:
        percentage = (cat.score / cat.max_score * 100) if cat.max_score > 0 else 0
        
        with st.expander(f"**{cat.name}**: {cat.score:.1f}/{cat.max_score} ({percentage:.0f}%)"):
            st.progress(percentage / 100)
            st.write(cat.reasoning)
    
    st.markdown("---")
    
    # Biggest leak callout
    st.subheader("🚨 Your Biggest Growth Leak")
    
    leak_cat = next(c for c in result.categories if c.name == result.biggest_leak_category)
    leak_percentage = (leak_cat.score / leak_cat.max_score * 100) if leak_cat.max_score > 0 else 0
    
    st.error(
        f"**{result.biggest_leak_category}**\n\n"
        f"Score: {leak_cat.score:.1f}/{leak_cat.max_score} ({leak_percentage:.0f}%)\n\n"
        f"*{leak_cat.reasoning}*"
    )
    
    st.markdown("---")
    
    # Recommendation
    st.subheader("💡 Recommended Next Step")
    st.info(result.recommendation)
    
    st.markdown("---")
    
    # Reset button
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🔄 Analyze Another Business", use_container_width=True):
            reset_analysis()
            st.rerun()
    
    with col2:
        # PDF Download button
        try:
            # Prepare business info for PDF
            business_info = {
                'industry': st.session_state.get('industry', 'N/A'),
                'avg_customer_value': st.session_state.get('avg_customer_value', 'N/A'),
                'main_channel': st.session_state.get('main_channel', 'N/A'),
                'monthly_traffic': st.session_state.get('monthly_traffic', 'N/A'),
                'conversion_rate': st.session_state.get('conversion_rate', 'N/A'),
            }
            
            # Generate PDF
            pdf_buffer = generate_pdf_report(
                result,
                st.session_state.get('website_url', 'N/A'),
                business_info
            )
            
            # Download button
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer.getvalue(),
                file_name=f"growth_leak_report_{st.session_state.get('website_url', 'report').replace('https://', '').replace('http://', '').replace('/', '_')[:50]}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error generating PDF: {e}")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 14px;'>"
    "Growth Leak Score Analyzer"
    "</p>",
    unsafe_allow_html=True
)
