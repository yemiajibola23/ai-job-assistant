from ui.components.ui_helpers import get_alert_status_message

def test_get_alert_status_message():
    assert get_alert_status_message(True) == "✅ Alerts are ON"
    assert get_alert_status_message(False) == "🔕 Alerts are OFF"