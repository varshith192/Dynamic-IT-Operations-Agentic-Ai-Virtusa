import psutil
from datetime import datetime
import time

def run():
    # Capture real system metrics with accurate 1-second interval
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    # Get top processes for AI context (essential for autonomous remediation)
    processes = []
    # First pass to initialize cpu_percent delta for all processes
    for proc in psutil.process_iter(['cpu_percent']):
        try:
            proc.info['cpu_percent']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    time.sleep(0.1) # Short delay for CPU delta calculation

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            info = proc.info
            processes.append({
                "pid": info['pid'],
                "name": info['name'],
                "cpu": info['cpu_percent'],
                "memory": info['memory_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Sort and take top 5 for AI analysis
    top_processes = sorted(processes, key=lambda x: x['cpu'], reverse=True)[:5]

    # Structured A2A Message
    message = {
        "server": "local",
        "sender": "monitor_agent",
        "type": "ALERT" if cpu > 80 or memory > 90 else "INFO",
        "data": {
            "cpu": cpu,
            "memory": memory,
            "top_processes": top_processes,
            "timestamp": datetime.now().isoformat(),
            "status": "CRITICAL" if cpu > 90 else ("WARNING" if cpu > 70 else "HEALTHY")
        }
    }
    
    return message
