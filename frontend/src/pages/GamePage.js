/**
 * Game Page Component
 *
 * Main game interface with terminal and game display.
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import GameTerminal from '../components/GameTerminal';
import PlayerStats from '../components/PlayerStats';
import { useWebSocket } from '../hooks/useWebSocket';

function GamePage() {
  const navigate = useNavigate();
  const [token, setToken] = useState(null);

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

  if (!token) {
    return <div>Loading...</div>;
  }

  return (
    <div className="game-page">
      <header className="game-header">
        <h1>Forgotten Ruin</h1>
        <button onClick={handleLogout} className="btn btn-logout">
          Logout
        </button>
      </header>

      <div className="game-container">
        <div className="game-sidebar">
          <PlayerStats token={token} />
        </div>

        <div className="game-main">
          <GameTerminal token={token} />
        </div>
      </div>
    </div>
  );
}

export default GamePage;
