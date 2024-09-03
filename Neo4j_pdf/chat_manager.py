from langchain_community.chat_message_histories import ChatMessageHistory
from neo4j_handler import Neo4jHandler

def get_session_history(session_id, store, neo4j_handler):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
        neo4j_handler.create_session(session_id)
    return store[session_id]

def store_chat_message(neo4j_handler, session_id, message_type, content):
    from datetime import datetime
    timestamp = datetime.now().isoformat()
    neo4j_handler.add_chat_message(session_id, message_type, content, timestamp)
