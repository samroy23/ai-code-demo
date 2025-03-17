# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Azure OpenAI Configuration
azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

openai.api_type = "azure"
openai.api_key = azure_openai_key
openai.api_base = azure_openai_endpoint
openai.api_version = "2023-05-15"

# Import multi-agent components
from agents.planning_agent import planning_agent
from agents.execution_agent import execution_agent
from agents.context_manager import ContextManager
from agents.knowledge_manager import knowledge_manager

# Initialize a context manager instance
context_manager = ContextManager()

@app.route('/api/multi-agent', methods=['POST'])
def multi_agent():
    try:
        # Detect whether an image file is included in the request
        if 'image' in request.files:
            has_image = True
            image_file = request.files['image']
            user_input = request.form.get('message', '')
            prompt = request.form.get('prompt', 'Describe this image in detail.')
        else:
            has_image = False
            image_file = None
            data = request.json
            user_input = data.get('message', '')
            prompt = data.get('prompt', '')

        if not user_input and not has_image:
            return jsonify({"error": "No input provided"}), 400

        # Update context with the user input
        context_manager.add_interaction(f"User: {user_input}")

        # Retrieve current conversation context
        current_context = context_manager.get_context()

        # Use the planning agent to determine the task type
        plan = planning_agent(user_input, has_image)

        # Execute the task using the execution agent, passing the conversation context
        ai_message = execution_agent(plan, user_input, context=current_context, image_file=image_file, prompt=prompt)

        # If image analysis was performed, store the result in the knowledge manager
        if plan == "image_analysis":
            knowledge_manager.add_knowledge("latest_image_analysis", ai_message)

        # Retrieve shared knowledge for optional display
        shared_knowledge = knowledge_manager.get_all_knowledge()

        # Update context with the AI's response
        context_manager.add_interaction(f"AI: {ai_message}")

        # Retrieve updated context
        context = context_manager.get_context()
        return jsonify({"message": ai_message, "context": context, "knowledge": shared_knowledge})

    except Exception as e:
        logger.error(f"Error in multi-agent endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Warn if required Azure credentials are missing
    required_vars = ["AZURE_OPENAI_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT", "AZURE_VISION_KEY", "AZURE_VISION_ENDPOINT"]
    if not all([os.getenv(var) for var in required_vars]):
        logger.warning("Some required Azure credentials are missing. Please check your .env file.")
    app.run(debug=True, port=5000)
