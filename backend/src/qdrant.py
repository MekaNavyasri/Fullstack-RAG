#from langchain_community.vectorstores import Qdrant
#from langchain_community.embeddings import OpenAIEmbeddings
from langchain_qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader

from qdrant_client import QdrantClient, models
from decouple import config

qdrant_api_key = config("QDRANT_API_KEY")
qdrant_url = config("QDRANT_URL")
collection_name="Websites"

#initialize Qdrant client
client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key
)

vector_store = Qdrant(
    client=client,
    collection_name=collection_name,
    embeddings=OpenAIEmbeddings(
        api_key=config("OPENAI_API_KEY"),
    )
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=20,
    length_function=len,
)

def create_collection(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=1536,  # Size of the OpenAI embeddings
            distance=models.Distance.COSINE,  # Distance metric
        ),
    )
    print(f"Collection '{collection_name}' created successfully.")

def upload_website_to_collection(url:str):
    if not client.collection_exists(collection_name=collection_name):
        create_collection(collection_name)
    loader = WebBaseLoader(url)
    docs = loader.load_and_split(text_splitter=text_splitter)
    for doc in docs:
        doc.metadata = {"source": url}
    vector_store.add_documents(docs)
    return f"{len(docs)} documents from {url} uploaded to collection '{collection_name}' successfully."


# create_collection(collection_name)
# upload_website_to_collection("https://hamel.dev/blog/posts/evals/")