import json
import re
import requests
import os
from jinja2 import Environment, FileSystemLoader

from .config import OLLAMA_URL, OLLAMA_MODEL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMAgent:
    def __init__(self):
        # Use absolute path to avoid issues with current working directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompts_dir = os.path.join(base_dir, "prompts")
        self.env = Environment(loader=FileSystemLoader(prompts_dir))
        self.template = self.env.get_template('extract_parameters.jinja2')


    def parse_query(self, query: str):
        prompt = self.template.render(query=query)
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            raw_output = response.json().get("response", "")
            logger.info(f"Raw LLM output: {raw_output}")
            return self._extract_json(raw_output)
        except Exception as e:
            logger.error(f"Error calling LLM: {e}", exc_info=True)
            return {"occupation": None, "field": None, "city": None, "country": None, "reasoning": f"Error communicating with LLM: {str(e)}"}


    def _extract_json(self, text: str):
        # 1. Basic cleanup
        text = text.strip()
        
        # 2. Extract JSON block if surrounded by other text
        match = re.search(r"(\{.*\})", text, re.DOTALL)
        if match:
            text = match.group(1)

        # 3. Robust fix for common local model error: missing commas
        # This matches a quoted value followed by whitespace and then another field name
        text = re.sub(r'("(?:[^"\\]|\\.)*")\s*\n?\s*(")', r'\1,\2', text)
        
        # 4. Handle nulls without quotes if model returns them (unlikely but safe)
        text = re.sub(r':\s*null\s*\n?\s*(")', r': null,\1', text)

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing failed after cleanup effort: {e}. Raw text: {text}")
            return {"occupation": None, "field": None, "city": None, "country": None, "reasoning": "Could not parse Agent reasoning accurately."}
