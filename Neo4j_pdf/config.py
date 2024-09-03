import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")
    os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
    os.environ['NEO4J_URI'] = os.getenv("NEO4J_URI")
    os.environ['NEO4J_USERNAME'] = os.getenv("NEO4J_USERNAME")
    os.environ['NEO4J_PASSWORD'] = os.getenv("NEO4J_PASSWORD")
  
