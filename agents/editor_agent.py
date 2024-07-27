# file: agents/editor_agent.py

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq  # Add this import
from langchain.prompts import ChatPromptTemplate
from config.settings import OPENAI_API_KEY, GROQ_API_KEY
from config.linkedin_knowledge import LINKEDIN_POST_KNOWLEDGE

def editor_agent(state: dict, model: str, use_groq: bool = False):
    if use_groq:
        llm = ChatGroq(temperature=0.7, model=model, api_key=GROQ_API_KEY)
    else:
        llm = ChatOpenAI(temperature=0.7, model=model, api_key=OPENAI_API_KEY)

    system_prompt = f"""
    You are an expert LinkedIn post editor. Your task is to refine and optimize the given post for 
    maximum engagement on LinkedIn. Use the following knowledge to guide your edits:

    {LINKEDIN_POST_KNOWLEDGE}

    Your primary goals are:
    1. Ensure the post follows LinkedIn best practices.
    2. Make the content more engaging and shareable.
    3. Keep the post under 2800 characters, and ideally even shorter.
    4. Maintain the original message and key points while improving the delivery.
    5. Add appropriate hashtags if they're missing.
    6. Ensure there's a compelling hook and a clear call-to-action.

    Remember, your edits should enhance the post's effectiveness on LinkedIn while preserving its 
    core message and authenticity.

    This Original Post submitted by an expert copywriter agent has been provided for your review.
   
   
    ***IMPORTANT***:
    -Your refined version of the  post will be the direct output to the LinkedIn Post Agent for final posting so do not include anything else by the post itelsf. Do not include any remarks or comments in the post.
    -Do not sound like a bot, or generic. you are a human and you are talking to humans.

    **OUTPUT FORMAT**:
    -Title:
    -Post
    -Hashtags
    """

    human_prompt = """
    Original LinkedIn Post:
    {original_post}

    Please edit and refine this post for LinkedIn, following the guidelines provided.
    """

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", human_prompt),
    ])

    original_post = state['messages'][-1]['content']

    result = llm.invoke(chat_prompt.format(original_post=original_post))

    state['messages'].append({"role": "assistant", "content": result.content})
    state['current_agent'] = 'editor'

    return {"content": result.content, "current_agent": 'editor'}