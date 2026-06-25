from .models import (
    ChatSession,
    ChatMessage
)
import re



def save_user_message(
    session,
    content
):

    ChatMessage.objects.create(
        session=session,
        role="user",
        content=content
    )


def save_assistant_message(
    session,
    content
):

    ChatMessage.objects.create(
        session=session,
        role="assistant",
        content=content
    )

def get_recent_messages(
    session,
    limit=10
):

    return list(
        session.messages.order_by(
            "-created_at"
        )[:limit]
    )




def get_last_reservation_id(
    session
):

    messages = (
        session.messages
        .filter(role="user")
        .order_by("-created_at")
    )

    for message in messages:

        match = re.search(
            r"reservation\s+(\d+)",
            message.content.lower()
        )

        if match:

            return int(
                match.group(1)
            )

    return None