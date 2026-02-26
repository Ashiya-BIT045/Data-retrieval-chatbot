from app.llm_agent import LLMAgent
from app.config import OLLAMA_URL
import logging

import os
print(f"Active OLLAMA_URL: {OLLAMA_URL}")
print(f"HTTP_PROXY: {os.environ.get('HTTP_PROXY')}")
print(f"HTTPS_PROXY: {os.environ.get('HTTPS_PROXY')}")
print(f"NO_PROXY: {os.environ.get('NO_PROXY')}")

# Force no proxy for this test
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'

logging.basicConfig(level=logging.INFO)


agent = LLMAgent()
query = "Software Engineer in Brazil"
result = agent.parse_query(query)
print(f"Query: {query}")
print(f"Result: {result}")
