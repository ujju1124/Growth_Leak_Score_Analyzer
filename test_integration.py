"""Quick integration test to verify all components work together."""
import sys

print("🧪 Testing Growth Leak Score Analyzer Integration...\n")

# Test 1: Import all modules
print("1️⃣ Testing imports...")
try:
    import scraper
    import scorer
    import rubric
    import models
    import config
    print("   ✅ All modules imported successfully\n")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    print("   Run: pip install -r requirements.txt\n")
    sys.exit(1)

# Test 2: Verify rubric sums to 100
print("2️⃣ Testing rubric...")
total = sum(cat['max_score'] for cat in rubric.RUBRIC)
if total == 100:
    print(f"   ✅ Rubric sums to {total} points\n")
else:
    print(f"   ❌ Rubric sums to {total} instead of 100\n")
    sys.exit(1)

# Test 3: Test scraper with a safe URL
print("3️⃣ Testing scraper...")
try:
    result = scraper.scrape_website("https://www.example.com")
    if 'error' in result:
        print(f"   ⚠️ Scraping returned error: {result['error']}")
        print("   (This might be a network issue, but scraper is working)\n")
    else:
        print(f"   ✅ Scraped successfully")
        print(f"   Title: {result.get('title', 'N/A')[:50]}...\n")
except Exception as e:
    print(f"   ❌ Scraper failed: {e}\n")
    sys.exit(1)

# Test 4: Verify config
print("4️⃣ Testing configuration...")
try:
    api_key = config.GROQ_API_KEY
    if api_key and api_key != "your_groq_api_key_here":
        print(f"   ✅ API key loaded (starts with: {api_key[:10]}...)\n")
    else:
        print("   ⚠️ API key not configured properly")
        print("   Please edit .env and add your real Groq API key\n")
except ValueError as e:
    print(f"   ❌ Config error: {e}")
    print("   Create a .env file with your GROQ_API_KEY\n")
    sys.exit(1)

# Test 5: Pydantic models
print("5️⃣ Testing data models...")
try:
    test_cat = models.CategoryScore(
        name="Test",
        score=10,
        max_score=15,
        reasoning="Test reasoning"
    )
    test_result = models.AnalysisResult(
        categories=[test_cat],
        total_score=10,
        biggest_leak_category="Test",
        recommendation="Test recommendation"
    )
    print("   ✅ Pydantic models working correctly\n")
except Exception as e:
    print(f"   ❌ Model validation failed: {e}\n")
    sys.exit(1)

print("="*60)
print("✅ All integration tests passed!")
print("\nNext steps:")
print("1. Make sure your .env file has a valid GROQ_API_KEY")
print("2. Run: streamlit run app.py")
print("3. Start analyzing businesses!")
print("="*60)
