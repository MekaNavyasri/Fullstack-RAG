from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_community.chat_models import ChatOpenAI
from operator import itemgetter

from decouple import config

from .qdrant import vector_store

model = ChatOpenAI(
    model_name="gpt-4o",
    openai_api_key=config("OPENAI_API_KEY"),
    temperature=0,
)

prompt_template = """
Answer the question based on the context, in a concise manner, in Markdown format and using bullet points where applicable.

Context: {context}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

retriever = vector_store.as_retriever()

def create_chain():
    chain = (
        {
        "context": retriever.with_config(top_k=4),
        "question": RunnablePassthrough(),
        }
        | RunnableParallel({
            "response": prompt | model,
            "context": itemgetter("context"),
        })
    )
    return chain

def get_answer_and_docs(question:str):
    chain = create_chain()
    response = chain.invoke(question)
    answer = response["response"].content
    context = response["context"]
    return {
        "answer": answer,
        "context": context,
    }

# response = get_answer_and_docs("Who is the author of this article?")
# print(response)
