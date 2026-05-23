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
    # libraryInfo = LibraryInfo.objects.all()
    # documents = []
    # for info in libraryInfo:
    #     document_chunk = Document(page_content=info.category + ": " + info.information)
    #     documents.append(document_chunk)

    # return documents

    documents = [
        Document(
            page_content="Saraswati Public Library is a well-known public library located in Lucknow, Uttar Pradesh. It was established in the year 1998 to promote reading and education among the local community."
        ),
        Document(
            page_content="The library operates under the supervision of the State Library Department and is registered with the government under the registration number LIB-UP-1998-0456."
        ),
        Document(
            page_content="It is situated at 123, Hazratganj Road, in a prime area of Lucknow, making it easily accessible to residents and visitors."
        ),
        Document(
            page_content="The library opens every day at 9:00 AM and closes at 7:00 PM, remaining open from Monday to Saturday and closed on Sundays."
        ),
        Document(
            page_content="The facility houses a vast collection of over 75,000 books across multiple genres including literature, science, and technology."
        ),
        Document(
            page_content="The library provides access to a digital library, including e-books and online journals."
        ),
    ]
    return documents


def similarity_search(query):
    # get the info chunks
    chunks = info_chunks()
    print("Chunks: ", chunks)
    # Create in-memory vector store (FAISS)
    vector_store = FAISS.from_documents(chunks, embeddings)
    print("Vector store", type(vector_store))
    # perform the similarity search
    results = vector_store.similarity_search(query, k=10)
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
