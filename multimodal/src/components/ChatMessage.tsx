import React from 'react';
import { Volume2, VolumeX, Loader2, Mic } from 'lucide-react';
import { Message } from '../types';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import remarkGfm from 'remark-gfm';

interface ChatMessageProps {
  message: Message;
  onSpeakToggle: () => void;
  isSpeaking: boolean;
}

// Update the message display to show when transcription is ready
const ChatMessage: React.FC<ChatMessageProps> = ({ message, onSpeakToggle, isSpeaking }) => {
  const isUser = message.role === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-[80%] ${isUser ? 'bg-indigo-600' : 'bg-gray-800'} rounded-lg p-4 shadow-md`}>
        {message.isVoice && (
          <div className="flex items-center text-sm text-gray-400 mb-2">
            {message.isProcessing ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Listening...
              </>
            ) : (
              <>
                <Mic className="w-4 h-4 mr-2" />
                Review and press Enter to send
              </>
            )}
          </div>
        )}
        
        {message.image && (
          <div className="mb-3">
            <img 
              src={message.image} 
              alt="User uploaded" 
              className="max-h-60 rounded-lg object-contain w-full" 
            />
          </div>
        )}
        
        <div className="prose prose-invert max-w-none">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              code({node, inline, className, children, ...props}) {
                const match = /language-(\w+)/.exec(className || '');
                return !inline && match ? (
                  <SyntaxHighlighter
                    style={vscDarkPlus}
                    language={match[1]}
                    PreTag="div"
                    customStyle={{ margin: 0 }}
                    {...props}
                  >
                    {String(children).replace(/\n$/, '')}
                  </SyntaxHighlighter>
                ) : (
                  <code className={`${className} bg-gray-700 rounded px-1 py-0.5`} {...props}>
                    {children}
                  </code>
                );
              },
              p: ({children}) => <p className="mb-4 last:mb-0">{children}</p>,
              ul: ({children}) => <ul className="list-disc pl-4 mb-4 last:mb-0">{children}</ul>,
              ol: ({children}) => <ol className="list-decimal pl-4 mb-4 last:mb-0">{children}</ol>
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>
        
        {message.audioUrl && (
          <div className="mt-2">
            <audio controls className="w-full">
              <source src={message.audioUrl} type="audio/webm" />
              <source src={message.audioUrl} type="audio/wav" />
              Your browser does not support the audio element.
            </audio>
          </div>
        )}
        
        {!isUser && (
          <div className="flex justify-end mt-2">
            <button 
              onClick={onSpeakToggle}
              className="text-gray-400 hover:text-white transition-colors"
              title={isSpeaking ? "Stop speaking" : "Speak this message"}
              disabled={message.isProcessing}
            >
              {isSpeaking ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;