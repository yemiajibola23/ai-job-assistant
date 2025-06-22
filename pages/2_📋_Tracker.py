import streamlit as st
from backend.dashboard import get_all_applications_ordered_by_date_created
from app.components.tracker_filters import tracker_score_filter
from backend.db.application_dao import update_application_status_and_notes
from app.components.db import get_db_connection

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
    status_options = ["Interested", "Applied", "Interviewing", "Rejected", "Offer"]
    for app in applications:
        # st.write(app)
        with st.container():
            st.markdown(f"### {app['job_title']} at {app['company_name']}")
            st.markdown(f"📍 {app['location']} &nbsp;&nbsp; ⭐️ {app['match_score']:.2f}")
            st.markdown(f"🕒 Applied on: {app['created_at']}")
            
            new_status =  st.selectbox("Select status",
                                       options=status_options,
                                       index=status_options.index(app['status']) if app['status'] in status_options else 0, 
                                       key=f"status-{app['id']}"
                                       )
            new_notes = st.text_area("Notes", value=app['notes'] or "", key=f"notes-{app['id']}")
            
            
            if st.button("Save", key=f"save-{app['id']}"):
                update_application_status_and_notes(db, app["id"], new_status, new_notes)
            
            st.divider()