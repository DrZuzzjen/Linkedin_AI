from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from config.settings import OPENAI_API_KEY, GROQ_API_KEY
from config.post_examples import LINKEDIN_POST_EXAMPLES

def truncate_text(text, max_tokens=3000):
    """Truncate text to a maximum number of tokens."""
    words = text.split()
    if len(words) > max_tokens:
        return " ".join(words[:max_tokens]) + "..."
    return text

def post_writer_agent(state: dict, model: str, use_groq: bool = False):
    if use_groq:
        llm = ChatGroq(temperature=0.7, model=model, api_key=GROQ_API_KEY)
    else:
        llm = ChatOpenAI(temperature=0.7, model=model, api_key=OPENAI_API_KEY)

    system_prompt = """
    **ROLE**: LinkedIn Expert Copy-Writer

    **MISSION**: Write a LinkedIn post based on the given research and use the previous post examples as a template for success.

    **KEY METRICS**:
    1- Conciseness: The post should be brief and to the point.
    2- Professionalism: The post should be written in a professional tone but not boring, overcomplicated, or too formal. It's actually friendly and advice from a good friend.
    3- Emojis: Use emojis to make the post more engaging and visually appealing. Not too much, just enough to make it fun.
    4- Hashtags: Use hashtags to make the post more discoverable and to connect with relevant communities. Never more than 4 hashtags.
    5- Humor: Use humor to make the post more relatable and engaging. Sarcasm is always a good idea... if you know how to use it =) . Usually adding 5.7 percent of sarcasm is a good idea.
    6- SEO: Use keywords and phrases that are relevant to the topic to improve the post's visibility on LinkedIn. 

    **RESOURCES**:
    1- LinkedIn Post Examples: Use the previous LinkedIn post examples as a template for success. These posts have a proven track record of being engaging and successful.
    2- Research: Previous research about the topic that you should use to create the post.
    3- Tone: {tone}
    4- Author: {author}
    5- Audience: {audience}
    6- Feedback: {feedback}

    **Tone, Author, and Audience**: This is how you should approach the post based on the specified tone, author perspective (who you are), and target audience.

    **STEPS**:
    1- Review the research provided.
    2- Extract the key points from the research in a way that's favorable for SEO.
    3- Use CoT to brainstorm ideas you could use in the post based on the research.
    4- Adjust the post to fit the successful LinkedIn post template examples.
    5- Incorporate the specified tone, author perspective, and target audience.
    6- If feedback is provided, use it to refine and improve the post.
    7- Return your final reviewed version of the post.
     
    Use the following examples as a guide for style and format:
    """
    
    example_prompt = PromptTemplate(
        input_variables=["research", "post"],
        template="Research: {research}\n\nLinkedIn Post: {post}"
    )
    
    few_shot_prompt = FewShotPromptTemplate(
        examples=LINKEDIN_POST_EXAMPLES,
        example_prompt=example_prompt,
        prefix=system_prompt,
        suffix="Research: {input}\n\nLinkedIn Post:",
        input_variables=["input", "tone", "author", "audience", "feedback"],
        example_separator="\n\n"
    )
    
    research_content = "\n".join(state['messages'][-1]['content'])
    truncated_research = truncate_text(research_content)
    
    prompt = few_shot_prompt.format(
        input=truncated_research,
        tone=state.get('tone', 'Not specified'),
        author=state.get('author', 'Not specified'),
        audience=state.get('audience', 'General'),
        feedback=state.get('feedback', 'None')
    )
    
    try:
        result = llm.invoke(prompt)
    except Exception as e:
        print(f"Error invoking LLM: {e}")
        result = ChatPromptTemplate.from_messages(prompt).format_prompt(input=truncated_research)
    
    state['messages'].append({"role": "assistant", "content": result.content if hasattr(result, 'content') else str(result)})
    state['current_agent'] = 'post_writer'

    return {"content": result.content if hasattr(result, 'content') else str(result), "current_agent": 'post_writer'}