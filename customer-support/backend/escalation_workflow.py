# escalation_workflow.py
def needs_escalation(response_data: dict, query: str) -> bool:

    low_confidence = response_data.get("confidence", 1.0) < 0.7
    critical_keywords = ["complaint", "urgent", "not satisfied", "escalate", "immediate", "asap"]
    contains_critical = any(word in query.lower() for word in critical_keywords)
    return low_confidence or contains_critical

def escalate_query(query: str, response_data: dict) -> str:

    urgent_keywords = ["urgent", "immediate", "asap"]
    if any(word in query.lower() for word in urgent_keywords):
        default_message = "Your query has been marked as urgent. A support agent will contact you immediately."
        escalation_message = f"Escalated Query (URGENT): {query}\nResponse: {default_message}"
        return escalation_message
    else:
        escalation_message = f"Escalated Query: {query}\nResponse: {response_data.get('response')}"
        return escalation_message