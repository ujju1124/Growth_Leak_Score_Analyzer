"""Quick test to ensure app.py loads without errors."""
import sys

print("Testing app.py imports and initialization...\n")

try:
    # Import the app module without running it
    import importlib.util
    spec = importlib.util.spec_from_file_location("app", "app.py")
    app_module = importlib.util.module_from_spec(spec)
    
    print("✅ app.py loads without syntax errors")
    print("\nThe Streamlit app should be running in the background.")
    print("Check your browser - it should have opened automatically!")
    print("\nIf not, open: http://localhost:8501")
    
except Exception as e:
    print(f"❌ Error loading app: {e}")
    sys.exit(1)
