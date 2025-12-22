import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta
import os
import re

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.css_loader import load_css
from utils.helpers import chatbot_response

# Load CSS
load_css()

# ==================== STATE MANAGEMENT ====================
# --- Dashboard State ---
if 'heart_rate' not in st.session_state: st.session_state['heart_rate'] = 72
if 'water_intake' not in st.session_state: st.session_state['water_intake'] = 6
if 'steps' not in st.session_state: st.session_state['steps'] = 7234
if 'sleep_hours' not in st.session_state: st.session_state['sleep_hours'] = 7.5

# --- Nutrition State ---
if 'cal_breakfast' not in st.session_state: st.session_state['cal_breakfast'] = 300
if 'cal_lunch' not in st.session_state: st.session_state['cal_lunch'] = 500
if 'cal_dinner' not in st.session_state: st.session_state['cal_dinner'] = 450
if 'cal_snacks' not in st.session_state: st.session_state['cal_snacks'] = 150
if 'meal_breakfast' not in st.session_state: st.session_state['meal_breakfast'] = ""
if 'meal_lunch' not in st.session_state: st.session_state['meal_lunch'] = ""
if 'meal_dinner' not in st.session_state: st.session_state['meal_dinner'] = ""
if 'meal_snacks' not in st.session_state: st.session_state['meal_snacks'] = ""

# --- Period Tracker State ---
if 'last_period' not in st.session_state: st.session_state['last_period'] = datetime.now().date() - timedelta(days=5)
if 'cycle_length' not in st.session_state: st.session_state['cycle_length'] = 28
if 'period_length' not in st.session_state: st.session_state['period_length'] = 5

# ==================== HERO SECTION ====================
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">❤️ Health & Wellness</h1>
        <p class="hero-subtitle">
            Take charge of your health with AI-driven insights and tracking tools
        </p>
    </div>
""", unsafe_allow_html=True)

# ==================== HEALTH DASHBOARD ====================
st.markdown("## 📊 Your Health Dashboard")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
dash_style = "padding: 20px; border-radius: 15px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1); height: 100%;"

with col1:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); {dash_style}">
            <h3 style="font-size: 32px; margin: 0;">💓</h3>
            <h2 style="font-size: 36px; margin: 10px 0; color: white;">{st.session_state['heart_rate']}</h2>
            <p style="margin: 0; opacity: 0.9;">Heart Rate (bpm)</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); {dash_style}">
            <h3 style="font-size: 32px; margin: 0;">💧</h3>
            <h2 style="font-size: 36px; margin: 10px 0; color: white;">{st.session_state['water_intake']}/8</h2>
            <p style="margin: 0; opacity: 0.9;">Water Intake (glasses)</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); {dash_style}">
            <h3 style="font-size: 32px; margin: 0;">🏃‍♀️</h3>
            <h2 style="font-size: 36px; margin: 10px 0; color: white;">{st.session_state['steps']:,}</h2>
            <p style="margin: 0; opacity: 0.9;">Steps Today</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); {dash_style}">
            <h3 style="font-size: 32px; margin: 0;">😴</h3>
            <h2 style="font-size: 36px; margin: 10px 0; color: white;">{st.session_state['sleep_hours']}h</h2>
            <p style="margin: 0; opacity: 0.9;">Sleep Last Night</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ==================== TRACKING TABS ====================
st.markdown("## 📝 Track Your Health")
st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🩺 General Health", "🍎 Nutrition", "🧘‍♀️ Mental Wellness", "🧠 Period Tracker"])

# --- TAB 1: General Health ---
with tab1:
    st.markdown("### 🩺 Daily Health Log")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("health_log_form"):
            c1, c2 = st.columns(2)
            with c1:
                weight = st.number_input("Weight (kg)", value=60.0, step=0.1)
                height = st.number_input("Height (cm)", value=165.0, step=1.0)
                blood_pressure = st.text_input("Blood Pressure", placeholder="120/80")
            with c2:
                hr_input = st.number_input("Heart Rate (bpm)", min_value=40, max_value=180, value=st.session_state['heart_rate'])
                water_input = st.slider("Water Intake (glasses)", 0, 15, st.session_state['water_intake'])
                sleep_input = st.slider("Sleep Hours", 0.0, 12.0, st.session_state['sleep_hours'], 0.5)
            
            health_notes = st.text_area("Daily Notes", placeholder="Any symptoms or mood changes...")
            
            submitted = st.form_submit_button("💾 Save Health Log", use_container_width=True)
            if submitted:
                st.session_state['heart_rate'] = hr_input
                st.session_state['water_intake'] = water_input
                st.session_state['sleep_hours'] = sleep_input
                st.success("✅ Dashboard updated!")
                st.rerun()

    with col2:
        st.markdown("#### ⚖️ BMI Calculator")
        bmi = weight / ((height/100) ** 2)
        bmi = round(bmi, 1)
        
        bmi_color = "green"
        bmi_status = "Healthy Weight"
        if bmi < 18.5: 
            bmi_status = "Underweight"; bmi_color = "orange"
        elif bmi > 25: 
            bmi_status = "Overweight"; bmi_color = "orange"
        elif bmi > 30: 
            bmi_status = "Obese"; bmi_color = "red"
            
        st.markdown(f"""
            <div style="background: white; border: 1px solid #eee; padding: 20px; border-radius: 15px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <h1 style="margin:0; font-size: 48px; color: {bmi_color};">{bmi}</h1>
                <p style="margin:0; font-weight: bold; color: {bmi_color};">{bmi_status}</p>
                <p style="font-size: 12px; color: #888; margin-top: 10px;">Healthy range: 18.5 - 24.9</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 🚑 Quick Symptom Checker")
    
    sym_col1, sym_col2 = st.columns([3, 1])
    with sym_col1:
        symptom_query = st.text_input("Describe what you are feeling...", placeholder="e.g., I have a throbbing headache and nausea")
    with sym_col2:
        st.write("") 
        st.write("") 
        check_sym = st.button("🔍 Check", use_container_width=True)
        
    if check_sym and symptom_query:
        with st.spinner("Consulting AI Health Assistant..."):
            prompt = f"I am feeling: {symptom_query}. Provide 3 simple home remedies and tell me when I should see a doctor. Keep it short."
            advice = chatbot_response(prompt, context="First Aid & Home Remedies")
            st.info(advice)

# --- TAB 2: Nutrition (AI MACROS & MEAL IDEAS) ---
with tab2:
    st.markdown("### 🍎 Smart Nutrition Tracker")
    
    if 'protein' not in st.session_state: st.session_state['protein'] = 0
    if 'carbs' not in st.session_state: st.session_state['carbs'] = 0
    if 'fats' not in st.session_state: st.session_state['fats'] = 0

    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("#### 🍽️ Log Your Meals")
        st.session_state['meal_breakfast'] = st.text_area("Breakfast", value=st.session_state['meal_breakfast'], placeholder="e.g., 2 Eggs and Toast", height=70)
        st.session_state['meal_lunch'] = st.text_area("Lunch", value=st.session_state['meal_lunch'], placeholder="e.g., Chicken Salad", height=70)
        st.session_state['meal_dinner'] = st.text_area("Dinner", value=st.session_state['meal_dinner'], placeholder="e.g., Salmon and Rice", height=70)
        st.session_state['meal_snacks'] = st.text_area("Snacks", value=st.session_state['meal_snacks'], placeholder="e.g., Apple", height=70)
    
    # --- UPDATED AI MACRO ESTIMATOR (GEMINI POWERED) ---
    def ai_estimate_macros():
        meals = f"B: {st.session_state.get('meal_breakfast')} L: {st.session_state.get('meal_lunch')} D: {st.session_state.get('meal_dinner')} S: {st.session_state.get('meal_snacks')}"
        if len(meals) < 20: return 

        try:
            prompt = f"""
            Analyze these meals: {meals}.
            Estimate total: 1. Calories 2. Protein(g) 3. Carbs(g) 4. Fats(g).
            Return ONLY 4 numbers separated by commas. Example: 1500, 80, 150, 50.
            """
            
            # Use Gemini helper function instead of direct OpenAI call
            response_text = chatbot_response(prompt, context="Nutritionist")
            
            # Extract numbers using regex
            nums = re.findall(r'\d+', response_text)
            
            if len(nums) >= 4:
                st.session_state['cal_total'] = int(nums[0])
                st.session_state['protein'] = int(nums[1])
                st.session_state['carbs'] = int(nums[2])
                st.session_state['fats'] = int(nums[3])
            else:
                # Fallback if AI output isn't perfect
                st.session_state['cal_total'] = 1650
                st.session_state['protein'] = 90
                st.session_state['carbs'] = 180
                st.session_state['fats'] = 60
        except: 
            pass

    with col2:
        st.markdown("#### 📊 Nutritional Breakdown")
        
        total_cal = st.session_state.get('cal_total', 0)
        
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Protein", f"{st.session_state['protein']}g")
        with m2: st.metric("Carbs", f"{st.session_state['carbs']}g")
        with m3: st.metric("Fats", f"{st.session_state['fats']}g")

        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white; text-align: center; margin-top: 15px;">
                <h3 style="margin: 0;">Total Calories</h3>
                <h1 style="font-size: 42px; margin: 10px 0; color: white;">{total_cal}</h1>
            </div>
        """, unsafe_allow_html=True)
        
        st.button("⚡ Calculate Macros (AI)", on_click=ai_estimate_macros, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("#### 🥗 Need a Healthy Meal Idea?")
    remaining_cal = 2000 - total_cal
    if st.button(f"Suggest a {remaining_cal} calorie dinner idea"):
        with st.spinner("Chef AI is thinking..."):
            prompt = f"Suggest a healthy, easy-to-cook dinner recipe that is approximately {remaining_cal} calories. Vegetarian or Lean Protein options."
            recipe = chatbot_response(prompt, context="Healthy Recipes")
            st.success(recipe)

# --- TAB 3: Mental Wellness ---
with tab3:
    st.markdown("### 🧘‍♀️ Mental Wellness Sanctuary")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("#### 📅 How are you feeling right now?")
    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    
    if col_a.button("🤩 Amazing", use_container_width=True): 
        st.session_state['current_mood'] = "Amazing"
        st.success("You're glowing! Keep spreading that positivity! ✨")
    
    if col_b.button("🙂 Good", use_container_width=True): 
        st.session_state['current_mood'] = "Good"
        st.info("That's great! A balanced mind is a powerful tool. 🌿")
    
    if col_c.button("😐 Okay", use_container_width=True): 
        st.session_state['current_mood'] = "Okay"
        st.warning("It's okay to just be okay. Be gentle with yourself today. ☕")
    
    if col_d.button("😫 Stressed", use_container_width=True): 
        st.session_state['current_mood'] = "Stressed"
        st.error("Deep breath. This feeling is temporary. You've got this. 💪")
    
    if col_e.button("😢 Sad", use_container_width=True): 
        st.session_state['current_mood'] = "Sad"
        st.error("Sending you a virtual hug. It's okay to cry and let it out. ❤️")

    st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### 💬 Safe Venting Space")
        st.markdown("*Write down what's on your mind. AI will listen and offer support.*")
        
        vent_text = st.text_area("What's bothering you today?", height=150, placeholder="I'm feeling overwhelmed because...")
        
        if st.button("💙 Share & Get Support"):
            if vent_text:
                with st.spinner("Listening and thinking..."):
                    prompt = f"I am feeling {st.session_state.get('current_mood', 'unsure')}. Here is what's on my mind: '{vent_text}'. Please act as an empathetic, supportive friend/therapist. Validate my feelings and offer 1-2 gentle coping strategies. Keep it short and warm."
                    support_msg = chatbot_response(prompt, context="Mental Health Support")
                    
                    st.markdown(f"""
                        <div style="background-color: #f0f7ff; border-left: 5px solid #4facfe; padding: 20px; border-radius: 10px; margin-top: 15px;">
                            <h4 style="color: #005cbf; margin-top:0;">Here for you 💙</h4>
                            <p style="font-size: 16px; line-height: 1.6; color: #333;">{support_msg}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Please write something first. We are here to listen.")

    with col2:
        st.markdown("#### 🌬️ Box Breathing")
        st.info("Follow the circle: Inhale (4s), Hold (4s), Exhale (4s), Hold (4s).")
        
        st.markdown("""
            <style>
            @keyframes breathe {
                0% { transform: scale(1); opacity: 0.6; background-color: #a8edea; }
                50% { transform: scale(1.5); opacity: 1; background-color: #4facfe; }
                100% { transform: scale(1); opacity: 0.6; background-color: #a8edea; }
            }
            .breathing-circle {
                width: 100px;
                height: 100px;
                border-radius: 50%;
                margin: 20px auto;
                animation: breathe 8s infinite ease-in-out;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                box-shadow: 0 0 20px rgba(79, 172, 254, 0.4);
            }
            </style>
            <div class="breathing-circle">Breathe</div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✨ Get Daily Affirmation", use_container_width=True):
            affirmations = [
                "I am enough just as I am.",
                "My feelings are valid and I accept them.",
                "I have the power to create change.",
                "I deserve peace and happiness.",
                "One step at a time is enough."
            ]
            import random
            chosen = random.choice(affirmations)
            st.success(f"**{chosen}**")

    st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown("#### 🆘 Crisis Resources")
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.error("📞 **Helpline:** 988 (Suicide & Crisis Lifeline)")
    with res_col2:
        st.warning("💬 **Text Line:** Text HOME to 741741")

# --- TAB 4: ADVANCED PERIOD TRACKER ---
with tab4:
    st.markdown("### 🧠 Advanced AI Period Tracker")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        last_p = st.date_input("Last Period Start Date", value=st.session_state['last_period'])
        c_len = st.slider("Average Cycle Length", 21, 35, st.session_state['cycle_length'])
        p_len = st.slider("Period Length", 3, 10, st.session_state['period_length'])
        st.session_state['last_period'] = last_p
        st.session_state['cycle_length'] = c_len
        st.session_state['period_length'] = p_len

    today = datetime.now().date()
    days_since_start = (today - last_p).days
    current_cycle_day = (days_since_start % c_len) + 1
    
    phase = "Luteal Phase"
    phase_color = "#a8edea"
    if current_cycle_day <= p_len: phase = "Menstrual Phase"; phase_color = "#ff6b6b"
    elif current_cycle_day <= (c_len / 2) - 2: phase = "Follicular Phase"; phase_color = "#4facfe"
    elif current_cycle_day <= (c_len / 2) + 2: phase = "Ovulation Phase"; phase_color = "#fa709a"

    with col2:
        st.markdown(f"""
            <div style="background: white; border: 2px solid {phase_color}; padding: 20px; border-radius: 15px; text-align: center;">
                <h4 style="color: #666; margin:0;">Current Status</h4>
                <h2 style="color: {phase_color}; font-size: 32px; margin: 10px 0;">Day {current_cycle_day}</h2>
                <span style="background: {phase_color}; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold;">{phase}</span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 💬 AI Symptom Analysis")
    symptoms = st.multiselect("Select symptoms:", ["Cramps", "Headache", "Mood Swings", "Fatigue", "Bloating", "Acne", "Cravings"])
    
    if st.button("🧠 Analyze Cycle", use_container_width=True):
        with st.spinner("Analyzing..."):
            prompt = f"Day {current_cycle_day} of {c_len}-day cycle. Phase: {phase}. Symptoms: {symptoms}. Give brief diet & mood advice."
            advice = chatbot_response(prompt, context="Women's Health")
            st.info(advice)

st.markdown("<br><br>", unsafe_allow_html=True)

# ==================== GENERAL AI HEALTH ASSISTANT ====================
st.markdown("## 🤖 General Health Assistant")
health_question = st.text_input("💬 Ask any other health question:", placeholder="E.g., Benefits of magnesium?")
if st.button("💡 Get General Advice", use_container_width=True):
    if health_question:
        with st.spinner("Getting advice..."):
            response = chatbot_response(health_question, context="women's health")
            st.info(response)

# ==================== CLICKABLE RESOURCES ====================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("## 📚 Health Resources")

r_col1, r_col2, r_col3 = st.columns(3)

res_card_style = """
    background: white; padding: 25px; border-radius: 15px; 
    border: 1px solid #eee; box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
    text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;
"""

with r_col1:
    st.markdown(f"""<div style="{res_card_style}"><h3>🏥</h3><h4>Find Doctors</h4><p style="font-size:13px; color:#666;">Book appointments with specialists near you</p></div>""", unsafe_allow_html=True)
    st.link_button("Find on Practo", "https://www.practo.com/doctors", use_container_width=True)

with r_col2:
    st.markdown(f"""<div style="{res_card_style}"><h3>💊</h3><h4>Order Medicines</h4><p style="font-size:13px; color:#666;">Get medicines delivered to your doorstep</p></div>""", unsafe_allow_html=True)
    st.link_button("Go to 1mg", "https://www.1mg.com", use_container_width=True)

with r_col3:
    st.markdown(f"""<div style="{res_card_style}"><h3>📖</h3><h4>Health Library</h4><p style="font-size:13px; color:#666;">Trusted articles on women's health</p></div>""", unsafe_allow_html=True)
    st.link_button("Visit Healthline", "https://www.healthline.com/womens-health", use_container_width=True)
