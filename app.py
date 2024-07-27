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
if 'tone' not in st.session_state:
    st.session_state.tone = None
if 'author' not in st.session_state:
    st.session_state.author = None
if 'audience' not in st.session_state:
    st.session_state.audience = None    


def set_tone(tone):
    st.session_state.tone = tone

# Set up the sidebar
setup_sidebar()

# Main content
st.title("LinkedIn Post Generator")

# Define functions
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
            if st.button("🔄", key="regenerate_image"):
                generate_image()
        save_image(st.session_state.generated_image)
    else:
        st.error("No image generated yet.")

def generate_post():
    if st.session_state.topic:
        if 'research_results' not in st.session_state:
            st.info("Researching and curating content... This may take a moment.")

            # Research step
            start_time = time.time()
            with st.spinner("Researching topic..."):
                research_results = research_agent({"messages": [{"content": st.session_state.topic}]}, model=st.session_state.model)
            st.session_state.research_time = time.time() - start_time
            st.text(f"Research completed in {st.session_state.research_time:.2f} seconds")

            # News Curation step
            start_time = time.time()
            with st.spinner("Curating and analyzing news..."):
                curated_results = news_curator_agent(research_results, model=st.session_state.model, use_groq=st.session_state.use_groq)
            st.session_state.curation_time = time.time() - start_time
            st.text(f"News curated and analyzed in {st.session_state.curation_time:.2f} seconds")    
            st.session_state.curated_news = curated_results['content']
            st.session_state.research_results = research_results
            st.session_state.show_personalization = True
            st.experimental_rerun()

        if st.session_state.get('show_personalization', False):
            # Personalization inputs
            st.subheader("Personalize Your Post")
            
            tone_options = ["", "Humor", "Inspirational", "Celebration", "Achievement"]
            selected_tone = st.selectbox("Select a tone:", tone_options, key="tone_select")
            custom_tone = st.text_input("Or enter a custom tone:", key="custom_tone")
            author = st.text_input("Enter your role (e.g., Student, Software Dev, English Teacher):", key="author_input")
            audience = st.text_input("Enter your target audience:", key="audience_input")

            if st.button("Generate Personalized Post", key="generate_personalized_post"):
                # Writing step
                start_time = time.time()
                with st.spinner("Writing post..."):
                    post_result = post_writer_agent(
                        {
                            "messages": [{"content": st.session_state.curated_news}],
                            "tone": custom_tone if custom_tone else selected_tone,
                            "author": author,
                            "audience": audience
                        },
                        model=st.session_state.model,
                        use_groq=st.session_state.use_groq
                    )
                st.session_state.writing_time = time.time() - start_time
                st.text(f"Post written in {st.session_state.writing_time:.2f} seconds")

                # Editing step
                start_time = time.time()
                with st.spinner("Editing and optimizing post for LinkedIn..."):
                    edited_result = editor_agent({"messages": [{"content": post_result['content']}]}, model=st.session_state.model, use_groq=st.session_state.use_groq)
                st.session_state.editing_time = time.time() - start_time
                st.text(f"Post edited and optimized in {st.session_state.editing_time:.2f} seconds")

                # Store the original post content
                st.session_state.original_post = edited_result['content']
                st.session_state.generated_post = edited_result['content']
                st.session_state.rewritten_post = None  # Reset rewritten post
            
                st.success("Post generated successfully!")
                st.session_state.post_generated = True
                st.session_state.show_personalization = False  # Hide personalization after generating
                st.experimental_rerun()

    else:
        st.warning("Please enter a topic before generating a post.")

def rewrite_post(feedback=""):
    if st.session_state.curated_news:
        st.info("Rewriting post... This may take a moment.")

        # Update the query with feedback
        updated_query = f"{st.session_state.topic} FEEDBACK: {feedback}" if feedback else st.session_state.topic

        # Writing step
        start_time = time.time()
        with st.spinner("Writing post..."):
            post_result = post_writer_agent(
                {
                    "messages": [{"content": st.session_state.curated_news}, {"content": updated_query}],
                    "tone": st.session_state.tone,
                    "author": st.session_state.author,
                    "audience": st.session_state.audience,
                    "feedback": feedback
                },
                model=st.session_state.model,
                use_groq=st.session_state.use_groq
            )
        st.session_state.writing_time = time.time() - start_time
        st.text(f"Post rewritten in {st.session_state.writing_time:.2f} seconds")

        # Editing step
        start_time = time.time()
        with st.spinner("Editing and optimizing post for LinkedIn..."):
            edited_result = editor_agent({"messages": [{"content": post_result['content']}]}, model=st.session_state.model, use_groq=st.session_state.use_groq)
        st.session_state.editing_time = time.time() - start_time
        st.text(f"Post edited and optimized in {st.session_state.editing_time:.2f} seconds")
       
        # Store the rewritten post content
        st.session_state.rewritten_post = edited_result['content']
        
        st.success("Post rewritten successfully!")
        st.session_state.post_generated = True
        st.experimental_rerun()
    else:
        st.error("No curated news available. Please generate a post first.")


def reset_app():
    keys_to_clear = [
        'topic', 'generated_post', 'rewritten_post', 'generated_image', 
        'post_approved', 'image_generated', 'curated_news', 'rewrite_clicked', 
        'tone', 'custom_tone', 'author', 'audience', 'research_results'
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.post_generated = False
    st.experimental_rerun()

def approve_post():
    st.session_state.post_approved = True

# Input area
if 'topic' not in st.session_state:
    st.session_state.topic = ""

st.session_state.topic = st.text_input("Enter the topic for your LinkedIn post:", 
                                       value=st.session_state.topic, 
                                       placeholder="e.g., Latest trends in AI")

if st.button("Start Post Generation", key="start_generation"):
    generate_post()

if 'research_results' in st.session_state:
    generate_post()

if st.session_state.get('post_generated', False):
    # Display generated post and image
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

    # Human Review section
    st.subheader("Human Review")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Approve Post", key="approve_post_button"):
            approve_post()
            st.success("Post approved!")
    with col2:
        if st.button("Re-write Post", key="rewrite_post_button"):
            st.session_state.rewrite_clicked = True
    with col3:
        if st.button("Restart", key="restart_button"):
            reset_app()

    if st.session_state.rewrite_clicked:
        feedback = st.text_area("Provide feedback or suggestions for improvement:")
        if st.button("Submit Feedback", key="submit_feedback_button"):
            rewrite_post(feedback)
            st.session_state.rewrite_clicked = False
            st.experimental_rerun()

    # Image generation button
    if st.session_state.post_approved:
        if st.button("Generate Image", key="generate_image_button"):
            generate_image()

    # Display generated image and regenerate option
    if st.session_state.image_generated:
        display_image()

# Run the Streamlit app
if __name__ == "__main__":
    pass  # Main logic is handled by Streamlit