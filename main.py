import streamlit as st
from app.ui_helpers import get_alert_status_message

enabled = st.checkbox("Enable Alerts")
st.write(get_alert_status_message(enabled))