from .llm import llm


def generate_answer(
    question,
    result
):

    prompt = f"""
    User Question:
    {question}

    Workflow Result:
    {result}

    Explain the result
    in a professional hotel
    management assistant tone.
    """

    response = llm.invoke(
        prompt
    )

    return response.content