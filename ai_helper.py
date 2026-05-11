import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

GROK_API_KEY = os.getenv("GROK_API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq(prompt, system_message="You are a helpful DevOps assistant.", json_output=False):
    if not GROK_API_KEY:
        raise ValueError("Missing GROK_API_KEY in environment.")

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    }

    if json_output:
        data["response_format"] = {"type": "json_object"}

    try:
        response = requests.post(URL, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        if json_output:
            return json.loads(content)
        return content
    except Exception as e:
        print(f"❌ Groq API error: {e}")
        return None
