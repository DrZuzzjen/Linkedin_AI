import streamlit as st

def render_linkedin_post(content, image_path=None):
   approval_icon = "✅" if st.session_state.post_approved else "⚪"
   st.markdown(f"""
    <div style="border: 1px solid var(--streamlit-color-secondary-50); border-radius: 8px; padding: 16px; max-width: 100%; margin: auto; background-color: var(--streamlit-color-white);">
        <div style="display: flex; align-items: center; margin-bottom: 12px;">
            <img src="https://images.ctfassets.net/2djrn56blv6r/mUI70ztjYTCXRWTLJyBJz/a9024aab73eb1f2718c138337d977415/bringing-dog-to-office-header.jpg" style="border-radius: 50%; width: 40px; height: 40px; margin-right: 8px;">
            <div>
                <div style="font-weight: bold; color: var(--streamlit-color-body-text);">{approval_icon}</div>
                <div style="color: var(--streamlit-color-secondary-text); font-size: 0.8em;">AI Post Generator • 1d</div>
            </div>
        </div>
        <p style="margin-bottom: 16px; white-space: pre-wrap; color: var(--streamlit-color-body-text); max-height: 300px; overflow-y: auto;">{content}</p>
        {'<img src="' + image_path + '" style="max-width: 100%; height: auto;">' if image_path else ''}
    </div>
    """, unsafe_allow_html=True)
    
    
st.markdown("""
    <div style="display: flex; justify-content: space-between; color: var(--streamlit-color-secondary-text); max-width: 552px; margin: auto;">
        <span>👍 Like</span>
        <span>💬 Comment</span>
        <span>🔁 Repost</span>
        <span>📤 Send</span>
    </div>
    """, unsafe_allow_html=True)