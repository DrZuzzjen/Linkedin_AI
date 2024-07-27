import streamlit as st
from state_manager import update_session_state

def render_personalization_inputs():
    st.subheader("Personalize Your Post")
    
    tone_options = ["", "Humor", "Inspirational", "Celebration", "Achievement"]
    selected_tone = st.selectbox("Select a tone:", tone_options, key="tone_select")
    custom_tone = st.text_input("Or enter a custom tone:", key="custom_tone")
    author = st.text_input("Enter your role (e.g., Student, Software Dev, English Teacher):", key="author_input")
    audience = st.text_input("Enter your target audience:", key="audience_input")

    update_session_state('tone', custom_tone if custom_tone else selected_tone)
    update_session_state('author', author)
    update_session_state('audience', audience)