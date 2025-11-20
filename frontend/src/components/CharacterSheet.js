import React, { useState, useEffect } from 'react';
import api from '../services/api';

const CharacterSheet = () => {
    const [sheet, setSheet] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchCharacterSheet = async () => {
            try {
                const response = await api.get('/api/v1/character/me/');
                setSheet(response.data);
            } catch (err) {
                setError('Failed to load character sheet.');
                console.error(err);
            }
        };

        fetchCharacterSheet();
    }, []);

    if (error) {
        return <div className="character-sheet error">{error}</div>;
    }

    if (!sheet) {
        return <div className="character-sheet loading">Loading...</div>;
    }

    return (
        <div className="character-sheet">
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

            <div className="equipment">
                <h3>Equipped Items</h3>
                {sheet.equipped_items.length > 0 ? (
                    <ul>
                        {sheet.equipped_items.map(item => (
                            <li key={item.name}>
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
                        {sheet.inventory.map(item => (
                            <li key={item.name}>
                                <strong>{item.name}</strong> ({item.item_type})
                                <p>{item.description}</p>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>Inventory is empty.</p>
                )}
            </div>

            <div className="quests">
                <h3>Active Quests</h3>
                {sheet.active_quests.length > 0 ? (
                    <ul>
                        {sheet.active_quests.map(quest => (
                            <li key={quest.title}>
                                <strong>{quest.title}</strong>
                                <p>{quest.description}</p>
                                <p>Status: {quest.status}</p>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No active quests.</p>
                )}
            </div>
        </div>
    );
};

export default CharacterSheet;
