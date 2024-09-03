# database.py
from neo4j import GraphDatabase

class Neo4jDatabase:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # Add more database-related methods as needed
