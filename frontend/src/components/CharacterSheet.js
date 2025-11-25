import React, { useState, useEffect } from 'react';
import api from '../services/api';
import SquadCustomization from './SquadCustomization';

const CharacterSheet = () => {
    const [sheet, setSheet] = useState(null);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('squad'); // squad, stats, inventory, quests
    const [showCustomization, setShowCustomization] = useState(false);
    const [showGenerateModal, setShowGenerateModal] = useState(false);
    const [generating, setGenerating] = useState(false);

    const fetchCharacterSheet = async () => {
        try {
            const response = await api.get('/character/me/');
            setSheet(response.data);
        } catch (err) {
            setError('Failed to load character sheet.');
            console.error(err);
        }
    };

    useEffect(() => {
        fetchCharacterSheet();
    }, []);

    const handleCustomizationUpdate = () => {
        fetchCharacterSheet(); // Refresh the character sheet
    };

    const handleGenerateSquad = async () => {
        setGenerating(true);
        setError(null);
        try {
            const response = await api.post('/squad/generate/', {});
            await fetchCharacterSheet(); // Refresh the character sheet
            setShowGenerateModal(false);
            setGenerating(false);
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to generate squad');
            setGenerating(false);
        }
    };

    if (error) {
        return <div className="character-sheet error">{error}</div>;
    }

    if (!sheet) {
        return <div className="character-sheet loading">Loading...</div>;
    }

    // Health bar component
    const HealthBar = ({ current, max }) => {
        const percentage = (current / max) * 100;
        const barLength = 20;
        const filled = Math.round((percentage / 100) * barLength);
        const bar = '█'.repeat(filled) + '░'.repeat(barLength - filled);
        return <span className="health-bar">{bar} {percentage.toFixed(0)}%</span>;
    };

    // Squad member row
    const SquadMemberRow = ({ member }) => {
        const statusClass = !member.is_alive ? 'kia' : member.is_wounded ? 'wounded' : '';
        const status = !member.is_alive ? '[KIA]' : member.is_wounded ? '[WOUNDED]' : '';
        const duty = member.secondary_duty_display ? ` - ${member.secondary_duty_display}` : '';

        return (
            <div className={`squad-member ${statusClass}`}>
                <span className="member-name">{member.name}</span>
                <span className="member-weapon">{member.weapon_display}</span>
                <HealthBar current={member.health} max={member.max_health} />
                <span className="member-status">{status}{duty}</span>
            </div>
        );
    };

    return (
        <div className="character-sheet forgotten-ruin">
            {showCustomization && sheet && sheet.has_squad && (
                <div className="modal-overlay">
                    <div className="modal-content customization-modal">
                        <SquadCustomization
                            squad={sheet.squad}
                            onUpdate={handleCustomizationUpdate}
                            onClose={() => setShowCustomization(false)}
                        />
                    </div>
                </div>
            )}

            {showGenerateModal && (
                <div className="modal-overlay">
                    <div className="modal-content generate-modal">
                        <div className="modal-header">
                            <h2>Generate New Squad</h2>
                            <button onClick={() => setShowGenerateModal(false)} className="btn-close">✕</button>
                        </div>
                        <div className="modal-body">
                            <p><strong>WARNING:</strong> This will delete your current squad and generate a completely new 9-person Ranger squad.</p>
                            <p>The new squad will follow the Forgotten Ruin squad composition:</p>
                            <ul>
                                <li>1 Squad Leader (Staff Sergeant) - You</li>
                                <li>Alpha Team: Team Leader, Automatic Rifleman, Grenadier, Rifleman/Medic</li>
                                <li>Bravo Team: Team Leader/Talker, Automatic Rifleman, Grenadier/Engineer, Rifleman/Medic</li>
                            </ul>
                            <p>All squad members will have randomly generated names, stats, and skills.</p>
                        </div>
                        <div className="modal-actions">
                            <button
                                onClick={handleGenerateSquad}
                                className="btn btn-danger"
                                disabled={generating}
                            >
                                {generating ? 'Generating...' : 'Generate New Squad'}
                            </button>
                            <button
                                onClick={() => setShowGenerateModal(false)}
                                className="btn btn-secondary"
                                disabled={generating}
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            )}

            <div className="tabs">
                <button
                    className={activeTab === 'squad' ? 'active' : ''}
                    onClick={() => setActiveTab('squad')}
                >
                    Squad Roster
                </button>
                <button
                    className={activeTab === 'stats' ? 'active' : ''}
                    onClick={() => setActiveTab('stats')}
                >
                    Personal Stats
                </button>
                <button
                    className={activeTab === 'inventory' ? 'active' : ''}
                    onClick={() => setActiveTab('inventory')}
                >
                    Inventory
                </button>
                <button
                    className={activeTab === 'quests' ? 'active' : ''}
                    onClick={() => setActiveTab('quests')}
                >
                    Missions
                </button>
                {sheet && sheet.has_squad && (
                    <>
                        <button
                            className="btn-customize"
                            onClick={() => setShowCustomization(true)}
                        >
                            ⚙️ Customize Squad
                        </button>
                        <button
                            className="btn-generate"
                            onClick={() => setShowGenerateModal(true)}
                        >
                            🔄 Generate New Squad
                        </button>
                    </>
                )}
            </div>

            {/* Squad Roster Tab */}
            {activeTab === 'squad' && sheet.has_squad && sheet.squad && (
                <div className="tab-content squad-tab">
                    <div className="squad-header">
                        <h2>RANGER SQUAD - {sheet.squad.squad_name.toUpperCase()}</h2>
                        <p>Callsign: {sheet.squad.callsign} | Commander: {sheet.character_name}</p>
                    </div>

                    <div className="squad-status">
                        <h3>Squad Status</h3>
                        <div className="status-grid">
                            <div>Personnel: {sheet.squad.alive_members_count}/{sheet.squad.total_members} alive ({sheet.squad.casualty_count} casualties)</div>
                            <div>Morale: {sheet.squad.morale}/100</div>
                            <div>Cohesion: {sheet.squad.cohesion}/100</div>
                            <div>Avg Health: {sheet.squad.average_health.toFixed(0)}%</div>
                        </div>
                    </div>

                    {/* Squad HQ */}
                    {sheet.squad.squad_leader && (
                        <div className="fire-team">
                            <h3>SQUAD HQ</h3>
                            <div className="team-roster">
                                <SquadMemberRow member={sheet.squad.squad_leader} />
                            </div>
                        </div>
                    )}

                    {/* Alpha Team */}
                    {sheet.squad.alpha_team && sheet.squad.alpha_team.length > 0 && (
                        <div className="fire-team">
                            <h3>ALPHA TEAM</h3>
                            <div className="team-roster">
                                {sheet.squad.alpha_team.map(member => (
                                    <SquadMemberRow key={member.id} member={member} />
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Bravo Team */}
                    {sheet.squad.bravo_team && sheet.squad.bravo_team.length > 0 && (
                        <div className="fire-team">
                            <h3>BRAVO TEAM</h3>
                            <div className="team-roster">
                                {sheet.squad.bravo_team.map(member => (
                                    <SquadMemberRow key={member.id} member={member} />
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Supplies */}
                    <div className="squad-supplies">
                        <h3>AMMUNITION & SUPPLIES</h3>
                        <div className="supplies-grid">
                            <div>5.56mm (M4A1): {sheet.squad.ammunition_556mm} rounds</div>
                            <div>5.56mm Belt (M249): {sheet.squad.ammunition_556mm_belt} rounds</div>
                            <div>Frag Grenades: {sheet.squad.grenades_frag}</div>
                            <div>40mm Grenades: {sheet.squad.grenades_40mm}</div>
                            <div>First Aid Kits: {sheet.squad.medkits}</div>
                        </div>
                    </div>

                    {/* Combat Record */}
                    <div className="combat-record">
                        <h3>COMBAT RECORD</h3>
                        <div>Total Kills: {sheet.squad.total_kills}</div>
                        <div>Missions Completed: {sheet.squad.missions_completed}</div>
                    </div>
                </div>
            )}

            {activeTab === 'squad' && !sheet.has_squad && (
                <div className="tab-content no-squad">
                    <h3>No Squad Assigned</h3>
                    <p>You currently don't have a Ranger squad. Generate a new 9-person squad to begin your mission.</p>
                    <button
                        className="btn btn-primary"
                        onClick={() => setShowGenerateModal(true)}
                    >
                        🔄 Generate Ranger Squad
                    </button>
                </div>
            )}

            {/* Personal Stats Tab */}
            {activeTab === 'stats' && (
                <div className="tab-content stats-tab">
                    <h2>{sheet.character_name}</h2>
                    <p>{sheet.description}</p>

                    <div className="stats">
                        <h3>Primary Stats</h3>
                        <ul>
                            <li>Level: {sheet.level}</li>
                            <li>Experience: {sheet.experience}</li>
                            <li>Health: {sheet.health} / {sheet.max_health}</li>
                            <li>Mana: {sheet.mana} / {sheet.max_mana}</li>
                        </ul>
                    </div>

                    <div className="attributes">
                        <h3>Attributes</h3>
                        <ul>
                            <li>Strength: {sheet.strength}</li>
                            <li>Dexterity: {sheet.dexterity}</li>
                            <li>Intelligence: {sheet.intelligence}</li>
                            <li>Constitution: {sheet.constitution}</li>
                        </ul>
                    </div>

                    <div className="currency">
                        <h3>Currency</h3>
                        <p>{sheet.currency} gold</p>
                    </div>
                </div>
            )}

            {/* Inventory Tab */}
            {activeTab === 'inventory' && (
                <div className="tab-content inventory-tab">
                    <div className="equipment">
                        <h3>Equipped Items</h3>
                        {sheet.equipped_items.length > 0 ? (
                            <ul>
                                {sheet.equipped_items.map((item, idx) => (
                                    <li key={idx}>
                                        <strong>{item.name}</strong> ({item.equipment_slot})
                                        <p>{item.description}</p>
                                        {item.stat_modifiers && Object.keys(item.stat_modifiers).length > 0 && (
                                            <ul>
                                                {Object.entries(item.stat_modifiers).map(([stat, value]) => (
                                                    <li key={stat}>{stat}: {value}</li>
                                                ))}
                                            </ul>
                                        )}
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p>No items equipped.</p>
                        )}
                    </div>

                    <div className="inventory">
                        <h3>Inventory</h3>
                        {sheet.inventory.length > 0 ? (
                            <ul>
                                {sheet.inventory.map((item, idx) => (
                                    <li key={idx}>
                                        <strong>{item.name}</strong> ({item.item_type})
                                        <p>{item.description}</p>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p>Inventory is empty.</p>
                        )}
                    </div>
                </div>
            )}

            {/* Missions/Quests Tab */}
            {activeTab === 'quests' && (
                <div className="tab-content quests-tab">
                    <h3>Active Missions</h3>
                    {sheet.active_quests.length > 0 ? (
                        <ul>
                            {sheet.active_quests.map((quest, idx) => (
                                <li key={idx}>
                                    <strong>{quest.title}</strong>
                                    <p>{quest.description}</p>
                                    <p>Status: {quest.status}</p>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>No active missions.</p>
                    )}
                </div>
            )}
        </div>
    );
};

export default CharacterSheet;
