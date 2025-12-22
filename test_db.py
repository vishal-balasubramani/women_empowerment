import os
from dotenv import load_dotenv

# 1. Try to load .env
loaded = load_dotenv()

print("--- DEBUG REPORT ---")
print(f"1. .env file found and loaded? {loaded}")

# 2. Check Key
key = os.getenv("GEMINI_API_KEY")

if key:
    print(f"2. Key found: Yes (Length: {len(key)})")
    print(f"3. Key starts with: {key[:5]}...")
    
    # 4. Test Key with Google
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello")
        print("4. Google API Test: ✅ SUCCESS! The key works.")
    except Exception as e:
        print(f"4. Google API Test: ❌ FAILED. Error: {e}")
else:
    print("2. Key found: ❌ NO. The variable GEMINI_API_KEY is empty.")
    print("   -> Check if your file is named exactly '.env' (no .txt)")
    print("   -> Check if the line says: GEMINI_API_KEY=AIza...")
