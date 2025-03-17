# Multimodal AI Assistant

A beautiful dark-themed AI assistant application that integrates with Azure AI services to provide:

- Text chat with GPT models
- Image analysis and description
- Speech recognition for voice input
- Text-to-speech for audio output

## Features

- **Chat Interface**: Communicate with Azure OpenAI GPT models
- **Image Analysis**: Upload images for AI-powered analysis and description
- **Voice Input**: Record speech and convert to text using Azure Speech Services
- **Audio Output**: Listen to AI responses with text-to-speech functionality
- **Responsive Design**: Beautiful dark-themed UI that works on all devices

## Tech Stack

### Frontend
- React with TypeScript
- Tailwind CSS for styling
- Lucide React for icons
- Axios for API requests
- React Markdown for rendering formatted responses

### Backend
- Python Flask server
- Azure OpenAI for chat functionality
- Azure Computer Vision for image analysis
- Azure Speech Services for speech-to-text and text-to-speech

## Setup Instructions

### Prerequisites
- Node.js and npm
- Python 3.8+
- Azure account with the following services:
  - Azure OpenAI
  - Azure Computer Vision
  - Azure Speech Services

### Frontend Setup
1. Install dependencies:
   ```
   npm install
   ```

2. Start the development server:
   ```
   npm run dev
   ```

### Backend Setup
1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and add your Azure credentials:
   ```
   cp .env.example .env
   ```

5. Start the Flask server:
   ```
   python app.py
   ```

## Usage

1. Open your browser and navigate to `http://localhost:5173`
2. Type a message or question in the input field and press Enter
3. Upload an image by clicking the image icon
4. Record voice input by clicking the microphone icon
5. Listen to AI responses by clicking the speaker icon on any assistant message

## Azure Setup

### Azure OpenAI
1. Create an Azure OpenAI resource
2. Deploy a model (e.g., GPT-4)
3. Get the API key, endpoint, and deployment name

### Azure Computer Vision
1. Create an Azure Computer Vision resource
2. Get the API key and endpoint

### Azure Speech Services
1. Create an Azure Speech resource
2. Get the API key and region