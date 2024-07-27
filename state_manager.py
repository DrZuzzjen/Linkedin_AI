import streamlit as st
from config.settings import OPENAI_MODELS

def initialize_session_state():
    """Initialize all session state variables."""
    if 'original_post' not in st.session_state:
        st.session_state.original_post = None
    if 'rewritten_post' not in st.session_state:
        st.session_state.rewritten_post = None
    if 'use_groq' not in st.session_state:
        st.session_state.use_groq = False
    if 'model' not in st.session_state:
        st.session_state.model = OPENAI_MODELS[0]
    if 'generated_post' not in st.session_state:
        st.session_state.generated_post = None
    if 'generated_image' not in st.session_state:
        st.session_state.generated_image = None
    if 'post_approved' not in st.session_state:
        st.session_state.post_approved = False
    if 'image_generated' not in st.session_state:
        st.session_state.image_generated = False
    if 'curated_news' not in st.session_state:
        st.session_state.curated_news = None
    if 'rewrite_clicked' not in st.session_state:
        st.session_state.rewrite_clicked = False
    if 'tone' not in st.session_state:
        st.session_state.tone = None
    if 'author' not in st.session_state:
        st.session_state.author = None
    if 'audience' not in st.session_state:
        st.session_state.audience = None
    if 'topic' not in st.session_state:
        st.session_state.topic = ""

def update_session_state(key, value):
    """Update a specific session state variable."""
    st.session_state[key] = value

def reset_session_state():
    """Reset all session state variables to their initial values."""
    initialize_session_state()
    st.session_state.post_generated = False