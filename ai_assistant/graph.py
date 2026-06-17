from langgraph.graph import StateGraph

from .state import CheckInState

from .tools import (
    check_reservation,
    check_invoice,
    check_room,
    make_decision
)
builder = StateGraph(
    CheckInState
)

builder.add_node(
    "reservation",
    check_reservation
)

builder.add_node(
    "invoice",
    check_invoice
)

builder.add_node(
    "room",
    check_room
)

builder.add_node(
    "decision",
    make_decision
)

builder.set_entry_point(
    "reservation"
)

builder.add_edge(
    "reservation",
    "invoice"
)

builder.add_edge(
    "invoice",
    "room"
)

builder.add_edge(
    "room",
    "decision"
)

graph = builder.compile()