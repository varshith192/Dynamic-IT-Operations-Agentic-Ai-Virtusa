import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def run(monitor_message):
    api_key = os.getenv("GROK_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    cpu = monitor_message["data"]["cpu"]
    memory = monitor_message["data"]["memory"]

    prompt = f"""
    Analyze the following LOCAL SERVER system metrics and process list for IT operations.
    Current Metrics: CPU {cpu}%, Memory {memory}%
    Top Processes: {monitor_message["data"].get("top_processes", [])}
    
    CRITICAL: You are an autonomous SRE Predictive Agent.
    Task:
    1. Evaluate the system for potential risks. 
    2. Detect Trends: If CPU > 70% or Memory > 70%, identify it as an "Increasing Pattern" risk. 
    3. Forecasting: Predict if this will lead to a system crash or service degradation.
    4. Recommend Action: Based on the top processes, decide if we should "kill" a specific PID or "restart" a service.
    
    Focus on creating a specific risk message like: "CPU usage is steadily increasing due to [Process Name], potential overload risk detected."
    
    Return ONLY a JSON object:
    {{
        "server": "local",
        "sender": "predict_agent",
        "type": "ANALYSIS",
        "data": {{
            "risk_level": "Healthy | Warning | Critical",
            "prediction": "Professional SRE risk assessment (e.g. CPU usage is steadily increasing...)",
            "should_remediate": true/false,
            "recommended_action": {{
                "action": "kill | restart | none",
                "pid": int or null,
                "process_name": "string or null",
                "reasoning": "Technical reasoning for this automated intervention"
            }},
            "reasoning": "Summary of overall system health and trend analysis"
        }}
    }}
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a Predictive SRE AI Agent specializing in infrastructure health and risk forecasting."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        ai_message = response.json()["choices"][0]["message"]["content"]
        return json.loads(ai_message)
    except Exception as e:
        # Fallback to rule-based if AI fails
        return {
            "server": "local",
            "sender": "predict_agent",
            "type": "ANALYSIS",
            "data": {
                "risk_level": "Critical" if cpu > 90 else "Healthy",
                "prediction": "Analyzing system metrics and predicting potential failures",
                "should_remediate": cpu > 85 or memory > 80,
                "reasoning": f"Fallback: metrics (CPU:{cpu}% | MEM:{memory}%) exceed manual thresholds."
            }
        }
