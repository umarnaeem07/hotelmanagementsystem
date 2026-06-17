from typing import TypedDict


class RoomState(TypedDict):

    hotel_id: int

    available_rooms: int
    occupied_rooms: int
    reserved_rooms: int
    cleaning_rooms: int
    maintenance_rooms: int

    room_details: dict | None

    decision: str
    steps: list

from rooms.models import Room


def load_room_stats(state):

    hotel_id = state["hotel_id"]

    rooms = Room.objects.filter(
        hotel_id=hotel_id
    )

    state["available_rooms"] = rooms.filter(
        status="available"
    ).count()

    state["occupied_rooms"] = rooms.filter(
        status="occupied"
    ).count()

    state["reserved_rooms"] = rooms.filter(
        status="reserved"
    ).count()

    state["cleaning_rooms"] = rooms.filter(
        status="cleaning"
    ).count()

    state["maintenance_rooms"] = rooms.filter(
        status="maintenance"
    ).count()

    state["steps"].append("Room stats loaded")

    return state
def get_room_details(state, room_number=None):

    if not room_number:
        return state

    try:

        room = Room.objects.get(
            hotel_id=state["hotel_id"],
            room_number=room_number
        )

        state["room_details"] = {
            "room_number": room.room_number,
            "type": room.room_type,
            "status": room.status,
            "price": room.price,
            "capacity": room.capacity,
        }

        state["steps"].append(
            f"Room {room_number} details fetched"
        )

    except Room.DoesNotExist:

        state["room_details"] = None

        state["steps"].append(
            "Room not found"
        )

    return state

from ai_assistant.llm import llm


def room_summary(state):

    prompt = f"""
You are a hotel operations assistant.

Room Status Summary:
- Available: {state['available_rooms']}
- Occupied: {state['occupied_rooms']}
- Reserved: {state['reserved_rooms']}
- Cleaning: {state['cleaning_rooms']}
- Maintenance: {state['maintenance_rooms']}

Room Detail (if any):
{state.get('room_details')}

Task:
Explain hotel room availability in simple terms for manager.
Suggest operational insights if needed.
"""

    response = llm.invoke(prompt)

    state["decision"] = response.content
    state["steps"].append("AI summary generated")

    return state

from langgraph.graph import StateGraph, END


builder = StateGraph(RoomState)

builder.add_node("load_room_stats", load_room_stats)
builder.add_node("room_summary", room_summary)

builder.set_entry_point("load_room_stats")

builder.add_edge("load_room_stats", "room_summary")
builder.add_edge("room_summary", END)

room_graph = builder.compile()