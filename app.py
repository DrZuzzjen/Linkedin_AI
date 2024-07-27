import streamlit as st
import os
import time
import pyperclip
from PIL import Image
from dotenv import load_dotenv
from langchain_groq import ChatGroq  # Add Groq import
from agents.research_agent import research_agent
from agents.post_writer_agent import post_writer_agent
from agents.post_illustrator_agent import post_illustrator_agent
from agents.linkedin_post_agent import linkedin_post_agent
from agents.news_curator_agent import news_curator_agent
from agents.editor_agent import editor_agent
from menu import setup_sidebar
from config.settings import (
    OPENAI_API_KEY,
    TAVILY_API_KEY,
    GROQ_API_KEY,
    OPENAI_MODELS,
    GROQ_MODELS
)
from config.post_examples import LINKEDIN_POST_EXAMPLES
from config.linkedin_post_layout import render_linkedin_post
from utils.database import Database


# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="LinkedIn Post Generator", layout="wide")

# Initialize session state
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


# Set up the sidebar
setup_sidebar()

# Main content
st.title("LinkedIn Post Generator")


# Input area
if 'post_generated' not in st.session_state or not st.session_state.post_generated:
    topic = st.text_input("Enter the topic for your LinkedIn post:", placeholder="e.g., Latest trends in AI")
else:
    feedback = st.text_input("Feedback for post rewrite:", placeholder="Enter feedback for post improvement")

# Button row
col1, col2, col3 = st.columns(3)
with col1:
    generate_button = st.button("Generate Post", disabled='post_generated' in st.session_state and st.session_state.post_generated)
with col2:
    rewrite_button = st.button("Re-write Post", disabled='post_generated' not in st.session_state or not st.session_state.post_generated)
with col3:
    restart_button = st.button("Restart", disabled='post_generated' not in st.session_state or not st.session_state.post_generated)

if generate_button:
    generate_post()

if rewrite_button:
    rewrite_post(feedback)

if restart_button:
    reset_app()    

def copy_to_clipboard(text):
    pyperclip.copy(text)
    st.success("Post copied to clipboard!")

def save_image(image_path):
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as file:
            btn = st.download_button(
                label="Save Image",
                data=file,
                file_name="linkedin_post_image.png",
                mime="image/png"
            )

def generate_image():
    if st.session_state.generated_post:
        start_time = time.time()
        with st.spinner("Creating Image..."):
            illustration_result = post_illustrator_agent({"content": st.session_state.generated_post})
        illustration_time = time.time() - start_time
        st.text(f"Image created in {illustration_time:.2f} seconds")
        
        st.session_state.generated_image = illustration_result['image_path']
        st.session_state.image_generated = True
    else:
        st.error("No post content available for image generation.")

def display_image():
    if 'generated_image' in st.session_state and st.session_state.generated_image:
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.image(st.session_state.generated_image)
        with col2:
            if st.button("🔄"):
                generate_image()
        save_image(st.session_state.generated_image)
    else:
        st.error("No image generated yet.")

def generate_post():
    if topic:
        st.info("Generating post... This may take a moment.")

        # Research step
        start_time = time.time()
        with st.spinner("Researching topic..."):
            research_results = research_agent({"messages": [{"content": topic}]}, model=st.session_state.model)
        research_time = time.time() - start_time
        st.text(f"Research completed in {research_time:.2f} seconds")

        # News Curation step
        start_time = time.time()
        with st.spinner("Curating and analyzing news..."):
            curated_results = news_curator_agent(research_results, model=st.session_state.model, use_groq=st.session_state.use_groq)
        curation_time = time.time() - start_time
        st.text(f"News curated and analyzed in {curation_time:.2f} seconds")    
        st.session_state.curated_news = curated_results['content']

        # Writing step
        start_time = time.time()
        with st.spinner("Writing post..."):
            post_result = post_writer_agent({"messages": [{"content": curated_results['content']}]}, model=st.session_state.model, use_groq=st.session_state.use_groq)
        writing_time = time.time() - start_time
        st.text(f"Post written in {writing_time:.2f} seconds")

        # Editing step
        start_time = time.time()
        with st.spinner("Editing and optimizing post for LinkedIn..."):
            edited_result = editor_agent({"messages": [{"content": post_result['content']}]}, model=st.session_state.model, use_groq=st.session_state.use_groq)
        editing_time = time.time() - start_time
        st.text(f"Post edited and optimized in {editing_time:.2f} seconds")

        # Store the original post content
        st.session_state.original_post = edited_result['content']
        st.session_state.generated_post = edited_result['content']
        st.session_state.rewritten_post = None  # Reset rewritten post
    
        st.success("Post generated successfully!")
        st.session_state.post_generated = True

def rewrite_post(feedback=""):
    if st.session_state.curated_news:
        st.info("Rewriting post... This may take a moment.")

        # Update the query with feedback
        updated_query = f"{topic} FEEDBACK: {feedback}" if feedback else topic

        # Writing step
        start_time = time.time()
        with st.spinner("Writing post..."):
            post_result = post_writer_agent({"messages": [{"content": st.session_state.curated_news}, {"content": updated_query}]}, model=st.session_state.model, use_groq=st.session_state.use_groq)
        writing_time = time.time() - start_time
        st.text(f"Post rewritten in {writing_time:.2f} seconds")

        # Editing step
        start_time = time.time()
        with st.spinner("Editing and optimizing post for LinkedIn..."):
            edited_result = editor_agent({"messages": [{"content": post_result['content']}]}, model=st.session_state.model, use_groq=st.session_state.use_groq)
        editing_time = time.time() - start_time
        st.text(f"Post edited and optimized in {editing_time:.2f} seconds")
       
        # Store the rewritten post content
        st.session_state.rewritten_post = edited_result['content']
        st.session_state.writing_time = writing_time
        st.session_state.editing_time = editing_time
        
        st.success("Post rewritten successfully!")
        st.session_state.post_generated = True

def reset_app():
    for key in ['generated_post', 'rewritten_post', 'generated_image', 'post_approved', 'image_generated', 'curated_news', 'rewrite_clicked']:
        if key in st.session_state:
            del st.session_state[key]
    st.experimental_rerun()

if st.button("Generate Post"):
    generate_post()
    
# Add a function to handle post approval:
def approve_post():
    st.session_state.post_approved = True

# Display generated post and image
if 'post_generated' in st.session_state and st.session_state.post_generated:
    st.subheader("Generated LinkedIn Post:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Original Post " + ("✅" if st.session_state.post_approved else "⚪"))
        render_linkedin_post(st.session_state.generated_post, None)
    with col2:
        if st.session_state.rewritten_post:
            st.markdown("### Rewritten Post " + ("✅" if st.session_state.post_approved else "⚪"))
            render_linkedin_post(st.session_state.rewritten_post, None)
        else:
            st.markdown("### Rewritten Post")
            st.write("No rewrite yet. Use the 'Re-write Post' button to generate a new version.")

     # Display process timings
    st.subheader("Process Timings:")
    st.text(f"Research completed in {st.session_state.research_time:.2f} seconds")
    st.text(f"News curated and analyzed in {st.session_state.curation_time:.2f} seconds")
    st.text(f"Post written in {st.session_state.writing_time:.2f} seconds")
    st.text(f"Post edited and optimized in {st.session_state.editing_time:.2f} seconds")        

    # Human review process
    st.subheader("Human Review")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Approve Post"):
            st.session_state.post_approved = True
            st.success("Post approved!")
    with col2:
        if st.button("Re-write Post"):
            st.session_state.rewrite_clicked = True
    with col3:
        if st.button("Restart"):
            reset_app()

    if st.session_state.rewrite_clicked:
        feedback = st.text_area("Provide feedback or suggestions for improvement:")
        if st.button("Submit Feedback"):
            rewrite_post(feedback)
            st.session_state.rewrite_clicked = False
            st.experimental_rerun()

    if st.session_state.post_approved:
        if st.button("Generate Image"):
            generate_image()

    # Display generated image and regenerate option
    if st.session_state.image_generated:
        display_image()

# Run the Streamlit app
if __name__ == "__main__":
    pass  # Main logic is handled by Streamlit