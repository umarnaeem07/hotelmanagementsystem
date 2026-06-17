from typing import TypedDict
from reservations.models import Reservation
from invoices.models import Invoice
from langgraph.graph import (
    StateGraph,
    END
)
class CheckoutState(TypedDict):

    reservation_id: int

    reservation_exists: bool

    checked_in: bool

    additional_invoice_exists: bool

    additional_invoice_paid: bool

    decision: str

    steps: list

def check_reservation(state):

    reservation_exists = (
        Reservation.objects.filter(
            pk=state["reservation_id"]
        ).exists()
    )

    state["reservation_exists"] = (
        reservation_exists
    )

    if reservation_exists:
        state["steps"].append(
            "Reservation found"
        )
    else:
        state["steps"].append(
            "Reservation not found"
        )

    return state
def check_checked_in(state):

    if not state[
        "reservation_exists"
    ]:
        return state

    reservation = Reservation.objects.get(
        pk=state["reservation_id"]
    )

    state["checked_in"] = (
        reservation.status ==
        "checked_in"
    )

    if state["checked_in"]:
        state["steps"].append(
            "Guest is checked in"
        )
    else:
        state["steps"].append(
            "Guest is not checked in"
        )

    return state

def check_additional_invoice(
    state
):

    if not state[
        "reservation_exists"
    ]:
        return state

    invoice = Invoice.objects.filter(
        reservation_id=
        state["reservation_id"],
        invoice_type="additional"
    ).first()

    if invoice:

        state[
            "additional_invoice_exists"
        ] = True

        state[
            "additional_invoice_paid"
        ] = (
            invoice.payment_status ==
            "paid"
        )

        if (
            state[
                "additional_invoice_paid"
            ]
        ):
            state["steps"].append(
                "Additional invoice paid"
            )
        else:
            state["steps"].append(
                "Additional invoice unpaid"
            )

    else:

        state[
            "additional_invoice_exists"
        ] = False

        state[
            "additional_invoice_paid"
        ] = True

        state["steps"].append(
            "No additional invoice"
        )

    return state

def make_decision(state):

    if not state[
        "reservation_exists"
    ]:

        state["decision"] = (
            "Reservation not found."
        )

        return state

    if not state[
        "checked_in"
    ]:

        state["decision"] = (
            "Guest is not checked in."
        )

        return state

    if not state[
        "additional_invoice_paid"
    ]:

        state["decision"] = (
            "Checkout denied. Additional charges are unpaid."
        )

        return state

    state["decision"] = (
        "Guest can check out."
    )

    return state

workflow = StateGraph(
    CheckoutState
)
workflow.add_node(
    "reservation",
    check_reservation
)

workflow.add_node(
    "checked_in",
    check_checked_in
)

workflow.add_node(
    "invoice",
    check_additional_invoice
)

workflow.add_node(
    "decision",
    make_decision
)

workflow.set_entry_point(
    "reservation"
)

workflow.add_edge(
    "reservation",
    "checked_in"
)

workflow.add_edge(
    "checked_in",
    "invoice"
)

workflow.add_edge(
    "invoice",
    "decision"
)

workflow.add_edge(
    "decision",
    END
)
checkout_graph = workflow.compile()

