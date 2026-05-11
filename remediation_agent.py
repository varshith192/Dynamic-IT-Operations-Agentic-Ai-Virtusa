import psutil
import os
import time

# Processes that must never be killed
PROTECTED_PROCESSES = {
    "system", "system idle process", "registry", "smss.exe", "csrss.exe", "wininit.exe",
    "winlogon.exe", "services.exe", "lsass.exe", "svchost.exe", "explorer.exe",
    "dwm.exe", "taskhostw.exe", "runtimebroker.exe", "searchhost.exe", 
    "startmenuexperiencehost.exe", "shellexperiencehost.exe", "sihost.exe", 
    "fontdrvhost.exe", "ctfmon.exe", "conhost.exe", "dllhost.exe", "audiodg.exe",
    "node.exe", "code.exe" # IDE/Node ecosystem
}

def _is_safe_to_kill(pid, name):
    if pid in (0, 1, 4) or pid == os.getpid(): return False
    if name.lower() in PROTECTED_PROCESSES: return False
    return True

def run(predict_message):
    data = predict_message.get("data", {})
    should_act = data.get("should_remediate", False)
    recommendation = data.get("recommended_action", {})
    
    if not should_act or not recommendation:
        return {
            "server": "local",
            "sender": "remediation_agent",
            "type": "REMEDIATION",
            "data": {
                "action_taken": "none",
                "success": True,
                "message": "No remediation required."
            }
        }

    action = recommendation.get("action", "none").lower()
    target_pid = recommendation.get("pid")
    target_name = recommendation.get("process_name", "Unknown")
    reasoning = recommendation.get("reasoning", "No reasoning provided.")

    if action == "none" or not target_pid:
        return {
            "server": "local",
            "sender": "remediation_agent",
            "type": "REMEDIATION",
            "data": {
                "action_taken": "none",
                "success": True,
                "message": f"AI decided to hold: {reasoning}"
            }
        }

    # Safety Validation
    if not _is_safe_to_kill(target_pid, target_name):
        return {
            "server": "local",
            "sender": "remediation_agent",
            "type": "REMEDIATION",
            "data": {
                "action_taken": "aborted",
                "success": False,
                "message": f"SRE Safety Bypass: Refused to kill critical process {target_name} ({target_pid})."
            }
        }

    # Execute Action
    try:
        proc = psutil.Process(target_pid)
        current_name = proc.name()
        
        if action == "kill":
            proc.terminate()
            proc.wait(timeout=3)
            result_msg = f"Successfully terminated {current_name} (PID {target_pid})."
        elif action == "restart":
            # Simulation of restart since real service restart is OS-specific and risky
            # We'll just terminate and assume a watchdog restarts it
            proc.terminate()
            result_msg = f"Restart signal sent to {current_name} (PID {target_pid})."
        else:
            result_msg = f"Action '{action}' is not supported yet."

        return {
            "server": "local",
            "sender": "remediation_agent",
            "type": "REMEDIATION",
            "data": {
                "action_taken": f"AI-Directed {action.capitalize()}",
                "target_process": {"pid": target_pid, "name": target_name},
                "success": True,
                "message": f"{result_msg} Reason: {reasoning}"
            }
        }

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
        return {
            "server": "local",
            "sender": "remediation_agent",
            "type": "REMEDIATION",
            "data": {
                "action_taken": "error",
                "success": False,
                "message": f"Execution failed for {target_name}: {str(e)}"
            }
        }
