# customer_service_agent.py

import openai
import os
from faq_retriever import retrieve_faq_response

def customer_service_agent(query: str) -> dict:

    faq_response = retrieve_faq_response(query)
    if faq_response is not None and faq_response.get("confidence", 0) >= 0.85:
        return faq_response

    messages = [
        {"role": "system", "content": "You are a customer service assistant."},
        {"role": "user", "content": query}
    ]
    response = openai.ChatCompletion.create(
        engine=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=messages,
        temperature=0.5,
        max_tokens=500
    )
    ai_response = response.choices[0].message.content
    # Force a low confidence value (0.1) for demo purposes.
    return {"response": ai_response, "confidence": 0.1}