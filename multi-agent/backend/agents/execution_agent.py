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

