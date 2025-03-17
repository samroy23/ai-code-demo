export interface Message {
  role: 'user' | 'assistant';
  content: string;
  image?: string;
  audioUrl?: string;
  isVoice?: boolean;
  isProcessing?: boolean;
}

export interface ApiResponse {
  message: string;
  error?: string;
}