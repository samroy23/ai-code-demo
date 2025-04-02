import azure.functions as func
import logging
import os
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="agent", methods=["GET", "POST"])
def agent(req: func.HttpRequest) -> func.HttpResponse:
   logging.info("Processing request for GPT‑4 agent.")

   # Try to get the 'message' parameter from the query string.
   user_message = req.params.get("message")
   
   # If not provided via GET, check if it's provided in the JSON body (for POST)
   if not user_message and req.method == "POST":
      try:
            req_body = req.get_json()
      except ValueError:
            return func.HttpResponse("Invalid JSON payload.", status_code=400)
      else:
            user_message = req_body.get("message")
   
   if not user_message:
      return func.HttpResponse(
            "Please provide a 'message' parameter (in the query string or request body).",
            status_code=400
      )
   
   # Retrieve your API key from the environment variables.
   api_key = os.environ.get("OPENAI_API_KEY")
   if not api_key:
      return func.HttpResponse("API key not configured.", status_code=500)
   
   # Define the Azure OpenAI endpoint URL.
   url = ("https://openai-1667358.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2025-01-01-preview")
   
   headers = {
      "Content-Type": "application/json",
      "api-key": api_key
   }
   
   payload = {
      "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
      ]
   }
   
   # Post the request to the OpenAI endpoint.
   response = requests.post(url, headers=headers, json=payload)
   
   if response.status_code != 200:
      logging.error(f"Error calling OpenAI API: {response.status_code} - {response.text}")
      return func.HttpResponse("Error calling OpenAI API.", status_code=response.status_code)
   
   result = response.json()
   # Extract the assistant's reply from the API response.
   assistant_reply = result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
   
   return func.HttpResponse(assistant_reply, status_code=200)