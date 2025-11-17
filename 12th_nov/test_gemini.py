import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

print("🔍 Available models that support generateContent:\n")
# List available models
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"✅ {m.name}")

print("\n" + "="*60)
print("🧪 Testing Gemini 2.5 Flash model...")
print("="*60 + "\n")

# Test with the correct model name
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Say hello in a friendly way")
    print(f"✅ SUCCESS! Model Response:\n{response.text}\n")
    print("🎉 Your Gemini API is working perfectly!")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    print("\n💡 Available models to try:")
    print("   - gemini-2.5-flash (recommended - free & fast)")
    print("   - gemini-2.5-pro")
    print("   - gemini-2.0-flash")