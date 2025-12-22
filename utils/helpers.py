import streamlit as st
from datetime import datetime, timedelta
import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
import re

# Load environment variables (Reads your .env file)
load_dotenv()

# ==================== GEMINI AI CONFIGURATION ====================
# 1. Get API Key securely
gemini_api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
model = None

if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        
        # ⚡ USE STANDARD STABLE MODELS (Dec 2025 Safe List)
        # We try the most likely to work first
        model_options = [
            'gemini-2.5-flash',       # Most reliable (Free Tier Standard)
            'gemini-2.5-pro',         # Standard Pro
            'gemini-pro',             # Legacy Stable
            'gemini-2.5-flash-exp'     # New lightweight
        ]
        
        for m in model_options:
            try:
                test_model = genai.GenerativeModel(m)
                test_model.generate_content("Hi") # Test Pulse
                model = test_model
                print(f"✅ CONNECTED TO: {m}")
                break
            except Exception as e:
                print(f"⚠️ {m} failed: {e}")
                continue

        if not model:
            print("❌ CRITICAL: No working Gemini models found. Check Google AI Studio for valid model names.")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
else:
    print("⚠️ Key Missing: GEMINI_API_KEY")


# ==================== DATE & TIME UTILS ====================

def format_date(date_obj):
    """Format datetime object to readable string"""
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime("%B %d, %Y")


def time_ago(date_obj):
    """Convert datetime to 'time ago' format"""
    if not date_obj:
        return ""
        
    now = datetime.now()
    # Handle timezone awareness
    if date_obj.tzinfo is None and now.tzinfo is None:
        pass
    elif date_obj.tzinfo and now.tzinfo:
        pass
    else:
        date_obj = date_obj.replace(tzinfo=None)
        now = now.replace(tzinfo=None)
        
    diff = now - date_obj
    
    if diff.days > 365:
        return f"{diff.days // 365} year{'s' if diff.days // 365 > 1 else ''} ago"
    elif diff.days > 30:
        return f"{diff.days // 30} month{'s' if diff.days // 30 > 1 else ''} ago"
    elif diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600} hour{'s' if diff.seconds // 3600 > 1 else ''} ago"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60} minute{'s' if diff.seconds // 60 > 1 else ''} ago"
    else:
        return "Just now"


# ==================== VALIDATION UTILS ====================

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Validate phone number format"""
    pattern = r'^[\d\s\+\-\(\)]{10,}$'
    return re.match(pattern, phone) is not None


# ==================== UI HELPERS ====================

def show_success_message(message, duration=3):
    """Display success message with animation"""
    placeholder = st.empty()
    placeholder.markdown(f"""
        <div class="success-box">
            <h3>✅ Success!</h3>
            <p>{message}</p>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(duration)
    placeholder.empty()


def show_error_message(message):
    """Display error message"""
    st.markdown(f"""
        <div class="warning-box">
            <h3>⚠️ Error</h3>
            <p>{message}</p>
        </div>
    """, unsafe_allow_html=True)


def show_info_message(message):
    """Display info message"""
    st.markdown(f"""
        <div class="info-box">
            <h3>ℹ️ Info</h3>
            <p>{message}</p>
        </div>
    """, unsafe_allow_html=True)


# ==================== AI FUNCTIONS (GEMINI POWERED) ====================

def chatbot_response(user_message, context="women empowerment"):
    """Get AI-powered chatbot response"""
    
    # 1. Fallback if API Key is missing or invalid
    if not model:
        return (
            "💡 **Demo Mode (AI Unavailable):**\n\n"
            "**Health:** Eat iron-rich foods & exercise 30 mins daily.\n"
            "**Career:** Update LinkedIn & learn new skills.\n"
            "**Mental:** Practice deep breathing & talk to friends.\n\n"
            "*(Please check your .env file to ensure GEMINI_API_KEY is correct)*"
        )
    
    # 2. Try to get real AI response
    try:
        prompt = f"""
        Role: Helpful, Empathetic Assistant for a Women Empowerment Platform.
        Context: {context}
        User Question: {user_message}
        
        Instructions: Answer in 2-3 short, helpful sentences. Be encouraging.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        # 3. Fallback if Internet/Quota fails
        return f"🤖 **AI Busy:** I'm currently unavailable. Please try again in a moment.\n(Error: {str(e)[:50]})"


def generate_job_recommendation(user_skills, user_experience):
    """Generate job recommendations"""
    if not model:
        return "1. Frontend Developer (Match)\n2. Data Analyst (Analytics)\n3. Product Manager (Strategy) - [Demo Data]"
    
    try:
        prompt = f"""
        Suggest 3 job roles for:
        Skills: {user_skills}
        Experience: {user_experience}
        
        Format:
        1. [Job Title] - [One sentence reason]
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "1. Frontend Developer\n2. Data Analyst\n3. Product Manager (Fallback Data)"


def generate_course_recommendation(interests, current_level):
    """Generate course recommendations"""
    if not model:
        return "1. Python (Udemy)\n2. Web Dev (freeCodeCamp)\n3. Data Science (Coursera) - [Demo Data]"
    
    try:
        prompt = f"""
        Suggest 3 courses for:
        Interests: {interests}
        Level: {current_level}
        
        Format:
        1. [Course Name] ([Platform]) - [Why good]
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "1. Python (Udemy)\n2. Web Dev (freeCodeCamp)\n3. Data Science (Coursera) (Fallback Data)"


# ==================== DATA UTILS ====================

def search_filter(items, query, search_fields):
    """Filter list of items based on search query"""
    if not query:
        return items
    
    query = query.lower()
    filtered = []
    
    for item in items:
        for field in search_fields:
            if field in item and query in str(item[field]).lower():
                filtered.append(item)
                break
    
    return filtered


def paginate(items, page=1, items_per_page=10):
    """Paginate a list of items"""
    start = (page - 1) * items_per_page
    end = start + items_per_page
    return items[start:end], len(items)


def get_sample_data_if_none(data, sample_data):
    """Return sample data if database is empty"""
    if data and len(data) > 0:
        return data
    return sample_data


def format_currency(amount, currency="₹"):
    """Format currency value"""
    if amount is None:
        return f"{currency}0"
    return f"{currency}{amount:,.2f}"
