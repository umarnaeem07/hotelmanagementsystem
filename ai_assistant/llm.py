from langchain_openai import ChatOpenAI
from django.conf import settings

llm = ChatOpenAI(
    model="deepseek/deepseek-chat-v3-0324",
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)