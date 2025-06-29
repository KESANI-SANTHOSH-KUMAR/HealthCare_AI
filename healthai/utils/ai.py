import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AI_API_KEY")
WML_URL = os.getenv("AI_URL")
PROJECT_ID = os.getenv("AI_PROJECT_ID")

def get_ai_response(prompt):
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
            "max_new_tokens": 150           # Longer output
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
    prompt =  f"""
A patient is experiencing the following symptoms: {symptoms}.

Please consider the most common and likely causes first, based on global clinical guidelines. Avoid listing rare or severe diseases unless strongly indicated.

List top 3 possible diagnoses with estimated likelihoods in percentage format. Example:
    - Common Cold: 60%
    - Flu: 25%
    - COVID-19: 10%
    """
    return get_ai_response(prompt)

def generate_treatment_plan(disease):
    prompt = f"Suggest a treatment plan for the disease: {disease}."
    return get_ai_response(prompt)


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

    return get_ai_response(prompt)
