from typing import TypedDict, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()
llm = ChatOpenAI(model="gpt-4o", temperature=0)

class AgentState(TypedDict):
    user_input: str
    intent: Optional[str] # "info" | "request" | "complaint"
    response: Optional[str]
    reteieved_docs: Optional[list]


def classify_intent(state: AgentState):
    prompt = f"""
    Classify the user input info one of the three categories:
    1. info
    2. request
    3. complaint

    Input: {state['user_input']}
    Respond with only one word: info, request, or complaint
    """
    result = llm.invoke(prompt).content.strip().lower()
    state["intent"] = result
    return state


def info_tool(state: AgentState):
    query = state["user_input"]

    # your similarity search logic here
    results = vector_store.similarity_search(query, k=3)

    context = "\n\n".join([doc.page_content for doc in results])

    response = llm.invoke([
        {"role": "system", "content": "Answer ONLY from context."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{query}"}
    ])

    state["response"] = response.content
    return state


def request_tool(state: AgentState):
    user_input = state["user_input"]

    # Example: detect book request
    if "book" in user_input.lower():
        # pseudo: check DB
        book_available = False  # replace with real query

        if not book_available:
            # insert into request table
            # db.insert_request(...)
            state["response"] = "Your book request has been recorded."
        else:
            state["response"] = "The book is already available in the library."

    else:
        # generic request (AC, timing, etc.)
        # db.insert_request(...)
        state["response"] = "Your request has been submitted."

    return state


def complaint_tool(state: AgentState):
    user_input = state["user_input"]

    # db.insert_complaint(...)
    state["response"] = "Your complaint has been registered. We will address it soon."

    return state

def route_intent(state: AgentState):
    return state["intent"]

def graph_builder():
