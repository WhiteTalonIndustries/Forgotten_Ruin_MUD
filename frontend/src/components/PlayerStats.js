/**
 * Player Stats Component
 *
 * Displays player statistics and character info.
 */
import React, { useState, useEffect } from 'react';
import { getPlayerStats } from '../services/api';

function PlayerStats({ token }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await getPlayerStats(token);
      setStats(data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load stats');
      setLoading(false);
    }
  };

  if (loading) return <div className="player-stats">Loading...</div>;
  if (error) return <div className="player-stats error">{error}</div>;
  if (!stats) return null;

  return (
    <div className="player-stats">
      <h2>{stats.character_name}</h2>

      <div className="stat-group">
        <div className="stat-item">
          <span className="stat-label">Level</span>
          <span className="stat-value">{stats.level}</span>
        </div>

        <div className="stat-item">
          <span className="stat-label">Experience</span>
          <span className="stat-value">{stats.experience}</span>
        </div>
      </div>

      <div className="stat-group">
        <div className="stat-bar">
          <div className="stat-label">Health</div>
          <div className="bar">
            <div
              className="bar-fill health"
              style={{width: `${(stats.health / stats.max_health) * 100}%`}}
            />
            <div className="bar-text">
              {stats.health} / {stats.max_health}
            </div>
          </div>
        </div>

        <div className="stat-bar">
          <div className="stat-label">Mana</div>
          <div className="bar">
            <div
              className="bar-fill mana"
              style={{width: `${(stats.mana / stats.max_mana) * 100}%`}}
            />
            <div className="bar-text">
              {stats.mana} / {stats.max_mana}
            </div>
          </div>
        </div>
      </div>

      <div className="stat-group">
        <h3>Attributes</h3>
        <div className="stat-item">
          <span className="stat-label">Strength</span>
          <span className="stat-value">{stats.strength}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Dexterity</span>
          <span className="stat-value">{stats.dexterity}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Intelligence</span>
          <span className="stat-value">{stats.intelligence}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Constitution</span>
          <span className="stat-value">{stats.constitution}</span>
        </div>
      </div>

      <div className="stat-group">
        <div className="stat-item">
          <span className="stat-label">Gold</span>
          <span className="stat-value">{stats.currency}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Inventory</span>
          <span className="stat-value">
            {stats.inventory_count} / {stats.inventory_size}
          </span>
        </div>
      </div>
    </div>
  );
}

export default PlayerStats;
