from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
import openai

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Azure OpenAI Configuration
azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# TODO 1: Configure Azure Vision API

# Configure OpenAI with Azure settings
openai.api_type = "azure"
openai.api_key = azure_openai_key
openai.api_base = azure_openai_endpoint
openai.api_version = "2023-05-15"

# TODO 2: Initialize Azure Vision API Client

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Call Azure OpenAI
        response = openai.ChatCompletion.create(
            engine=azure_openai_deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        ai_message = response.choices[0].message.content
        
        return jsonify({"message": ai_message})
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

# TODO 3: Implement the /api/analyze-image endpoint

if __name__ == '__main__':
    if not all([azure_openai_key, azure_openai_endpoint, azure_openai_deployment, 
                vision_key, vision_endpoint]):
        logger.warning("Some Azure credentials are missing. Please set them in .env file.")
    
    app.run(debug=True, port=5000)
