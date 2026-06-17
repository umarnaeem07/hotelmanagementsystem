def classify_intent(question):

    question = question.lower()

    if "check in" in question:
        return "checkin"

    if "check out" in question:
        return "checkout"

    if "payment" in question:
        return "payment"

    if "revenue" in question:
        return "revenue"

    if "room" in question:
        return "room"

    if "guest" in question:
        return "guest"

    if "reservation" in question:
        return "reservation"

    return "unknown"