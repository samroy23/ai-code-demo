# faq_retriever.py

def retrieve_faq_response(query: str) -> dict:

    faq_db = {
        "hours": "Our business hours are from 9 AM to 5 PM, Monday through Friday.",
        "return policy": "You can return any item within 30 days of purchase with a receipt.",
        "shipping": "We offer free shipping on orders over $50."
    }
    
    query_lower = query.lower()
    for key, answer in faq_db.items():
        if key in query_lower:
            return {"response": answer, "confidence": 0.9}
    return None