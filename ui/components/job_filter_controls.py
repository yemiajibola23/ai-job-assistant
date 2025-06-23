import streamlit as st
from backend.utils.constants import DEFAULT_SCORE_THRESHOLD

def tracker_score_filter(threshold: float = DEFAULT_SCORE_THRESHOLD) -> tuple[bool, float]:
    st.sidebar.subheader("Filters")
    best_matches_only = st.sidebar.checkbox("⭐️ Show best matches only", value=False)
    return best_matches_only, threshold