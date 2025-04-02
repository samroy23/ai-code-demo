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
vision_key = os.getenv("AZURE_VISION_KEY")
vision_endpoint = os.getenv("AZURE_VISION_ENDPOINT")

# Configure OpenAI with Azure settings
openai.api_type = "azure"
openai.api_key = azure_openai_key
openai.api_base = azure_openai_endpoint
openai.api_version = "2023-05-15"

# TODO 2: Initialize Azure Vision API Client
vision_client = ImageAnalysisClient(
 endpoint=vision_endpoint,
 credential=AzureKeyCredential(vision_key)
)

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
@app.route('/api/analyze-image', methods=['POST'])
def analyze_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
      
        image_file = request.files['image']
        prompt = request.form.get('prompt', 'Describe this image in detail.')
        
        # Save image temporarily
        temp_image_path = "temp_image.jpg"
        image_file.save(temp_image_path)
        
        with open(temp_image_path, "rb") as f:
                image_data = f.read()
      
        try:
            result = vision_client.analyze(
               image_data=image_data,
               visual_features=[
                  VisualFeatures.CAPTION,
                  VisualFeatures.TAGS,
                  VisualFeatures.OBJECTS
               ]
            )
         
            caption = result.caption.text if result.caption else ""
            tags = [getattr(tag, "name", str(tag)) for tag in result.tags] if result.tags else []
            objects = [getattr(obj, "name", str(obj)) for obj in result.objects] if result.objects else []
         
        except Exception as analysis_error:
            logger.error(f"Image analysis error: {str(analysis_error)}")
            return jsonify({"error": "Failed to analyze image"}), 500

        analysis_prompt = f"""
            Image Analysis:
            - Caption: {caption}
            - Tags: {', '.join(tags)}
            - Objects: {', '.join(objects)}
            """
        analysis_prompt += f"\n\nUser prompt: {prompt}\n\nBased on the image analysis above, please respond to the user's prompt."
        
        response = openai.ChatCompletion.create(
            engine=azure_openai_deployment,
            messages=[
               {"role": "system", "content": "You are a helpful assistant that analyzes images."},
               {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.7,
            max_tokens=800
            )
      
        ai_message = response.choices[0].message.content
      
        os.remove(temp_image_path)
      
        return jsonify({"message": ai_message})
   
    except Exception as e:
      logger.error(f"Error in analyze-image endpoint: {str(e)}")
      if os.path.exists("temp_image.jpg"):
        os.remove("temp_image.jpg")
      return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if not all([azure_openai_key, azure_openai_endpoint, azure_openai_deployment, 
                vision_key, vision_endpoint]):
        logger.warning("Some Azure credentials are missing. Please set them in .env file.")
    
    app.run(debug=True, port=5000)
