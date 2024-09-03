from neo4j import GraphDatabase

class Neo4jHandler:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_document(self, file_name, content):
        with self.driver.session() as session:
            session.write_transaction(self._create_document_node, file_name, content)

    @staticmethod
    def _create_document_node(tx, file_name, content):
        tx.run("MERGE (d:Document {name: $file_name}) "
               "ON CREATE SET d.content = $content", 
               file_name=file_name, content=content)

    def add_chat_message(self, session_id, message_type, content, timestamp):
        with self.driver.session() as session:
            session.write_transaction(self._create_chat_node, session_id, message_type, content, timestamp)

    @staticmethod
    def _create_chat_node(tx, session_id, message_type, content, timestamp):
        tx.run("MATCH (s:Session {id: $session_id}) "
               "MERGE (m:Message {type: $message_type, content: $content, timestamp: $timestamp}) "
               "MERGE (s)-[:HAS_MESSAGE]->(m)", 
               session_id=session_id, message_type=message_type, content=content, timestamp=timestamp)

    def create_session(self, session_id):
        with self.driver.session() as session:
            session.write_transaction(self._create_session_node, session_id)

    @staticmethod
    def _create_session_node(tx, session_id):
        tx.run("MERGE (s:Session {id: $session_id})", session_id=session_id)
