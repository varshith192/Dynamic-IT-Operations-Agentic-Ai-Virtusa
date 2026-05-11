import json
import sys
import os
from dotenv import load_dotenv

# Ensure the script can import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import monitor_agent
import predict_agent
import remediation_agent
import report_agent

load_dotenv()

def run_pipeline():
    # 1. Monitoring Agent (INITIAL)
    monitor_message_before = monitor_agent.run()
    
    # 2. Predictive Agent (AI-DRIVEN ANALYSIS)
    predict_message = predict_agent.run(monitor_message_before)
    
    # 3. Remediation Agent (EXECUTION)
    remediation_message = remediation_agent.run(predict_message)
    
    # 4. Feedback Loop: Monitor After Remediation
    # Allow 2 seconds for process termination to reflect in metrics
    import time
    time.sleep(2)
    monitor_message_after = monitor_agent.run()
    
    # 5. Reporting Agent (SENSING IMPROVEMENT)
    report_message = report_agent.run(
        monitor_message_before, 
        predict_message, 
        remediation_message, 
        monitor_message_after
    )
    
    # Return full A2A message exchange
    return {
        "success": True,
        "server": "local",
        "pipeline": [
            monitor_message_before,
            predict_message,
            remediation_message,
            monitor_message_after,
            report_message
        ]
    }

if __name__ == "__main__":
    try:
        # Check API Key
        if not os.getenv("GROK_API_KEY"):
            print(json.dumps({
                "success": False, "error": "Missing GROK_API_KEY"
            }))
            sys.exit(1)
            
        result = run_pipeline()
        print(json.dumps(result, indent=2))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)
