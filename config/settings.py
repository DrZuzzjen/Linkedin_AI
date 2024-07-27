import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
LINKEDIN_REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI')
POST_TIME_24HS = int(os.getenv('POST_TIME_24HS', 8))
HUMAN_REVIEW = os.getenv('HUMAN_REVIEW', 'True').lower() == 'true'
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LANGCHAIN_TRACING_V2 = True
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")

OPENAI_MODELS = [
    "gpt-4o",
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo",

    # ... other OpenAI models
]

GROQ_MODELS = [
      "llama3-70b-8192",
      "llama-3.1-70b-versatile",
      "llama3-groq-70b-8192-tool-use-preview",
      "llama-3.1-405b-reasoning",

    ]

