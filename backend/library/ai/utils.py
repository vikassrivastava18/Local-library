from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from catalog.models import LibraryInfo


llm = ChatOpenAI(model="gpt-4o", temperature=0)


load_dotenv()
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def info_chunks():
    libraryInfo = LibraryInfo.objects.all()
    documents = []
    for info in libraryInfo:
        document_chunk = Document(page_content=info.category + ": " + info.information)
        documents.append(document_chunk)

    return documents


def similarity_search(query):
    # get the info chunks
    chunks = info_chunks()
    # Create in-memory vector store (FAISS)
    vector_store = FAISS.from_documents(chunks, embeddings)
    # perform the similarity search
    results = vector_store.similarity_search(query, k=10)
    # results = vector
    print("Simimilarity results: ", results)
    context = "\n\n".join([doc.page_content for doc in results])
    return context


def generate_ai_response(query, context):
    from datetime import datetime

    today = datetime.now().strftime("%A")
    time = datetime.now().strftime("%H:%M")

    prompt = f"""
        You are a helpful assistant for a library system based in India.

        Use the following context to answer the question. 

        Today is: {today}
        Time is: {time}

        Context:
        {context}

        Question:
        {query}

        Answer:
    """
    response = llm.invoke(prompt)
    return response.content
