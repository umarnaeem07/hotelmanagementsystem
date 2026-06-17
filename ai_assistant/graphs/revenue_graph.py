from typing import TypedDict
from datetime import date

from langgraph.graph import StateGraph, END

from invoices.models import Invoice
from payments.models import Payment
from ai_assistant.llm import llm


# -----------------------------
# STATE
# -----------------------------
class RevenueState(TypedDict):

    hotel_id: int

    today_revenue: float
    monthly_revenue: float
    total_revenue: float

    paid_invoices: int
    unpaid_invoices: int

    decision: str
    steps: list


# -----------------------------
# NODE 1: LOAD INVOICE STATS
# -----------------------------
def load_invoices(state):

    hotel_id = state["hotel_id"]

    invoices = Invoice.objects.filter(
        reservation__hotel_id=hotel_id
    )

    state["paid_invoices"] = invoices.filter(
        payment_status="paid"
    ).count()

    state["unpaid_invoices"] = invoices.filter(
        payment_status="unpaid"
    ).count()

    state["steps"].append("Invoices loaded")

    return state


# -----------------------------
# NODE 2: REVENUE CALCULATION
# (BASED ON PAYMENTS - CORRECT)
# -----------------------------
def calculate_revenue(state):

    hotel_id = state["hotel_id"]

    payments = Payment.objects.filter(
        invoice__reservation__hotel_id=hotel_id
    )

    # Total revenue
    state["total_revenue"] = sum(
        p.amount for p in payments
    )

    today = date.today()

    # Today's revenue
    state["today_revenue"] = sum(
        p.amount for p in payments
        if p.paid_at.date() == today
    )

    # Monthly revenue
    state["monthly_revenue"] = sum(
        p.amount for p in payments
        if p.paid_at.month == today.month
    )

    state["steps"].append("Revenue calculated from payments")

    return state


# -----------------------------
# NODE 3: AI SUMMARY
# -----------------------------
def revenue_summary(state):

    prompt = f"""
You are a senior hotel financial analyst.

Analyze hotel financial performance:

Today's Revenue: {state['today_revenue']}
Monthly Revenue: {state['monthly_revenue']}
Total Revenue: {state['total_revenue']}

Invoice Stats:
- Paid Invoices: {state['paid_invoices']}
- Unpaid Invoices: {state['unpaid_invoices']}

Task:
1. Explain financial health
2. Highlight any risks
3. Give short actionable recommendation

Keep response simple and professional for hotel manager.
"""

    response = llm.invoke(prompt)

    state["decision"] = response.content
    state["steps"].append("AI summary generated")

    return state


# -----------------------------
# GRAPH BUILDING
# -----------------------------
builder = StateGraph(RevenueState)

builder.add_node("load_invoices", load_invoices)
builder.add_node("calculate_revenue", calculate_revenue)
builder.add_node("revenue_summary", revenue_summary)

builder.set_entry_point("load_invoices")

builder.add_edge("load_invoices", "calculate_revenue")
builder.add_edge("calculate_revenue", "revenue_summary")
builder.add_edge("revenue_summary", END)

revenue_graph = builder.compile()