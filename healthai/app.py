import streamlit as st
import pandas as pd
from utils.ai import get_ai_response, predict_disease, generate_treatment_plan
from utils.visualizer import display_health_analytics


#st.set_page_config(page_title="AI Health Assistant", layout="wide")
st.set_page_config(page_title="🧠 HealthAI", layout="wide")
st.markdown("<h1 style='text-align: center;'>🩺 HealthAI - Intelligent Healthcare Assistant</h1>", unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp {
        background-color: #1e1e1e;
    }

    .stButton>button {
        background-color: cyan;
        color: black;
    }

    .stButton>button:hover {
        box-shadow: 3px 4px 5px lightgreen;
        color: black;
    }

    .stSidebar:hover {
        box-shadow: 4px 4px 5px white;
    }
    </style>
""", unsafe_allow_html=True)

if "profile" not in st.session_state:
    st.session_state.profile = {}


col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("## 🙍 Patient Profile")
    with st.form("profile_form"):
        name = st.text_input("Name", st.session_state.profile.get("name", ""))
        age = st.number_input("Age", min_value=0, max_value=120, step=1, value=st.session_state.profile.get("age", 30))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(st.session_state.profile.get("gender", "Male")))
        history = st.text_area("Medical History", st.session_state.profile.get("history", ""))
        medications = st.text_area("Current Medications", st.session_state.profile.get("medications", ""))
        allergies = st.text_input("Allergies", st.session_state.profile.get("allergies", ""))

        submitted = st.form_submit_button("💾 Save Profile")
        if submitted:
            st.session_state.profile = {
                "name": name,
                "age": age,
                "gender": gender,
                "history": history,
                "medications": medications,
                "allergies": allergies
            }
            st.success("✅ Profile saved!")

    if st.session_state.profile:
        st.markdown("#### 🧾 Saved Info")
        st.json(st.session_state.profile)


with col2:

    profile = st.session_state.profile
    profile_summary = f"""
    Patient Info:
    - Age: {profile.get('age')}
    - Gender: {profile.get('gender')}
    - History: {profile.get('history')}
    - Medications: {profile.get('medications')}
    - Allergies: {profile.get('allergies')}
    """
    
    menu = st.sidebar.selectbox("Navigation", [
      "Patient Chat",
      "Disease Prediction",
      "Treatment Plan",
      "Health Analytics"
    ])
    
    
    if menu == "Patient Chat":
       st.title("🗨️ Patient Chat")
       user_input = st.text_area("Enter your health concern:")
       prompt=f"""You are HealthAI, an intelligent and safe AI medical assistant. Respond clearly using bullet points. Be medically accurate, empathetic, and concise.

Instructions:
- If symptoms are minor: give home remedies and self-care tips.
- If symptoms are serious: recommend seeing a healthcare provider.
- Avoid vague or blog-style answers.
- Do not make a diagnosis here.

Patient's message:{user_input}

Your response (clear advice in bullet points):
"""
       token=300
       if st.button("Know what is the problem"):
          response = get_ai_response(prompt,token)
          cleaned = response.replace("<human>:", "").replace("<bot>:", "").strip()
          st.success(cleaned)
   
    elif menu == "Disease Prediction":
       symptoms = st.text_input("Enter symptoms (comma-separated):")
       if st.button("Predict Disease"):
          result = predict_disease(symptoms)
          st.info(result)
   
    elif menu == "Treatment Plan":
       disease = st.text_input("Enter diagnosed disease:")
       if st.button("Get Treatment Plan"):
          plan = generate_treatment_plan(disease)
          st.write(plan)


    elif menu == "Health Analytics":
       uploaded_file = st.file_uploader("Upload your health data (CSV or Excel)", type=['csv', 'xlsx'])

       if uploaded_file is not None:
          try:
              if uploaded_file.name.endswith('.csv'):
                  df = pd.read_csv(uploaded_file)
              else:
                  df = pd.read_excel(uploaded_file)
  
              display_health_analytics(df)

          except Exception as e:
              st.error(f"Error loading file: {e}")
