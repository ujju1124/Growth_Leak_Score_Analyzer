"""Website scraping module for extracting business and marketing signals."""
import requests
from bs4 import BeautifulSoup
from typing import Dict
import re


def scrape_website(url: str) -> Dict:
    """
    Scrape a website URL and extract business/marketing signals.
    
    Args:
        url: The website URL to scrape
        
    Returns:
        Dictionary containing extracted data or error information
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        # Make request with timeout
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Store full page source for pattern detection (before any modifications)
        page_source = response.text.lower()
        
        # Extract page title
        title = soup.title.string.strip() if soup.title else "No title found"
        
        # Extract meta description (always include in full - don't truncate)
        meta_desc = ""
        meta_tag = soup.find('meta', attrs={'name': 'description'}) or \
                   soup.find('meta', attrs={'property': 'og:description'})
        if meta_tag:
            meta_desc = meta_tag.get('content', '').strip()
        
        # Create a copy for content extraction (don't modify the original soup for feature detection)
        content_soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove only navigation, scripts, and styles BEFORE extracting text
        # DO NOT remove <header> or <footer> as they often contain important content
        for element in content_soup(['script', 'style', 'nav']):
            element.decompose()
        
        # Try to extract from <main> or main content area first
        main_content = content_soup.find('main') or \
                      content_soup.find('div', attrs={'id': re.compile(r'main|content', re.I)}) or \
                      content_soup.find('div', attrs={'class': re.compile(r'main|content', re.I)})
        
        # Extract visible body text from main content or full body (truncate to 4000 chars)
        if main_content:
            body_text = main_content.get_text(separator=' ', strip=True)
        else:
            body_text = content_soup.get_text(separator=' ', strip=True)
        
        body_text = re.sub(r'\s+', ' ', body_text)[:4000]
        
        # Check for contact form (use original soup, not modified content_soup)
        has_contact_form = bool(
            soup.find('form') and (
                soup.find('input', attrs={'type': 'email'}) or
                soup.find('textarea') or
                'contact' in page_source
            )
        )
        
        # Check for pricing page/link (use original soup)
        has_pricing = bool(
            soup.find('a', href=re.compile(r'pricing|price|plans', re.I)) or
            re.search(r'\bpricing\b|\bplans\b|\bprice\b', page_source, re.I)
        )
        
        # Check for live chat widget - use FULL page source, not truncated text
        chat_patterns = [
            # Popular platforms
            r'intercom', r'drift', r'tawk\.to', r'crisp',
            r'livechat', r'zendesk', r'olark', r'liveperson',
            # Additional platforms
            r'tidio', r'chatra', r'livechatinc', r'helpscout',
            r'userlike', r'snapengage', r'purechat', r'chatbot',
            r'freshchat', r'livesupport', r'comm100', r'liveagent',
            # Generic chat indicators
            r'chat-widget', r'chat-button', r'live-chat',
            r'chat\.js', r'webchat', r'messenger-widget',
            # Visual indicators in text
            r'chat with us', r'live support', r'talk to us'
        ]
        has_live_chat = any(re.search(pattern, page_source) for pattern in chat_patterns)
        
        # Check for analytics/ad pixels - use FULL page source
        tracking_patterns = [
            # Google Analytics (GA3 & GA4)
            r'google-analytics\.com/analytics\.js',
            r'googletagmanager\.com/gtag/js',
            r'google-analytics\.com/ga\.js',
            r'gtag\(', r'ga\(', r'_ga', r'GA_MEASUREMENT_ID',
            r'G-[A-Z0-9]{10}',  # GA4 measurement IDs
            r'UA-\d+-\d+',  # Universal Analytics IDs
            
            # Facebook/Meta Pixel
            r'connect\.facebook\.net', r'fbevents\.js',
            r'fbq\(', r'_fbq', r'facebook\.com/tr',
            r'FB_PIXEL_ID', r'facebook-pixel',
            
            # Google Ads
            r'googleadservices\.com', r'google\.com/ads',
            r'googlesyndication\.com', r'adsbygoogle',
            
            # Other major platforms
            r'hotjar', r'_hjSettings', r'hjid',
            r'mixpanel', r'amplitude', r'segment\.com',
            r'linkedin\.com/insight', r'snap\.licdn\.com',
            r'analytics\.tiktok', r'clarity\.ms',
            r'plausible\.io', r'matomo', r'piwik',
            r'heap\.io', r'fullstory', r'logrocket',
            
            # Tag managers
            r'tagmanager', r'tealium', r'ensighten'
        ]
        has_tracking = any(re.search(pattern, page_source) for pattern in tracking_patterns)
        
        # Check for testimonials/reviews - check FULL page source, not just truncated body_text
        testimonial_keywords = [
            # Direct testimonial indicators
            'testimonial', 'review', 'customer success', 'case study',
            'client story', 'what our clients say', 'feedback',
            'success story', 'customer story', 'client testimonial',
            
            # Review platforms
            'trustpilot', 'g2.com', 'capterra', 'gartner',
            'rated', 'stars', 'reviews',
            
            # Social proof phrases
            'what people say', 'hear from our', 'customer voices',
            'real results', 'proven results', 'client results',
            'loved by', 'trusted by', 'companies using',
            
            # Quantified social proof
            r'\d+\+?\s*(customers|clients|users|companies)',
            r'\d+\s*stars?', r'5\.0', r'4\.[5-9]',
            r'\d+k?\+?\s*reviews?'
        ]
        has_testimonials = any(
            re.search(keyword if isinstance(keyword, str) and keyword.startswith('\\d') else re.escape(keyword), 
                     page_source) 
            for keyword in testimonial_keywords
        )
        
        # Check for blog/content section - use original soup
        has_blog = bool(
            soup.find('a', href=re.compile(r'/blog|/articles|/resources|/news|/insights|/learn|/content|/knowledge', re.I)) or
            re.search(r'\b(blog|articles|resources|insights|knowledge\s+base)\b', page_source, re.I)
        )
        
        # Check for email/phone contact info - use FULL page source
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_patterns = [
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
            r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',  # (123) 456-7890
            r'\+\d{1,3}\s*\d{1,14}',  # International
            r'tel:', r'phone:', r'call us'
        ]
        has_email = bool(re.search(email_pattern, page_source))
        has_phone = any(re.search(pattern, page_source) for pattern in phone_patterns)
        
        # NEW: Check for CTA strength indicators (expanded with search-based CTAs)
        strong_cta_keywords = [
            # Traditional action CTAs
            r'get\s+started', r'start\s+free', r'try\s+free',
            r'sign\s+up', r'get\s+demo', r'book\s+a?\s*demo',
            r'contact\s+sales', r'request\s+demo', r'free\s+trial',
            r'buy\s+now', r'shop\s+now', r'add\s+to\s+cart',
            r'learn\s+more', r'get\s+quote', r'schedule\s+call',
            
            # Search/discovery CTAs (for sites like Airbnb, Booking.com, Google)
            r'search', r'find', r'explore', r'discover',
            r'where\s+to', r'check\s+in', r'check\s+out',
            r'check\s+availability', r'view\s+all', r'browse',
            r'start\s+your\s+search', r'see\s+options'
        ]
        cta_count = sum(len(re.findall(pattern, body_text.lower())) for pattern in strong_cta_keywords)
        
        # Also check for search forms/inputs as CTAs
        search_forms = soup.find_all(['input', 'button'], attrs={
            'type': re.compile(r'search|submit', re.I)
        }) or soup.find_all(['input', 'button'], attrs={
            'placeholder': re.compile(r'search|find|where|what|when', re.I)
        })
        if search_forms:
            cta_count += len(search_forms)
        
        # Check for security/trust badges - use FULL page source
        trust_indicators = [
            r'ssl', r'secure', r'encrypted', r'https',
            r'money.?back', r'guarantee', r'certified',
            r'bbb\s+accredited', r'norton', r'mcafee',
            r'trustwave', r'verisign', r'privacy\s+policy',
            r'terms\s+of\s+service', r'gdpr', r'compliance'
        ]
        has_trust_badges = any(re.search(pattern, page_source) for pattern in trust_indicators)
        
        return {
            'success': True,
            'url': url,
            'title': title,
            'meta_description': meta_desc,
            'body_text': body_text,
            'has_contact_form': has_contact_form,
            'has_pricing': has_pricing,
            'has_live_chat': has_live_chat,
            'has_tracking': has_tracking,
            'has_testimonials': has_testimonials,
            'has_blog': has_blog,
            # New enhanced detections
            'has_email': has_email,
            'has_phone': has_phone,
            'cta_count': cta_count,
            'has_trust_badges': has_trust_badges,
        }
        
    except requests.exceptions.Timeout:
        return {'error': 'Request timed out after 10 seconds'}
    except requests.exceptions.ConnectionError:
        return {'error': 'Could not connect to the website'}
    except requests.exceptions.HTTPError as e:
        return {'error': f'HTTP error: {e.response.status_code}'}
    except requests.exceptions.RequestException as e:
        return {'error': f'Request failed: {str(e)}'}
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'}


if __name__ == "__main__":
    # Test with a few real URLs
    test_urls = [
        "https://www.example.com",
        "https://www.stripe.com",
        "https://www.shopify.com"
    ]
    
    for url in test_urls:
        print(f"\n{'='*60}")
        print(f"Testing: {url}")
        print('='*60)
        result = scrape_website(url)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Success!")
            print(f"Title: {result['title']}")
            print(f"Meta: {result['meta_description'][:100]}...")
            print(f"Body preview: {result['body_text'][:200]}...")
            print(f"\nSignals:")
            print(f"  Contact Form: {result['has_contact_form']}")
            print(f"  Pricing: {result['has_pricing']}")
            print(f"  Live Chat: {result['has_live_chat']}")
            print(f"  Tracking: {result['has_tracking']}")
            print(f"  Testimonials: {result['has_testimonials']}")
            print(f"  Blog: {result['has_blog']}")
