/**
 * Game Terminal Component
 *
 * Main terminal interface for game commands and output.
 */
import React, { useState, useEffect, useRef } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

function GameTerminal({ token }) {
  const [output, setOutput] = useState([]);
  const [input, setInput] = useState('');
  const [commandHistory, setCommandHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const terminalEndRef = useRef(null);
  const inputRef = useRef(null);

  const { sendMessage, lastMessage, connected } = useWebSocket(token);

  // Auto-scroll to bottom
  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [output]);

  // Handle incoming WebSocket messages
  useEffect(() => {
    if (lastMessage) {
      setOutput(prev => [...prev, lastMessage]);
    }
  }, [lastMessage]);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!input.trim()) return;

    // Add to output
    setOutput(prev => [...prev, { type: 'command', message: `> ${input}` }]);

    // Send command via WebSocket
    sendMessage({
      type: 'command',
      command: input.trim()
    });

    // Add to history
    setCommandHistory(prev => [input, ...prev]);
    setHistoryIndex(-1);

    // Clear input
    setInput('');
  };

  const handleKeyDown = (e) => {
    // Arrow up - previous command
    if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (historyIndex < commandHistory.length - 1) {
        const newIndex = historyIndex + 1;
        setHistoryIndex(newIndex);
        setInput(commandHistory[newIndex]);
      }
    }

    // Arrow down - next command
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIndex > 0) {
        const newIndex = historyIndex - 1;
        setHistoryIndex(newIndex);
        setInput(commandHistory[newIndex]);
      } else if (historyIndex === 0) {
        setHistoryIndex(-1);
        setInput('');
      }
    }
  };

  return (
    <div className="game-terminal">
      <div className="terminal-output">
        {!connected && (
          <div className="connection-status disconnected">
            Connecting to game server...
          </div>
        )}

        {output.map((line, index) => (
          <div key={index} className={`output-line ${line.type}`}>
            <pre>{line.message}</pre>
          </div>
        ))}

        <div ref={terminalEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="terminal-input-form">
        <div className="terminal-input">
          <span className="terminal-prompt">&gt;</span>
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Enter command..."
            disabled={!connected}
            autoFocus
          />
        </div>
      </form>
    </div>
  );
}

export default GameTerminal;
