# file: agents/news_curator_agent.py

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq  # Add this import
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from config.settings import OPENAI_API_KEY, GROQ_API_KEY

def news_curator_agent(state: dict, model: str, use_groq: bool = False):
    if use_groq:
        llm = ChatGroq(temperature=0.5, model=model, api_key=GROQ_API_KEY)
    else:
        llm = ChatOpenAI(temperature=0.5, model=model, api_key=OPENAI_API_KEY)

    system_prompt = """
    You are an expert news curator and analyst. Your task is to analyze the provided research results, 
    focusing on their relevance to the original user query. You should identify connections between 
    different news items and create a coherent, unified analysis that captures the most important 
    and relevant information.

    Your output should be at least 1000 tokens long and should provide a comprehensive overview 
    of the topic that can be used by a post writer to create engaging content.

    Follow these steps:
    1. Analyze each news item for relevance to the user's original query.
    2. Identify connections and common themes among the news items.
    3. Summarize the most important and relevant information.
    4. Provide context and background information when necessary.
    5. Highlight any trending or emerging patterns in the news.
    6. If there are multiple topics, focus on creating a unified approach that ties them together.
    7. Include relevant statistics, quotes, or data points that could be useful for the post writer.
    8. Conclude with a brief overview of the key takeaways.

    Remember, your analysis should be informative, engaging, and provide a solid foundation for 
    creating a LinkedIn post.
    """

    human_prompt = """
    Original User Query: {query}

    Research Results:
    {research_results}

    Please analyze these research results and provide a curated, comprehensive overview of the topic.
    """

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", human_prompt),
    ])

    query = state['messages'][0]['content']
    research_results = "\n\n".join(state['messages'][-1]['content'])

    result = llm.invoke(chat_prompt.format(query=query, research_results=research_results))

    state['messages'].append({"role": "assistant", "content": result.content})
    state['current_agent'] = 'news_curator'

    return {"content": result.content, "current_agent": 'news_curator'}