# ai_assistant/router/chat_router.py

from typing import TypedDict
from ai_assistant.extractor import (
    extract_reservation_id
)

class ChatState(TypedDict):

    question: str

    intent: str

    reservation_id: int | None

    hotel_id: int | None

    result: dict

    answer: str

from ai_assistant.llm import llm


from ai_assistant.router.intent_classifier import (
    classify_intent
)

def detect_intent(state):

    state["intent"] = classify_intent(
        state["question"]
    )

    return state
def extract_entities(state):

    state["reservation_id"] = (
        extract_reservation_id(
            state["question"]
        )
    )

    return state


from ai_assistant.graphs.payment_graph import (
    payment_graph
)

from ai_assistant.graphs.revenue_graph import (
    revenue_graph
)

from ai_assistant.graphs.room_graph import (
    room_graph
)

from ai_assistant.graphs.checkout_graph import (
    checkout_graph
)
from ai_assistant.graphs.checkin_graph import (
    checkin_graph
)
from ai_assistant.graphs.guest_graph import (
    guest_graph
)
from ai_assistant.graphs.reservation_graph import (
    reservation_graph
)

def execute_graph(state):

    intent = state["intent"]

    if intent == "checkin":

        state["result"] = (
            checkin_graph.invoke(
                {
                    "reservation_id":
                    state["reservation_id"]
                }
            )
        )

    elif intent == "checkout":

        state["result"] = (
            checkout_graph.invoke(
                {
                    "reservation_id":
                    state["reservation_id"],
                    "steps": []
                }
            )
        )

    elif intent == "payment":

        state["result"] = (
            payment_graph.invoke(
                {
                    "reservation_id":
                    state["reservation_id"],
                    "steps": []
                }
            )
        )

    elif intent == "revenue":

        state["result"] = (
            revenue_graph.invoke(
                {
                    "hotel_id":
                    state["hotel_id"],
                    "steps": []
                }
            )
        )

    elif intent == "room":

        state["result"] = (
            room_graph.invoke(
                {
                    "hotel_id":
                    state["hotel_id"],
                    "steps": []
                }
            )
        )

    elif intent == "guest":

        state["result"] = (
            guest_graph.invoke(
                {
                    "hotel_id":
                    state["hotel_id"],
                    "steps": []
                }
            )
        )

    elif intent == "reservation":

        state["result"] = (
            reservation_graph.invoke(
                {
                    "hotel_id":
                    state["hotel_id"],
                    "steps": []
                }
            )
        )

    else:

        state["result"] = {
            "decision":
            "Unknown request."
        }

    return state

def generate_response(state):

    result = state["result"]

    prompt = f"""
Question:
{state['question']}

System Result:
{result}

Explain the answer naturally.
"""

    response = llm.invoke(prompt)

    state["answer"] = (
        response.content
    )

    return state

from langgraph.graph import (
    StateGraph,
    END
)

builder = StateGraph(ChatState)

builder.add_node(
    "detect_intent",
    detect_intent
)

builder.add_node(
    "extract_entities",
    extract_entities
)

builder.add_node(
    "execute_graph",
    execute_graph
)

builder.add_node(
    "generate_response",
    generate_response
)

builder.set_entry_point(
    "detect_intent"
)

builder.add_edge(
    "detect_intent",
    "extract_entities"
)

builder.add_edge(
    "extract_entities",
    "execute_graph"
)

builder.add_edge(
    "execute_graph",
    "generate_response"
)

builder.add_edge(
    "generate_response",
    END
)

chat_router = builder.compile()