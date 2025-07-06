# Fullstack-RAG

Source - https://www.youtube.com/watch?v=vEGqCleTHfM

I did a quick follow through of the tutorial in the yt to learn how to connect frontend with backend, and jotted down few pointers on env setup. 

backend - fastapi python
frontend - react+js


Steps to setup the env(MacOS)

- Poetry for package and env management
  
    - Install poetry
      
            brew install poetry
    - To add the homebrews curl path,as the version of curl provided by macOS might be old or missing some features. Poetry (or another dependency) likely requires a newer version. So Homebrew is suggesting:
      
            echo 'export PATH="/opt/homebrew/opt/curl/bin:$PATH"' >> ~/.zshrc
            source ~/.zshrc (to reload the shell config)
    - Initialize poetry
      
            poetry init
        This will create file poetry.toml file
    - To add dependencies
      
            poetry add fastapi
        This will create a .venv file with the dependencies installed.
        For me it installed in a different folder, hence I had to delete the existing env and set the config to create venv in my folder using the follwoing command.
      
                poetry config virtualenvs.in-project true
    - To activate the env
 
            poetry env list --full-path
            source [use the path output]/bin/activate (or)
            source .venv/bin/activate
    - To deactivate
      
            deacivate
    
Fastapi gives logic to define the API, we need web servers to run the API, which gonna handle actual protocol requests and responses, there are many frameworks for web servers in python, we have used uvicorn. 
    - To install uvicorn
    
        poetry add uvicorn
To work on RAG, we are using qdrant for vectorestore and langchain for RAG logic
    - To install qdrant and langchain
    
        poetry add langchain qdrant-client

To access API keys and qdrant cluster url in .py files from .env, decouple is used

    - poetry add python-decouple

To run the fastapi app

    uvicorn src.app:app --reload

To view the documentation of the API, we can access the url 

    http://127.0.0.1:8000/docs

Issues and solutions:

In rag.py file, to import qdrant file vector_store, I have used 
from .qdrant import vector_store but it threw error, saying can't find it, hence I ran this as a package using the command "python -m src.rag" instead of "python src/rag.py" to run the python file. 

Frontend -

Install nodejs from nodejs.org/en
And run the command to install necessary dependencies to run react and also directories with sample files to work on in you project

    npx create-react-app .

we need axios to handle http and api requests in js.
To install 

    npm install axios
To install react-markdown 

    npm install react_markdown

