from flask import Flask, request, jsonify, send_from_directory
import os
import logging
from dotenv import load_dotenv
import openai

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Serve frontend from the static folder
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend'), static_url_path='')

# Azure OpenAI configuration
azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
openai.api_type = "azure"
openai.api_key = azure_openai_key
openai.api_base = azure_openai_endpoint
openai.api_version = "2023-05-15"

# Import modules
from customer_service_agent import customer_service_agent
from escalation_workflow import escalate_query
from notification import send_notification_via_logic_app
from feedback_manager import record_feedback, get_feedback

# Define escalation keywords
ESCALATION_KEYWORDS = ["urgent", "immediate", "asap"]

def needs_escalation(query: str) -> bool:
    """Checks if the query contains any escalation keywords."""
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in ESCALATION_KEYWORDS)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/customer-service', methods=['POST'])
def customer_service():
    try:
        data = request.json
        query = data.get("query", "")
        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Process the customer query (using FAQ retrieval with GPT fallback)
        response_data = customer_service_agent(query)
        
        # Check for escalation based solely on urgent keywords
        if needs_escalation(query):
            escalation_message = escalate_query(query, response_data)
            notification_status = send_notification_via_logic_app(escalation_message)
            response_data["escalated"] = True
            response_data["notification"] = notification_status
            # Override response with default urgent message
            response_data["response"] = "Your query has been marked as urgent. A support agent will contact you immediately."
        else:
            response_data["escalated"] = False

        return jsonify(response_data)
    except Exception as e:
        logger.error(f"Error in customer service endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def feedback():
    try:
        data = request.json
        query = data.get("query")
        ai_response = data.get("ai_response")
        feedback_text = data.get("feedback")
        if not query or not ai_response or not feedback_text:
            return jsonify({"error": "Missing data"}), 400
        entry = record_feedback(query, ai_response, feedback_text)
        return jsonify({"status": "Feedback recorded", "entry": entry})
    except Exception as e:
        logger.error(f"Error in feedback endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
