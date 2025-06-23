import streamlit as st

def tracker_score_filter(threshold: float = 0.75) -> tuple[bool, float]:
    st.sidebar.subheader("Filters")
    best_matches_only = st.sidebar.checkbox("⭐️ Show best matches only", value=False)
    return best_matches_only, threshold