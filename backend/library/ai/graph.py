import os
import requests
from typing import TypedDict, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.types import interrupt
from langgraph.checkpoint.memory import InMemorySaver

from .utils import generate_ai_response, similarity_search

from .models import Complain
from django.contrib.auth.models import User


load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
checkpointer = InMemorySaver()


class AgentState(TypedDict):
    user_input: str
    username: Optional[str]
    intent: Optional[str] # "info" | "request" | "complaint"
    response: Optional[str]
    reteieved_docs: Optional[list]


# def classify_intent(state: AgentState):
#     prompt = f"""
#     Classify the user input info one of the two categories:
#     1. info
#     2. complaint

#     Input: {state['user_input']}
#     Respond with only one word: info or complaint
#     """
#     result = llm.invoke(prompt).content.strip().lower()
#     print("Intent: ", result)
#     state["intent"] = result
#     return state


def classify_intent(state: AgentState):
    print("user input: ", state["user_input"])
    response = requests.post(
            "https://openrouter.ai/api/alpha/decisions",
            headers={
                "Authorization": f"Bearer {os.environ['JEV_API_KEY']}",
                "Content-Type": "application/json",
            },
            json={
                "model": "typesafe/jev-1.13",
                "state": {
                    "topic": "local library",
                    "query": state['user_input'],
                },
                "questions": {
                    "is_info": {
                        "type": "noul",
                        "instructions": (
                            "Determine whether the user is asking for information"
                            "or making a complaint."
                        ),
                        "criteria": {
                            "true": "The user needs some information.",
                            "false": "The user wants to register a complaint.",
                        },
                    }
                },
            },
        )
    response.raise_for_status()
    print("JEV answer: ", response.json()["answers"])
    needs_info = response.json()["answers"]["is_info"]["noul"] > 0.5
    state["intent"] = "info" if needs_info else "complaint"
    return state


def info_tool(state: AgentState):
    query = state["user_input"]
    context = similarity_search(query)
    response = generate_ai_response(query, context)

    state["response"] = response
    print("Response: ", response)
    return state


def complaint_tool(state: AgentState):
    username = state["username"]
    user = User.objects.get(username=username)
    answer = interrupt(
        # This message will be sent to the client
        # as part of the interrupt information.
        "Could you please elaborate your problem, tell us when this happened?"
    )
    # Insert complain in the database 
    Complain.objects.create(complain=answer, user=user)
    state["response"] = "Sorry for the inconvenience, your complaint has been registered. We will address it soon."

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
    graph = builder.compile(checkpointer=checkpointer)
    return graph




    