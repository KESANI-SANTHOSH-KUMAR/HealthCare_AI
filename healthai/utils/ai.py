import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AI_API_KEY") or st.secrets("AI_API_KEY")
WML_URL = os.getenv("AI_URL") or st.secrets("AI_URL")
PROJECT_ID = os.getenv("AI_PROJECT_ID") or st.secrets("AI_PROJECT_ID")

def get_ai_response(prompt,token):
    token_url = "https://iam.cloud.ibm.com/identity/token"
    print("🔐 Getting access token...")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "apikey": API_KEY,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }

    token_response = requests.post(token_url, headers=headers, data=data)
    if token_response.status_code != 200:
        return "⚠️ Error fetching access token."

    access_token = token_response.json().get("access_token")
    print("✅ Access token received")
    print("🚀 Sending prompt to Granite model...")

    model_id = "ibm/granite-3-2b-instruct"
    inference_url = f"{WML_URL}/ml/v1/text/generation?version=2024-05-01"

    payload = {
        "model_id": model_id,
        "input": prompt,
        # "parameters": {
        #     "decoding_method": "greedy",
        #     "max_new_tokens": 500
        # },
        "parameters": {
            "decoding_method": "greedy",    
            "max_new_tokens":token           # Longer output
        },
        "project_id": PROJECT_ID  
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(inference_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['results'][0]['generated_text']
    else:
        return f"❌ API Error: {response.status_code} - {response.text}"
# if __name__ == "__main__":
#     prompt = "Explain Artificial Intelligence in simple words."
#     response = get_ai_response(prompt)
#     print("🤖 Response:", response)

def predict_disease(symptoms):
    st.title("🧠 Disease Prediction")
    prompt =  f"""
You are HealthAI, a medically accurate and safe AI assistant. A patient describes their symptoms.

Symptoms: {symptoms}

Based on these symptoms, list the **top 3 most likely common diseases** (not rare ones), ordered by estimated likelihood. Be realistic.

Format:
Top 3 likely diagnoses with estimated likelihoods:
1. [Most likely disease]: 70%
2. [Second most likely disease]: 20%
3. [Less likely disease]: 10%

Only include diseases that match the given symptoms and are likely in general population.

    """
    token=200
    return get_ai_response(prompt,token)

def generate_treatment_plan(disease):
    st.title("📝 Treatment Plan")
    prompt = f"""You are HealthAI, a professional AI healthcare assistant.

A patient is affected by the following disease: **{disease}**

Provide a guideline-based treatment plan suitable for outpatient care. Keep the response concise, safe, and medically accurate.

Format:
**Disease**: {disease}

**Treatment Plan**:
1. [First-line treatment or medication]
2. [Supportive advice or lifestyle changes]
3. [When to consult a doctor or specialist]

Avoid unproven, experimental, or off-label treatments. Follow established clinical standards and safety practices.
"""
    token=400
    return get_ai_response(prompt,token)


# if __name__ == "__main__":
#     while True:
#         prompt = input("\n📝 Enter your prompt (or type 'exit' to quit):\n> ")
#         if prompt.lower() == "exit":
#             break
#         response = get_ai_response(prompt)
#         print("\n🤖 AI Response:\n", response)

def prompt_simple_summary(df):
    desc = df.describe(include='all').to_string()
    
    prompt = (
        "This is a health dataset containing information like heart rate, blood pressure, glucose levels, and symptoms.\n"
        "Here is the summary:\n"
        f"{desc}\n\n"
        "Please write a short and easy-to-understand paragraph summarizing the key points in this data for a doctor."
    )
    token=400

    return get_ai_response(prompt,token)
