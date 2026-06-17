from typing import TypedDict

from guests.models import Guest
from reservations.models import Reservation

from langgraph.graph import (
    StateGraph,
    END
)

from ai_assistant.llm import llm


class GuestState(TypedDict):

    hotel_id: int

    total_guests: int

    checked_in_guests: int

    guest_name: str | None

    guest_exists: bool

    guest_details: dict

    decision: str

    steps: list


def load_guest_statistics(state):

    hotel_id = state["hotel_id"]

    state["total_guests"] = (
        Guest.objects.filter(
            hotel_id=hotel_id
        ).count()
    )

    state["checked_in_guests"] = (
        Reservation.objects.filter(
            hotel_id=hotel_id,
            status="checked_in"
        ).count()
    )

    state["steps"].append(
        "Guest statistics loaded"
    )

    return state


def load_guest_details(state):

    guest_name = state.get("guest_name")

    if not guest_name:
        state["guest_exists"] = False

        state["steps"].append(
            "No guest name provided"
        )

        return state

    guest = Guest.objects.filter(
        hotel_id=state["hotel_id"],
        first_name__icontains=guest_name
    ).first()

    if not guest:

        state["guest_exists"] = False

        state["steps"].append(
            "Guest not found"
        )

        return state

    state["guest_exists"] = True

    latest_reservation = (
        Reservation.objects.filter(
            guest=guest
        )
        .order_by("-created_at")
        .first()
    )

    state["guest_details"] = {
        "id": guest.id,
        "name": f"{guest.first_name} {guest.last_name}",
        "email": guest.email,
        "phone": guest.phone_number,
        "reservation_status":
        latest_reservation.status
        if latest_reservation
        else "No reservation"
    }

    state["steps"].append(
        "Guest details loaded"
    )

    return state


def generate_guest_summary(state):

    if state.get("guest_exists"):

        prompt = f"""
You are a hotel assistant.

Guest details:

{state['guest_details']}

Explain these details in a friendly way.
"""

    else:

        prompt = f"""
You are a hotel assistant.

Total guests:
{state['total_guests']}

Currently checked-in guests:
{state['checked_in_guests']}

Explain these statistics to a hotel manager.
"""

    response = llm.invoke(prompt)

    state["decision"] = response.content

    state["steps"].append(
        "AI summary generated"
    )

    return state


builder = StateGraph(
    GuestState
)

builder.add_node(
    "load_guest_statistics",
    load_guest_statistics
)

builder.add_node(
    "load_guest_details",
    load_guest_details
)

builder.add_node(
    "generate_guest_summary",
    generate_guest_summary
)

builder.set_entry_point(
    "load_guest_statistics"
)

builder.add_edge(
    "load_guest_statistics",
    "load_guest_details"
)

builder.add_edge(
    "load_guest_details",
    "generate_guest_summary"
)

builder.add_edge(
    "generate_guest_summary",
    END
)

guest_graph = builder.compile()