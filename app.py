import streamlit as st
from PIL import Image
from dotenv import load_dotenv

from state_manager import initialize_session_state, update_session_state
from components.linkedin_post_display import render_linkedin_post
from components.personalization_inputs import render_personalization_inputs
from services.post_generation_service import generate_post, rewrite_post
from services.image_generation_service import generate_image, display_image
from menu import setup_sidebar

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="LinkedIn Post Generator", layout="wide")

# Initialize session state
initialize_session_state()

# Set up the sidebar
setup_sidebar()

# Main content
st.title("LinkedIn Post Generator")

def copy_to_clipboard(text):
    pyperclip.copy(text)
    st.success("Post copied to clipboard!")

# Input area
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
            update_session_state('post_approved', True)
            st.success("Post approved!")
    with col2:
        if st.button("Re-write Post", key="rewrite_post_button"):
            update_session_state('rewrite_clicked', True)
    with col3:
        if st.button("Restart", key="restart_button"):
            initialize_session_state()
            st.experimental_rerun()

    if st.session_state.rewrite_clicked:
        feedback = st.text_area("Provide feedback or suggestions for improvement:")
        if st.button("Submit Feedback", key="submit_feedback_button"):
            rewrite_post(feedback)
            update_session_state('rewrite_clicked', False)
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