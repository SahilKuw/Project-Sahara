from dotenv import load_dotenv
import os

load_dotenv()

llm_api_key = os.getenv("LLM_API_KEY")

print(llm_api_key)
