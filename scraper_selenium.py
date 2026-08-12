"""Enhanced website scraping with Selenium for JavaScript rendering."""
import time
from typing import Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re

# Import the basic scraper as fallback
from scraper import scrape_website as scrape_basic


def scrape_with_selenium(url: str, wait_time: int = 5) -> Dict:
    """
    Scrape a website using Selenium to render JavaScript.
    
    Args:
        url: The website URL to scrape
        wait_time: Seconds to wait for JavaScript to load (default: 5)
        
    Returns:
        Dictionary containing extracted data or error information
    """
    driver = None
    
    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Additional options for cloud environments
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-setuid-sandbox')
        
        # Only add experimental options on Windows (Streamlit Cloud doesn't support these)
        import platform
        if platform.system() == 'Windows':
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User agent
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # On Linux (Streamlit Cloud), use chromium binary path
        if platform.system() == 'Linux':
            chrome_options.binary_location = '/usr/bin/chromium'
        
        # Initialize driver
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            # Fallback for Streamlit Cloud - try without webdriver-manager
            if platform.system() == 'Linux':
                service = Service('/usr/bin/chromedriver')
                driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                raise e
        
        driver.set_page_load_timeout(15)
        
        # Load the page
        driver.get(url)
        
        # Wait for JavaScript to render
        time.sleep(wait_time)
        
        # Get the rendered HTML
        page_source = driver.page_source
        page_source_lower = page_source.lower()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Extract page title
        title = driver.title or "No title found"
        
        # Extract meta description (always include in full - don't truncate)
        meta_desc = ""
        meta_tag = soup.find('meta', attrs={'name': 'description'}) or \
                   soup.find('meta', attrs={'property': 'og:description'})
        if meta_tag:
            meta_desc = meta_tag.get('content', '').strip()
        
        # Create a copy for content extraction (don't modify the original soup for feature detection)
        content_soup = BeautifulSoup(page_source, 'html.parser')
        
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
                'contact' in page_source_lower
            )
        )
        
        # Check for pricing page/link (use original soup)
        has_pricing = bool(
            soup.find('a', href=re.compile(r'pricing|price|plans', re.I)) or
            re.search(r'\bpricing\b|\bplans\b|\bprice\b', page_source_lower, re.I)
        )
        
        # Check for live chat widget - use FULL page source
        chat_patterns = [
            r'intercom', r'drift', r'tawk\.to', r'crisp',
            r'livechat', r'zendesk', r'olark', r'liveperson',
            r'tidio', r'chatra', r'livechatinc', r'helpscout',
            r'userlike', r'snapengage', r'purechat', r'chatbot',
            r'freshchat', r'livesupport', r'comm100', r'liveagent',
            r'chat-widget', r'chat-button', r'live-chat',
            r'chat\.js', r'webchat', r'messenger-widget',
            r'chat with us', r'live support', r'talk to us'
        ]
        has_live_chat = any(re.search(pattern, page_source_lower) for pattern in chat_patterns)
        
        # Check for analytics/ad pixels - use FULL page source
        tracking_patterns = [
            # Google Analytics
            r'google-analytics\.com', r'googletagmanager\.com',
            r'gtag\(', r'ga\(', r'_ga', r'GA_MEASUREMENT_ID',
            r'G-[A-Z0-9]{10}', r'UA-\d+-\d+',
            
            # Facebook/Meta
            r'connect\.facebook\.net', r'fbevents\.js',
            r'fbq\(', r'_fbq', r'facebook\.com/tr',
            
            # Google Ads
            r'googleadservices\.com', r'google\.com/ads',
            r'googlesyndication\.com', r'adsbygoogle',
            
            # Other platforms
            r'hotjar', r'_hjSettings', r'hjid',
            r'mixpanel', r'amplitude', r'segment\.com',
            r'linkedin\.com/insight', r'snap\.licdn\.com',
            r'analytics\.tiktok', r'clarity\.ms',
            r'plausible\.io', r'matomo', r'piwik',
            r'heap\.io', r'fullstory', r'logrocket',
            r'tagmanager', r'tealium', r'ensighten'
        ]
        has_tracking = any(re.search(pattern, page_source_lower) for pattern in tracking_patterns)
        
        # Check for testimonials/reviews - check FULL page source
        testimonial_keywords = [
            'testimonial', 'review', 'customer success', 'case study',
            'client story', 'what our clients say', 'feedback',
            'success story', 'customer story', 'client testimonial',
            'trustpilot', 'g2.com', 'capterra', 'gartner',
            'rated', 'stars', 'reviews',
            'what people say', 'hear from our', 'customer voices',
            'real results', 'proven results', 'client results',
            'loved by', 'trusted by', 'companies using',
            r'\d+\+?\s*(customers|clients|users|companies)',
            r'\d+\s*stars?', r'5\.0', r'4\.[5-9]',
            r'\d+k?\+?\s*reviews?'
        ]
        has_testimonials = any(
            re.search(keyword if '\\d' in str(keyword) else re.escape(str(keyword)), 
                     page_source_lower) 
            for keyword in testimonial_keywords
        )
        
        # Check for blog/content section - use original soup
        has_blog = bool(
            soup.find('a', href=re.compile(r'/blog|/articles|/resources|/news|/insights|/learn|/content|/knowledge', re.I)) or
            re.search(r'\b(blog|articles|resources|insights|knowledge\s+base)\b', page_source_lower, re.I)
        )
        
        # Check for email/phone contact info - use FULL page source
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_patterns = [
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',
            r'\+\d{1,3}\s*\d{1,14}',
            r'tel:', r'phone:', r'call us'
        ]
        has_email = bool(re.search(email_pattern, page_source_lower))
        has_phone = any(re.search(pattern, page_source_lower) for pattern in phone_patterns)
        
        # Check for CTA strength indicators (expanded with search-based CTAs)
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
        has_trust_badges = any(re.search(pattern, page_source_lower) for pattern in trust_indicators)
        
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
            'has_email': has_email,
            'has_phone': has_phone,
            'cta_count': cta_count,
            'has_trust_badges': has_trust_badges,
            'method': 'selenium'  # Indicate which method was used
        }
        
    except TimeoutException:
        return {'error': 'Page load timeout after 15 seconds'}
    except WebDriverException as e:
        return {'error': f'Browser error: {str(e)[:100]}...'}
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)[:100]}...'}
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


def scrape_website_smart(url: str, use_selenium: bool = False) -> Dict:
    """
    Smart scraping: tries basic scraper first, falls back to Selenium if needed.
    
    Args:
        url: The website URL to scrape
        use_selenium: Force use of Selenium (default: False, tries basic first)
        
    Returns:
        Dictionary containing extracted data
    """
    if use_selenium:
        # User explicitly wants Selenium
        return scrape_with_selenium(url)
    
    # Try basic scraper first (faster)
    result = scrape_basic(url)
    
    # Check if basic scraper worked and found reasonable data
    if 'error' in result:
        # Basic scraper failed, try Selenium
        print("⚠️ Basic scraper failed, trying Selenium...")
        return scrape_with_selenium(url)
    
    # Check if we got minimal data (might be JS-heavy site)
    if (not result.get('has_tracking') and 
        not result.get('has_live_chat') and
        result.get('cta_count', 0) < 2):
        # Might be missing JS-rendered content, try Selenium
        print("⚠️ Limited data detected, trying Selenium for better results...")
        selenium_result = scrape_with_selenium(url)
        
        # If Selenium succeeds and finds more, use it
        if 'error' not in selenium_result:
            return selenium_result
    
    # Basic scraper worked fine
    return result


if __name__ == "__main__":
    # Test both methods
    test_url = "https://www.hubspot.com"
    
    print("="*60)
    print(f"Testing: {test_url}")
    print("="*60)
    
    print("\n1️⃣ Testing BASIC scraper...")
    basic_result = scrape_basic(test_url)
    if 'error' in basic_result:
        print(f"❌ Error: {basic_result['error']}")
    else:
        print(f"✅ Success!")
        print(f"  Live Chat: {basic_result.get('has_live_chat')}")
        print(f"  Tracking: {basic_result.get('has_tracking')}")
        print(f"  CTAs: {basic_result.get('cta_count', 0)}")
    
    print("\n2️⃣ Testing SELENIUM scraper...")
    selenium_result = scrape_with_selenium(test_url)
    if 'error' in selenium_result:
        print(f"❌ Error: {selenium_result['error']}")
    else:
        print(f"✅ Success!")
        print(f"  Live Chat: {selenium_result.get('has_live_chat')}")
        print(f"  Tracking: {selenium_result.get('has_tracking')}")
        print(f"  CTAs: {selenium_result.get('cta_count', 0)}")
    
    print("\n3️⃣ Testing SMART scraper (auto-select)...")
    smart_result = scrape_website_smart(test_url)
    print(f"✅ Used method: {smart_result.get('method', 'basic')}")
    print(f"  Live Chat: {smart_result.get('has_live_chat')}")
    print(f"  Tracking: {smart_result.get('has_tracking')}")
    print(f"  CTAs: {smart_result.get('cta_count', 0)}")
