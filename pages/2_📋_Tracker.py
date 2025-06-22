import streamlit as st
from backend.dashboard import get_all_applications_ordered_by_date_created
from app.components.db import get_db_connection
from app.components.tracker_filters import tracker_score_filter

st.set_page_config(page_title="📋 Job Tracker", layout="wide")
st.title("📋 Job Application Tracker")

best_matches_only, threshold = tracker_score_filter()

db = get_db_connection()
applications = get_all_applications_ordered_by_date_created(db)

if best_matches_only:
    applications = [app for app in applications if app["match_score"] >= threshold]

# st.write("🧪 DEBUG SAMPLE ROW:", applications[0])

if not applications:
    st.info("No applications saved yet")
else:
    for app in applications:
        with st.container():
            st.markdown(f"### {app['job_title']} at {app['company_name']}")
            st.markdown(f"📍 {app['location']} &nbsp;&nbsp; ⭐️ {app['match_score']:.2f}")
            st.markdown(f"🕒 Applied on: {app['created_at']}")
            st.divider()