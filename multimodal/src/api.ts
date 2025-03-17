import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const sendMessage = async (message: string): Promise<{ message: string }> => {
  try {
    const response = await axios.post(`${API_URL}/chat`, { message });
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};

export const analyzeImage = async (image: File, prompt?: string): Promise<{ message: string }> => {
  try {
    const formData = new FormData();
    formData.append('image', image);
    if (prompt) {
      formData.append('prompt', prompt);
    }
    
    const response = await axios.post(`${API_URL}/analyze-image`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 30000, // Increase timeout to 30 seconds for image analysis
    });
    
    return response.data;
  } catch (error) {
    console.error('Error analyzing image:', error);
    throw error;
  }
};