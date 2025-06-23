import streamlit as st
from utils.ai import get_ai_response
from utils.ai import predict_disease, generate_treatment_plan
from utils.visualizer import display_health_analytics
import pandas as pd
#st.image("https://png.pngtree.com/background/20250102/original/pngtree-vivid-abstract-texture-a-burst-of-colorful-background-picture-image_15292555.jpg", use_container_width=True)
st.markdown(
    """<style>
    .stApp{
    background-color:black-gray;
    }
    .stButton>button{
     background-color:cyan;
     color:black;
    }
    .stButton>button:hover{
     box-shadow:3px 4px 5px lightgreen;
     color:black;
    }
    .stSidebar:hover{
    box-shadow:4px 4px 5px white;}
 
   
    </style>""",unsafe_allow_html=True
)

st.set_page_config(page_title="AI Health Assistant", layout="wide")
st.title("🧠 AI-Powered Healthcare Assistant")

menu = st.sidebar.selectbox("Navigation", ["Patient Chat", "Disease Prediction", "Treatment Plan", "Health Analytics"])

if menu == "Patient Chat":
    user_input = st.text_area("Enter your health concern:")
    if st.button("Know what is the problem"):
       response = get_ai_response(user_input)
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
