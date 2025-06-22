import streamlit as st
from backend.dashboard import get_all_applications_ordered_by_date_created
from app.components.db import get_db_connection

st.set_page_config(page_title="📋 Job Tracker", layout="wide")
st.title("📋 Job Application Tracker")

# Step 1: DB connection
db = get_db_connection()

# Step 2: Load applications
applications = get_all_applications_ordered_by_date_created(db)

# Step 3: Display 
if not applications:
    st.info("No applications saved yet")
else:
    for app in applications:
        with st.container():
            st.markdown(f"### {app['job_title']} at {app['company_name']}")
            st.markdown(f"📍 {app['location']} &nbsp;&nbsp; ⭐️ {app['match_score']:.2f}")
            st.markdown(f"🕒 Applied on: {app['created_at']}")
            st.divider()