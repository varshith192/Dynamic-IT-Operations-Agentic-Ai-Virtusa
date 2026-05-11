import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def run(monitor_message_before, predict_message, remediation_message, monitor_message_after):
    api_key = os.getenv("GROK_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    prompt = f"""
    Synthesize a final SRE executive report based on the full agentic pipeline for the LOCAL SERVER.
    
    1. MONITOR (BEFORE): CPU {monitor_message_before["data"]["cpu"]}%, RAM {monitor_message_before["data"]["memory"]}%
    2. PREDICT (ANALYSIS): {predict_message["data"]["prediction"]}
    3. REMEDIATE (ACTION): {remediation_message["data"]["action_taken"]} - {remediation_message["data"]["message"]}
    4. MONITOR (AFTER): CPU {monitor_message_after["data"]["cpu"]}%, RAM {monitor_message_after["data"]["memory"]}%
    
    STRICT REQUIREMENT: 
    - Contrast the metrics BEFORE vs AFTER. 
    - Be technical and professional.
    
    Return ONLY a JSON object:
    {{
        "server": "local",
        "sender": "report_agent",
        "type": "REPORT",
        "data": {{
            "issue": "Detailed issue description",
            "cause": "Root cause analysis",
            "action_taken": "The exact remediation performed",
            "feedback_loop": "Comparison of metrics showing efficiency",
            "result": "Final system status",
            "summary_message": "A concise executive summary with improvement stats",
            "pipeline_complete": true
        }}
    }}
    """

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a Senior SRE Reporting AI Agent. Your goal is to show the value of automation by highlighting system improvements after remediation."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        ai_message = response.json()["choices"][0]["message"]["content"]
        return json.loads(ai_message)
    except Exception as e:
        # Fallback to simple reporting if AI fails
        cpu_diff = monitor_message_before["data"]["cpu"] - monitor_message_after["data"]["cpu"]
        return {
            "server": "local",
            "sender": "report_agent",
            "type": "REPORT",
            "data": {
                "issue": "Performance bottleneck identified",
                "cause": predict_message["data"]["prediction"],
                "action_taken": remediation_message["data"]["action_taken"],
                "feedback_loop": f"CPU dropped by {cpu_diff:.1f}% after remediation",
                "result": "System stabilized",
                "summary_message": f"Remediation successful. CPU improved from {monitor_message_before['data']['cpu']}% to {monitor_message_after['data']['cpu']}%",
                "pipeline_complete": True
            }
        }
if __name__ == "__main__":
    # Mock data for standalone testing
    monitor_before = {
        "server": "local",
        "sender": "monitor_agent",
        "type": "ALERT",
        "data": {"cpu": 92.5, "memory": 84.1, "timestamp": "2026-03-31T07:15:00"}
    }
    predict = {
        "server": "local",
        "sender": "predict_agent",
        "type": "ANALYSIS",
        "data": {"prediction": "CPU usage is steadily increasing due to high-load stressor."}
    }
    remediation = {
        "server": "local",
        "sender": "remediation_agent",
        "type": "REMEDIATION",
        "data": {"action_taken": "Kill Process", "message": "Successfully terminated high_cpu_stressor.py"}
    }
    monitor_after = {
        "server": "local",
        "sender": "monitor_agent",
        "type": "INFO",
        "data": {"cpu": 35.2, "memory": 42.8, "timestamp": "2026-03-31T07:15:05"}
    }
    
    print("--- Running Standalone Report Agent ---")
    report = run(monitor_before, predict, remediation, monitor_after)
    print(json.dumps(report, indent=2))
