from typing import TypedDict
from reservations.models import Reservation
from invoices.models import Invoice
from langgraph.graph import (
    StateGraph,
    END
)
from ai_assistant.llm import llm



class PaymentState(TypedDict):

    reservation_id: int

    reservation_exists: bool

    room_invoice_paid: bool

    additional_invoice_paid: bool

    outstanding_balance: float

    decision: str

    steps: list

def get_reservation(state):

    reservation_id = state["reservation_id"]

    try:

        reservation = Reservation.objects.get(
            pk=reservation_id
        )

        state["reservation_exists"] = True

        state["steps"].append(
            "Reservation found"
        )

    except Reservation.DoesNotExist:

        state["reservation_exists"] = False

        state["decision"] = (
            "Reservation not found."
        )

        state["steps"].append(
            "Reservation not found"
        )

    return state


def get_invoices(state):

    if not state["reservation_exists"]:
        return state

    reservation = Reservation.objects.get(
        pk=state["reservation_id"]
    )

    room_invoice = Invoice.objects.filter(
        reservation=reservation,
        invoice_type="room"
    ).first()

    additional_invoice = Invoice.objects.filter(
        reservation=reservation,
        invoice_type="additional"
    ).first()

    # -------------------------
    # ROOM INVOICE
    # -------------------------
    if room_invoice:

        state["room_invoice_paid"] = (
            room_invoice.payment_status == "paid"
        )

        state["steps"].append(
            "Room invoice found"
        )

    else:

        state["room_invoice_paid"] = False

        state["steps"].append(
            "No room invoice"
        )

    # -------------------------
    # ADDITIONAL INVOICE
    # -------------------------
    if additional_invoice:

        state["additional_invoice_paid"] = (
            additional_invoice.payment_status == "paid"
        )

        state["steps"].append(
            "Additional invoice found"
        )

    else:

        state["additional_invoice_paid"] = True

        state["steps"].append(
            "No additional invoice"
        )

    # -------------------------
    # BALANCE CALCULATION
    # -------------------------
    balance = 0.0

    if room_invoice and room_invoice.payment_status == "unpaid":
        balance += float(room_invoice.total_amount)

    if additional_invoice and additional_invoice.payment_status == "unpaid":
        balance += float(additional_invoice.total_amount)

    state["outstanding_balance"] = balance

    return state

def payment_summary(state):

    if not state["reservation_exists"]:
        return state

    prompt = f"""
            Reservation ID: {state['reservation_id']}

            Room invoice paid:
            {state['room_invoice_paid']}

            Outstanding balance:
            {state['outstanding_balance']}

            Explain the payment status to a hotel receptionist.
            """
    response = llm.invoke(prompt)
    state["decision"] = response.content

    state["steps"].append(
        "Payment summary generated"
    )

    return state

builder = StateGraph(
    PaymentState
)
builder.add_node(
    "get_reservation",
    get_reservation
)

builder.add_node(
    "get_invoices",
    get_invoices
)

builder.add_node(
    "payment_summary",
    payment_summary
)

builder.set_entry_point(
    "get_reservation"
)

builder.add_edge(
    "get_reservation",
    "get_invoices"
)

builder.add_edge(
    "get_invoices",
    "payment_summary"
)

builder.add_edge(
    "payment_summary",
    END
)

payment_graph = builder.compile()

