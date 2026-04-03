from typing import TypedDict, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

from .utils import generate_ai_response, similarity_search

from .models import Complain
from django.contrib.auth.models import User

load_dotenv()
llm = ChatOpenAI(model="gpt-4o", temperature=0)

class AgentState(TypedDict):
    user_input: str
    username: Optional[str]
    intent: Optional[str] # "info" | "request" | "complaint"
    response: Optional[str]
    reteieved_docs: Optional[list]


def classify_intent(state: AgentState):
    prompt = f"""
    Classify the user input info one of the two categories:
    1. info
    2. complaint

    Input: {state['user_input']}
    Respond with only one word: info or complaint
    """
    result = llm.invoke(prompt).content.strip().lower()
    print("Intent: ", result)
    state["intent"] = result
    return state


def info_tool(state: AgentState):
    query = state["user_input"]
    context = similarity_search(query)
    response = generate_ai_response(query, context)

    state["response"] = response
    return state


def complaint_tool(state: AgentState):
    user_input = state["user_input"]
    username = state["username"]
    user = User.objects.get(username=username)
    # Insert complain in the database 
    Complain.objects.create(complain=user_input, user=user)
    state["response"] = "Your complaint has been registered. We will address it soon."

    return state

def route_intent(state: AgentState):
    return state["intent"]


def graph_builder():
    builder = StateGraph(AgentState)
    builder.add_node("classifier", classify_intent)
    builder.add_node("info", info_tool)
    builder.add_node("complaint", complaint_tool)

    # Entry point
    builder.set_entry_point("classifier")

    # Routing
    builder.add_conditional_edges(
        "classifier",
        route_intent,
        {
            "info": "info",
            "complaint": "complaint"
        },
    )

    # End nodes
    builder.add_edge("info", END)
    builder.add_edge("complaint", END)

    graph = builder.compile()
    return graph