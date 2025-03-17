import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, MicOff, Image as ImageIcon, Volume2, VolumeX, Loader2 } from 'lucide-react';
import ChatMessage from './components/ChatMessage';
import { Message } from './types';
import { sendMessage, analyzeImage } from './api';

function App() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! I\'m your multimodal AI assistant. You can chat with me, upload images for analysis, or use voice input.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [recordingError, setRecordingError] = useState<string | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const mediaRecorderRef = useRef<any>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle text input submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    let messageToSend = input.trim();
    
    // Check if there's a transcribed message
    const lastMessage = messages[messages.length - 1];
    if (lastMessage?.isVoice && !lastMessage.isProcessing) {
      messageToSend = lastMessage.content;
      // Remove the transcription message since we're sending it
      setMessages(prev => prev.slice(0, -1));
    }
  
    if (!messageToSend && !selectedImage) return;
  
    // Clear input
    setInput('');
  
    // Add user message
    const newUserMessage: Message = { 
      role: 'user', 
      content: messageToSend 
    };
    setMessages(prev => [...prev, newUserMessage]);
  
    // Handle image upload
    if (selectedImage) {
      setIsLoading(true);
      try {
        // Add user message with image
        const imageUrl = URL.createObjectURL(selectedImage);
        const newUserMessage: Message = {
          role: 'user',
          content: input || 'Please analyze this image.',
          image: imageUrl
        };
        
        setMessages(prev => [...prev, newUserMessage]);
        
        // Send image for analysis
        const response = await analyzeImage(selectedImage, input);
        
        // Add AI response
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: response.message 
        }]);
        
        // Clear image
        setSelectedImage(null);
        setImagePreview(null);
      } catch (error) {
        console.error('Error analyzing image:', error);
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: 'Sorry, I encountered an error analyzing the image. Please make sure your Azure Vision service is properly configured.' 
        }]);
      } finally {
        setIsLoading(false);
      }
      return;
    }
  
    // Send message to chat API
    setIsLoading(true);
    try {
      const response = await sendMessage(messageToSend);
      
      const newAiMessage: Message = { 
        role: 'assistant', 
        content: response.message 
      };
      
      setMessages(prev => [...prev, newAiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error processing your request.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle image selection
  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedImage(file);
      setImagePreview(URL.createObjectURL(file));
    }
  };

  // Trigger file input click
  const handleImageButtonClick = () => {
    fileInputRef.current?.click();
  };

  // Clear selected image
  const handleClearImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Handle voice recording
  const startRecording = async () => {
    try {
      setRecordingError(null);
      
      if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        setRecordingError('Speech recognition is not supported in your browser. Please use Chrome.');
        return;
      }

      // Create speech recognition instance
      const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
      const recognition = new SpeechRecognition();
      
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      // Add user message placeholder for transcription
      const transcriptionMessage: Message = {
        role: 'user',
        content: '...',
        isVoice: true,
        isProcessing: true
      };
      setMessages(prev => [...prev, transcriptionMessage]);

      recognition.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map(result => result[0])
          .map(result => result.transcript)
          .join('');

        // Update the last message with current transcript
        setMessages(prev => 
          prev.map((msg, idx) => 
            idx === prev.length - 1 && msg.isVoice 
              ? { ...msg, content: transcript, isProcessing: false } 
              : msg
          )
        );
        // Set the input value so user can edit if needed
        setInput(transcript);
      };

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setRecordingError(`Error: ${event.error}`);
        setIsRecording(false);
        recognition.stop();
      };

      recognition.onend = () => {
        setIsRecording(false);
        // Keep the transcribed message in chat area
        setMessages(prev => 
          prev.map((msg, idx) => 
            idx === prev.length - 1 && msg.isVoice 
              ? { ...msg, isProcessing: false } 
              : msg
          )
        );
      };

      recognition.start();
      setIsRecording(true);
      mediaRecorderRef.current = recognition;

    } catch (error) {
      console.error('Error starting recording:', error);
      setRecordingError('Could not access microphone. Please check your browser permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  // Text-to-speech functionality
  const speakText = (text: string) => {
    if ('speechSynthesis' in window) {
      // Stop any ongoing speech
      window.speechSynthesis.cancel();
      
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);
      
      window.speechSynthesis.speak(utterance);
    }
  };

  const stopSpeaking = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  };

  // Toggle speech for a specific message
  const toggleSpeech = (message: Message) => {
    if (isSpeaking) {
      stopSpeaking();
    } else {
      speakText(message.content);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-gray-100">
      {/* Header */}
      <header className="bg-gray-800 p-4 shadow-md">
        <div className="container mx-auto flex items-center justify-between">
          <h1 className="text-2xl font-bold text-indigo-400 flex items-center">
            <div className="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center mr-3">
              <Volume2 className="w-6 h-6" />
            </div>
            MultiAgent AI Assistant
          </h1>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 overflow-hidden container mx-auto flex flex-col p-4">
        {/* Chat messages */}
        <div className="flex-1 overflow-y-auto mb-4 space-y-4 pr-2">
          {messages.map((message, index) => (
            <ChatMessage 
              key={index} 
              message={message} 
              onSpeakToggle={() => toggleSpeech(message)}
              isSpeaking={isSpeaking}
            />
          ))}
          {isLoading && (
            <div className="flex justify-center items-center py-4">
              <Loader2 className="w-6 h-6 animate-spin text-indigo-500" />
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Image preview */}
        {imagePreview && (
          <div className="relative mb-4 inline-block">
            <img 
              src={imagePreview} 
              alt="Selected" 
              className="max-h-60 rounded-lg border border-gray-700" 
            />
            <button 
              onClick={handleClearImage}
              className="absolute top-2 right-2 bg-gray-800 rounded-full p-1 text-gray-300 hover:text-white"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        )}

        {/* Recording error message */}
        {recordingError && (
          <div className="mb-4 p-3 bg-red-900/50 text-red-200 rounded-lg">
            <p>{recordingError}</p>
          </div>
        )}

        {/* Input form */}
        <form onSubmit={handleSubmit} className="flex items-end gap-2 bg-gray-800 p-3 rounded-lg">
          <button 
            type="button"
            onClick={handleImageButtonClick}
            className="p-2 rounded-full bg-gray-700 hover:bg-gray-600 text-gray-300 hover:text-white transition-colors"
            title="Upload image"
          >
            <ImageIcon className="w-5 h-5" />
          </button>
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleImageSelect} 
            accept="image/*" 
            className="hidden" 
          />
          
          <button 
            type="button"
            onClick={isRecording ? stopRecording : startRecording}
            className={`p-2 rounded-full ${isRecording ? 'bg-red-600 hover:bg-red-700' : 'bg-gray-700 hover:bg-gray-600'} text-gray-300 hover:text-white transition-colors`}
            title={isRecording ? "Stop recording" : "Start recording"}
          >
            {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
          </button>
          
          <div className="flex-1 relative">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="w-full p-3 pr-10 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
              rows={1}
              style={{ minHeight: '44px', maxHeight: '150px' }}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
          </div>
          
          <button 
            type="submit" 
            disabled={isLoading || (!input.trim() && !selectedImage)}
            className={`p-2 rounded-full ${(!input.trim() && !selectedImage) ? 'bg-gray-700 text-gray-500' : 'bg-indigo-600 hover:bg-indigo-700 text-white'} transition-colors`}
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;