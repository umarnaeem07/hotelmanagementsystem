from typing import TypedDict


class CheckInState(TypedDict):

    reservation_id: int

    reservation_exists: bool

    invoice_paid: bool

    room_available: bool

    decision: str