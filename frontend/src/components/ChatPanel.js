/**
 * Chat Panel Component
 *
 * Displays chat messages separate from game commands.
 * Supports different message types: say, whisper, shout, global.
 */
import React, { useState, useEffect, useRef } from 'react';
import './ChatPanel.css';

function ChatPanel({ lastMessage }) {
  const [messages, setMessages] = useState([]);
  const [filter, setFilter] = useState('all'); // all, say, whisper, shout, global
  const chatEndRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle incoming messages
  useEffect(() => {
    if (!lastMessage) return;

    const chatTypes = ['broadcast', 'whisper', 'shout', 'zone_broadcast', 'chat', 'global'];
    if (chatTypes.includes(lastMessage.type)) {
      setMessages(prev => [...prev, {
        type: lastMessage.type,
        content: lastMessage.message,
        timestamp: new Date()
      }]);
    }
  }, [lastMessage]);

  const getFilteredMessages = () => {
    if (filter === 'all') return messages;
    return messages.filter(msg => {
      if (filter === 'say') return msg.type === 'broadcast';
      if (filter === 'whisper') return msg.type === 'whisper';
      if (filter === 'shout') return msg.type === 'shout' || msg.type === 'zone_broadcast';
      if (filter === 'global') return msg.type === 'chat' || msg.type === 'global';
      return false;
    });
  };

  const getMessageClass = (type) => {
    switch(type) {
      case 'broadcast': return 'message-say';
      case 'whisper': return 'message-whisper';
      case 'shout':
      case 'zone_broadcast': return 'message-shout';
      case 'chat':
      case 'global': return 'message-global';
      default: return 'message-default';
    }
  };

  const getMessagePrefix = (type) => {
    switch(type) {
      case 'broadcast': return '[SAY]';
      case 'whisper': return '[WHISPER]';
      case 'shout': return '[SHOUT]';
      case 'zone_broadcast': return '[SHOUT]';
      case 'chat': return '[GLOBAL]';
      case 'global': return '[GLOBAL]';
      default: return '';
    }
  };

  const clearMessages = () => {
    setMessages([]);
  };

  const filteredMessages = getFilteredMessages();

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <h3>Chat</h3>
        <button onClick={clearMessages} className="btn-clear" title="Clear chat">
          Clear
        </button>
      </div>

      <div className="chat-filters">
        <button
          className={filter === 'all' ? 'active' : ''}
          onClick={() => setFilter('all')}
        >
          All
        </button>
        <button
          className={filter === 'say' ? 'active' : ''}
          onClick={() => setFilter('say')}
        >
          Say
        </button>
        <button
          className={filter === 'whisper' ? 'active' : ''}
          onClick={() => setFilter('whisper')}
        >
          Whisper
        </button>
        <button
          className={filter === 'shout' ? 'active' : ''}
          onClick={() => setFilter('shout')}
        >
          Shout
        </button>
        <button
          className={filter === 'global' ? 'active' : ''}
          onClick={() => setFilter('global')}
        >
          Global
        </button>
      </div>

      <div className="chat-messages">
        {filteredMessages.length === 0 ? (
          <div className="no-messages">No messages yet...</div>
        ) : (
          filteredMessages.map((msg, index) => (
            <div key={index} className={`chat-message ${getMessageClass(msg.type)}`}>
              <span className="message-prefix">{getMessagePrefix(msg.type)}</span>
              <span className="message-content">{msg.content}</span>
            </div>
          ))
        )}
        <div ref={chatEndRef} />
      </div>
    </div>
  );
}

export default ChatPanel;
