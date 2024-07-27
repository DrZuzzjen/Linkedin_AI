import streamlit as st
import time
from agents.post_illustrator_agent import post_illustrator_agent
from state_manager import update_session_state

def generate_image():
    if st.session_state.generated_post:
        start_time = time.time()
        with st.spinner("Creating Image..."):
            illustration_result = post_illustrator_agent({"content": st.session_state.generated_post})
        illustration_time = time.time() - start_time
        st.text(f"Image created in {illustration_time:.2f} seconds")
        
        update_session_state('generated_image', illustration_result['image_path'])
        update_session_state('image_generated', True)
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

def save_image(image_path):
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as file:
            btn = st.download_button(
                label="Save Image",
                data=file,
                file_name="linkedin_post_image.png",
                mime="image/png"
            )