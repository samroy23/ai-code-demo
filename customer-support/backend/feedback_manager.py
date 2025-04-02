# feedback_manager.py

import json
import os

feedback_db = []

# Define the file path for storing feedback
FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "feedbacks.json")

def load_feedbacks():
    global feedback_db
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            try:
                feedback_db = json.load(f)
            except json.JSONDecodeError:
                feedback_db = []
    else:
        feedback_db = []

def save_feedbacks():
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback_db, f, indent=2)

def record_feedback(query: str, ai_response: str, feedback: str):
    entry = {"query": query, "response": ai_response, "feedback": feedback}
    feedback_db.append(entry)
    save_feedbacks()  # Save the updated feedback to file
    return entry

def get_feedback():
    load_feedbacks()  # Reload from file to ensure the latest data is returned
    return feedback_db