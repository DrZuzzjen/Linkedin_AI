from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from config.settings import TAVILY_API_KEY

def research_agent(state: dict, model: str):
    tavily_tool = TavilySearchResults(max_results=5, api_key=TAVILY_API_KEY)
    
    query = state['messages'][-1]['content']
    results = tavily_tool.run(query)
    
    # Extract just the content from each result
    answer_contents = [result['content'] for result in results]
    
    state['messages'].append({"role": "assistant", "content": answer_contents})
    state['current_agent'] = 'research'
    return state