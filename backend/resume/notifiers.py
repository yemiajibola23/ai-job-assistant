from datetime import datetime

def console_notifier(message: str):
    timestamp = datetime.now().isoformat(timespec="seconds")
    print(f"[{timestamp}] 🔔 {message}")