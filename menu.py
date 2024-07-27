# menu.py

import streamlit as st
import os
from config.settings import OPENAI_MODELS, GROQ_MODELS
from config.settings import (
    OPENAI_API_KEY,
    TAVILY_API_KEY,
    GROQ_API_KEY,
    OPENAI_MODELS,
    GROQ_MODELS
)
from config.post_examples import LINKEDIN_POST_EXAMPLES

def setup_sidebar():
    st.sidebar.title("Setup Options")
    setup_environment_variables()
    setup_model_selection()
    setup_post_examples()
    setup_settings_lock()

def setup_environment_variables():
    st.sidebar.header("Environment Variables")
    
    openai_api_key = st.sidebar.text_input("OpenAI API Key", value=OPENAI_API_KEY or "", type="password")
    tavily_api_key = st.sidebar.text_input("Tavily API Key", value=TAVILY_API_KEY or "", type="password")
    groq_api_key = st.sidebar.text_input("Groq API Key", value=GROQ_API_KEY or "", type="password")
    
    # Update session state
    st.session_state.openai_api_key = openai_api_key
    st.session_state.tavily_api_key = tavily_api_key
    st.session_state.groq_api_key = groq_api_key
    
    # Update session state and environment variables
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        os.environ["OPENAI_API_KEY"] = openai_api_key
    if tavily_api_key:
        st.session_state.tavily_api_key = tavily_api_key
        os.environ["TAVILY_API_KEY"] = tavily_api_key
    if groq_api_key:
        st.session_state.groq_api_key = groq_api_key
        os.environ["GROQ_API_KEY"] = groq_api_key

def setup_model_selection():
    st.session_state.use_groq = st.sidebar.checkbox("Use Groq", value=st.session_state.get("use_groq", False))
    if st.session_state.use_groq:
        st.session_state.model = st.sidebar.selectbox("Select Groq Model", GROQ_MODELS, index=GROQ_MODELS.index(st.session_state.model) if st.session_state.model in GROQ_MODELS else 0)
    else:
        st.session_state.model = st.sidebar.selectbox("Select OpenAI Model", OPENAI_MODELS, index=OPENAI_MODELS.index(st.session_state.model) if st.session_state.model in OPENAI_MODELS else 0)

def setup_post_examples():
    st.sidebar.header("Post Examples")
    post_examples = st.sidebar.text_area("Enter new post example", height=150)
    if st.sidebar.button("Add Example"):
        LINKEDIN_POST_EXAMPLES.append({"research": "Example Research", "post": post_examples})
        st.sidebar.success("Example added successfully!")

def setup_settings_lock():
    if st.sidebar.button("Save and Lock Settings"):
        st.sidebar.success("Settings saved and locked!")

    if st.sidebar.button("Unlock Settings"):
        st.sidebar.info("Settings unlocked!")