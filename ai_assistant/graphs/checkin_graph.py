from typing import TypedDict
from reservations.models import Reservation
from invoices.models import Invoice
from langgraph.graph import StateGraph
from ai_assistant.llm import llm


class CheckInState(TypedDict):

    reservation_id: int

    reservation_exists: bool

    invoice_paid: bool

    room_available: bool

    decision: str


def check_reservation(state):

    reservation_id = state["reservation_id"]

    try:

        reservation = Reservation.objects.get(
            pk=reservation_id
        )

        state["reservation_exists"] = True

    except Reservation.DoesNotExist:

        state["reservation_exists"] = False

    return state



def check_invoice(state):

    if not state["reservation_exists"]:
        return state

    invoice = Invoice.objects.filter(
        reservation_id=state["reservation_id"],
        invoice_type="room"
    ).first()

    if (
        invoice and
        invoice.payment_status == "paid"
    ):
        state["invoice_paid"] = True

    else:
        state["invoice_paid"] = False

    return state


def check_room(state):

    if not state["reservation_exists"]:
        return state

    reservation = Reservation.objects.get(
        pk=state["reservation_id"]
    )

    if reservation.room.status == "available":

        state["room_available"] = True

    else:

        state["room_available"] = False

    return state

def make_decision(state):

    if not state["reservation_exists"]:

        state["decision"] = (
            "Reservation not found."
        )

        return state

    if not state["invoice_paid"]:

        state["decision"] = (
            "Check-in denied. "
            "Room invoice is unpaid."
        )

        return state

    if not state["room_available"]:

        state["decision"] = (
            "Check-in denied. "
            "Room is not available."
        )

        return state

    state["decision"] = (
        "Guest can be checked in."
    )

    return state

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

checkin_graph = builder.compile()