from .llm import llm


def extract_reservation_id(
    question
):

    prompt = f"""
    Extract the reservation number
    from this question.

    Question:
    {question}

    Return ONLY the number.
    """

    response = llm.invoke(
        prompt
    )

    return int(
        response.content.strip()
    )