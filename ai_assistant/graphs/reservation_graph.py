from typing import TypedDict

from reservations.models import Reservation

from langgraph.graph import (
    StateGraph,
    END
)

from ai_assistant.llm import llm


class ReservationState(TypedDict):

    hotel_id: int

    reservation_id: int | None

    reservation_exists: bool

    total_reservations: int

    active_reservations: int

    reservation_details: dict

    decision: str

    steps: list


def load_reservation_statistics(state):

    hotel_id = state["hotel_id"]

    state["total_reservations"] = (
        Reservation.objects.filter(
            hotel_id=hotel_id
        ).count()
    )

    state["active_reservations"] = (
        Reservation.objects.filter(
            hotel_id=hotel_id,
            status__in=[
                "reserved",
                "checked_in"
            ]
        ).count()
    )

    state["steps"].append(
        "Reservation statistics loaded"
    )

    return state


def load_reservation_details(state):

    reservation_id = state.get(
        "reservation_id"
    )

    if not reservation_id:

        state["reservation_exists"] = False

        state["steps"].append(
            "No reservation id provided"
        )

        return state

    try:

        reservation = Reservation.objects.select_related(
            "guest",
            "room"
        ).get(
            pk=reservation_id,
            hotel_id=state["hotel_id"]
        )

        state["reservation_exists"] = True

        state["reservation_details"] = {
            "reservation_id": reservation.id,
            "guest_name":
                f"{reservation.guest.first_name} "
                f"{reservation.guest.last_name}",
            "room_number":
                reservation.room.room_number,
            "status":
                reservation.status,
            "check_in":
                str(reservation.check_in),
            "check_out":
                str(reservation.check_out),
            "payment_status":
                reservation.payment_status,
            "total_amount":
                float(reservation.total_amount),
        }

        state["steps"].append(
            "Reservation loaded"
        )

    except Reservation.DoesNotExist:

        state["reservation_exists"] = False

        state["steps"].append(
            "Reservation not found"
        )

    return state


def generate_reservation_summary(state):

    if state["reservation_exists"]:

        prompt = f"""
You are a hotel reservation assistant.

Reservation details:

{state["reservation_details"]}

Explain this reservation to a hotel manager.
"""

    else:

        prompt = f"""
You are a hotel reservation assistant.

Total reservations:
{state["total_reservations"]}

Active reservations:
{state["active_reservations"]}

Explain these statistics to a hotel manager.
"""

    response = llm.invoke(prompt)

    state["decision"] = response.content

    state["steps"].append(
        "AI summary generated"
    )

    return state


builder = StateGraph(
    ReservationState
)

builder.add_node(
    "load_reservation_statistics",
    load_reservation_statistics
)

builder.add_node(
    "load_reservation_details",
    load_reservation_details
)

builder.add_node(
    "generate_reservation_summary",
    generate_reservation_summary
)

builder.set_entry_point(
    "load_reservation_statistics"
)

builder.add_edge(
    "load_reservation_statistics",
    "load_reservation_details"
)

builder.add_edge(
    "load_reservation_details",
    "generate_reservation_summary"
)

builder.add_edge(
    "generate_reservation_summary",
    END
)

reservation_graph = builder.compile()