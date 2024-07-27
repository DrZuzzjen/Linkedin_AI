import streamlit as st

def render_linkedin_post(content, image_path=None):
    st.markdown(
        f"""
        <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
            <p style="font-family: Arial, sans-serif; font-size: 14px;">{content}</p>
            {'<img src="' + image_path + '" style="max-width: 100%; height: auto;">' if image_path else ''}
        </div>
        """,
        unsafe_allow_html=True
    )