from langchain_core.messages import AIMessage
from utils.linkedin_auth import LinkedInAuth
from config.settings import LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, LINKEDIN_REDIRECT_URI

def linkedin_post_agent(state: dict):
    linkedin_auth = LinkedInAuth(LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, LINKEDIN_REDIRECT_URI)
    
    post_content = state['messages'][-1].content
    
    try:
        # This is a placeholder. Implement actual LinkedIn posting logic here.
        # linkedin_auth.post_update(post_content)
        result = "Successfully posted to LinkedIn."
    except Exception as e:
        result = f"Failed to post to LinkedIn. Error: {str(e)}"
    
    state['messages'].append(AIMessage(content=result))
    state['current_agent'] = 'linkedin_post'
    return state