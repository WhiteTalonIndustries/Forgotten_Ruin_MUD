/**
 * Home Page Component
 *
 * Landing page for the game.
 */
import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div className="home-page">
      <header className="game-header">
        <h1>Forgotten Ruin MUD</h1>
        <p>A text-based multiplayer adventure</p>
      </header>

      <div className="home-content">
        <div className="button-group">
          <Link to="/login" className="btn btn-primary">
            Login
          </Link>
          <Link to="/register" className="btn btn-secondary">
            Register
          </Link>
        </div>

        <div className="game-description">
          <h2>Welcome to the Forgotten Ruin</h2>
          <p>
            Explore a vast world filled with mystery, danger, and adventure.
            Battle monsters, complete quests, and forge your legend in this
            classic-style MUD experience brought to the modern web.
          </p>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
