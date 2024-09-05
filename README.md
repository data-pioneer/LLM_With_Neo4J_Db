# login into Neo4j Db 

## Create Virtual environment 
conda create -n langhainVenv python=3.10 -y

conda activate langhainVenv

pip install -r requirements.txt 

##  Store Wikipedia page as Nodes and Relationship inside Neo4j DB 
- app.py : User interface for initalize another variables and communaite with user. 
- Configuration.py : It loads the environment variables. 
- database.py : Initilize neo4j database driver and made connection. 
- ResponseGenerator : split the input into documents for model undersatnding. 
- DataRetriever : This class retrive data from Neo4j db. It is perform embedding, vector search and then finally perform similarity search to extract answer. 
- LLMTransformer : This class will convert user entered wikipedia page in graph format, which futher store into Neo4j Db. 
- WikipediaHandler.py : This class fetch data from Wikipedia page and then split into document.
  
![Screenshot 2024-09-04 120609](https://github.com/user-attachments/assets/414caa50-65e8-455d-9ebe-365f2931ecf4)

![Screenshot 2024-09-05 115417](https://github.com/user-attachments/assets/af78b04d-32ab-483e-ae13-f610f3d9a1c5)

## Store user selected PDF file into Neo4j DB 
- app.py : streamlit interface for user connectivity and calling subclasses. 
- chat_manager : it stores session and message history. 
- config.py : read all environment variables. 
- document_handler.py : This class process the user selected pdf and store it into Neo4j db.
- embedding_store.py : This class perform embedding and vector store on pdf file.
- neo4j_handler.py : This class perform various operation related to Neo4j DB. 
- rag_chain.py : implementaion of rag pipeline for data retriver.

 ![Screenshot 2024-09-04 121938](https://github.com/user-attachments/assets/1d300e6e-ff28-45b3-98ab-9e55baeddf91)



 


