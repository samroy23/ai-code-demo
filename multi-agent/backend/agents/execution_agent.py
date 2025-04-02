# execution_agent.py
import os
import logging
from azure.ai.vision.imageanalysis.models import VisualFeatures
import openai
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Initialize Azure Vision client using environment variables
vision_key = os.getenv("AZURE_VISION_KEY")
vision_endpoint = os.getenv("AZURE_VISION_ENDPOINT")
azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

vision_client = ImageAnalysisClient(
    endpoint=vision_endpoint,
    credential=AzureKeyCredential(vision_key)
)

research_agent = None

logger = logging.getLogger(__name__)

# TODO 2: Implement execution_agent
def execution_agent(plan: str, user_input: str, context: str = "", image_file=None, prompt: str = "") -> str:
    if plan == "chat":
         # Build the messages including conversation history (if available)
         messages = [
             {"role": "system", "content": "You are a helpful assistant."}
         ]
         if context:
             messages.append({"role": "system", "content": f"Conversation history:\n{context}"})
         messages.append({"role": "user", "content": user_input})
         response = openai.ChatCompletion.create(
             engine=azure_openai_deployment,
             messages=messages,
             temperature=0.7,
             max_tokens=800
         )
         ai_message = response.choices[0].message.content
         return ai_message

    elif plan == "image_analysis" and image_file is not None:
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
             return "Failed to analyze image"
         os.remove(temp_image_path)
         analysis_prompt = (
             f"Image Analysis:\n- Caption: {caption}\n"
             f"- Tags: {', '.join(tags)}\n"
             f"- Objects: {', '.join(objects)}\n\n"
             f"User prompt: {prompt}\n\nBased on the image analysis above, please respond to the user's prompt."
         )
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
         return ai_message

    elif plan == "research":
         query = user_input.strip()[7:].strip()
         if research_agent:
             return research_agent(query)
         else:
             return "Research functionality is not available."

    else:
         return "Invalid plan or missing required input."

