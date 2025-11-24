/**
 * Game Page Component
 *
 * Main game interface with terminal and game display.
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import GameTerminal from '../components/GameTerminal';
import PlayerStats from '../components/PlayerStats';
import CharacterSheet from '../components/CharacterSheet';
import ChatPanel from '../components/ChatPanel';
import { useWebSocket } from '../hooks/useWebSocket';

function GamePage() {
  const navigate = useNavigate();
  const [token, setToken] = useState(null);
  const [showCharacterSheet, setShowCharacterSheet] = useState(false);

  // Shared WebSocket connection
  const { sendMessage, lastMessage, connected } = useWebSocket(token);

  useEffect(() => {
    // Check if user is logged in
    const storedToken = localStorage.getItem('token');
    if (!storedToken) {
      navigate('/login');
      return;
    }
    setToken(storedToken);
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/');
  };

  const toggleCharacterSheet = () => {
    setShowCharacterSheet(!showCharacterSheet);
  };

  if (!token) {
    return <div>Loading...</div>;
  }

  return (
    <div className="game-page">
      <header className="game-header">
        <h1>Forgotten Ruin</h1>
        <div>
          <button onClick={toggleCharacterSheet} className="btn">
            Character Sheet
          </button>
          <button onClick={handleLogout} className="btn btn-logout">
            Logout
          </button>
        </div>
      </header>

      <div className="game-container">
        <div className="game-sidebar">
          <PlayerStats token={token} lastMessage={lastMessage} />
        </div>

        <div className="game-main">
          <GameTerminal
            token={token}
            sendMessage={sendMessage}
            lastMessage={lastMessage}
            connected={connected}
          />
        </div>

        <div className="game-sidebar-right">
          <ChatPanel lastMessage={lastMessage} />
        </div>
      </div>

      {showCharacterSheet && (
        <div className="modal-overlay">
          <div className="modal-content">
            <CharacterSheet />
            <button onClick={toggleCharacterSheet} className="btn">
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default GamePage;
