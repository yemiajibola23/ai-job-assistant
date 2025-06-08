def get_alert_status_message(is_enabled: bool) -> str:
    return "✅ Alerts are ON" if is_enabled else "🔕 Alerts are OFF"