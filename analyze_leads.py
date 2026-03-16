from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env
api_key = os.getenv("OPENAI_API_KEY")

import pandas as pd
from openai import OpenAI
import json
import re

# Groq API
client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

df = pd.read_csv("leads.csv")

results = []

def safe_json_parse(text):
    """
    Safely parse AI output. Use regex fallback if JSON is invalid.
    """
    try:
        return json.loads(text)
    except:
        data = {}
        for key in ["industry", "lead_score", "business_need", "recommended_action"]:
            match = re.search(rf'"?{key}"?\s*[:=]\s*"?(.*?)"?(\n|,|$)', text, re.IGNORECASE)
            data[key] = match.group(1).strip() if match else ""
        return data

def normalize_lead_score(score_str):
    """
    Convert lead score to 0-100 numeric.
    Handles "8/10", "78", "80%" etc.
    Works even if score_str is int or float.
    """
    score_str = str(score_str).replace("%", "").strip()  # <- convert to string first
    if "/" in score_str:
        parts = score_str.split("/")
        try:
            score = float(parts[0]) / float(parts[1]) * 100
        except:
            score = 0
    else:
        try:
            score = float(score_str)
        except:
            score = 0
    return int(score)

def get_priority(score):
    if score >= 80:
        return "High"
    elif score >= 50:
        return "Medium"
    else:
        return "Low"

## Process Each Lead

for _, row in df.iterrows():
    prompt = f"""
You are an AI assistant that qualifies sales leads.

Lead Info:
Name: {row['Name']}
Company: {row['Company Name']}
Job Title: {row['Job Title']}
Message: {row['Message']}

Return JSON with the following keys:
"industry", "lead_score" (0-100), "business_need", "recommended_action"
Respond ONLY with JSON. Do not include explanations or extra text.
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    ai_output = response.choices[0].message.content.strip()
    data = safe_json_parse(ai_output)

    # Normalize lead score and calculate priority
    score = normalize_lead_score(data.get("lead_score", "0"))
    priority = get_priority(score)

    results.append({
        "Name": row["Name"],
        "Email": row["Email"],
        "Company": row["Company Name"],
        "Job Title": row["Job Title"],
        "Industry": data.get("industry", ""),
        "Lead Score": score,
        "Lead Priority": priority,
        "Business Need": data.get("business_need", ""),
        "Recommended Action": data.get("recommended_action", "")
    })

## Save to CSV

output_df = pd.DataFrame(results)
output_df.to_csv("output.csv", index=False)
print(" AI Lead Qualification Automation completed successfully!")