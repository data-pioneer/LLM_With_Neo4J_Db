# configuration.py
import os
from dotenv import load_dotenv

def load_environment_variables():
    load_dotenv()
    return {
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
        "HF_TOKEN": os.getenv("HF_TOKEN"),
        "NEO4J_URI": os.getenv("NEO4J_URI"),
        "NEO4J_USERNAME": os.getenv("NEO4J_USERNAME"),
        "NEO4J_PASSWORD":os.getenv("NEO4J_PASSWORD")

    }
