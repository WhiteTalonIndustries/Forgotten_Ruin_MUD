import React, { useState } from 'react';
import api from '../services/api';

const SquadCustomization = ({ squad, onUpdate, onClose }) => {
    const [editMode, setEditMode] = useState(null); // 'squad' | 'member-{id}'
    const [formData, setFormData] = useState({});
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    // Squad info editing
    const handleSquadEdit = () => {
        setEditMode('squad');
        setFormData({
            squad_name: squad.squad_name,
            callsign: squad.callsign
        });
        setError(null);
        setSuccess(null);
    };

    const handleSquadSave = async () => {
        try {
            const response = await api.patch('/squad/customize/', formData);
            setSuccess('Squad info updated successfully!');
            setEditMode(null);
            onUpdate(); // Refresh character sheet
            setTimeout(() => setSuccess(null), 3000);
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to update squad info');
        }
    };

    // Member editing
    const handleMemberEdit = (member) => {
        setEditMode(`member-${member.id}`);
        setFormData({
            member_id: member.id,
            name: member.name,
            secondary_duty: member.secondary_duty || ''
        });
        setError(null);
        setSuccess(null);
    };

    const handleMemberSave = async () => {
        try {
            const response = await api.patch(
                `/squad/member/${formData.member_id}/`,
                {
                    name: formData.name,
                    secondary_duty: formData.secondary_duty
                }
            );
            setSuccess('Squad member updated successfully!');
            setEditMode(null);
            onUpdate(); // Refresh character sheet
            setTimeout(() => setSuccess(null), 3000);
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to update squad member');
        }
    };

    const handleCancel = () => {
        setEditMode(null);
        setFormData({});
        setError(null);
    };

    const renderSquadEditor = () => (
        <div className="editor-form">
            <h3>Edit Squad Info</h3>
            <div className="form-group">
                <label>Squad Name:</label>
                <input
                    type="text"
                    value={formData.squad_name || ''}
                    onChange={(e) => setFormData({ ...formData, squad_name: e.target.value })}
                    maxLength={100}
                    placeholder="Enter squad name"
                />
            </div>
            <div className="form-group">
                <label>Callsign:</label>
                <input
                    type="text"
                    value={formData.callsign || ''}
                    onChange={(e) => setFormData({ ...formData, callsign: e.target.value })}
                    maxLength={50}
                    placeholder="Enter callsign"
                />
            </div>
            <div className="form-actions">
                <button onClick={handleSquadSave} className="btn btn-primary">Save</button>
                <button onClick={handleCancel} className="btn btn-secondary">Cancel</button>
            </div>
        </div>
    );

    const renderMemberEditor = (member) => (
        <div className="editor-form">
            <h3>Edit {member.name}</h3>
            <div className="form-group">
                <label>Name:</label>
                <input
                    type="text"
                    value={formData.name || ''}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    maxLength={100}
                    placeholder="Enter name (e.g., SGT Smith)"
                />
            </div>
            <div className="form-group">
                <label>Secondary Duty:</label>
                <select
                    value={formData.secondary_duty || ''}
                    onChange={(e) => setFormData({ ...formData, secondary_duty: e.target.value })}
                >
                    <option value="">None</option>
                    <option value="medic">Medic</option>
                    <option value="engineer">Engineer</option>
                    <option value="talker">Talker (Linguist)</option>
                </select>
                <small>Note: Only one member per fire team can have each duty</small>
            </div>
            <div className="member-info">
                <p><strong>Role:</strong> {member.role_display}</p>
                <p><strong>Fire Team:</strong> {member.fire_team_display}</p>
                <p><strong>Weapon:</strong> {member.weapon_display}</p>
            </div>
            <div className="form-actions">
                <button onClick={handleMemberSave} className="btn btn-primary">Save</button>
                <button onClick={handleCancel} className="btn btn-secondary">Cancel</button>
            </div>
        </div>
    );

    const renderMemberCard = (member) => {
        const isEditing = editMode === `member-${member.id}`;

        if (isEditing) {
            return (
                <div key={member.id} className="member-card editing">
                    {renderMemberEditor(member)}
                </div>
            );
        }

        return (
            <div key={member.id} className="member-card">
                <div className="member-header">
                    <h4>{member.name}</h4>
                    <button onClick={() => handleMemberEdit(member)} className="btn-edit">
                        ✏️ Edit
                    </button>
                </div>
                <div className="member-details">
                    <p><strong>Role:</strong> {member.role_display}</p>
                    <p><strong>Weapon:</strong> {member.weapon_display}</p>
                    {member.secondary_duty && (
                        <p><strong>Duty:</strong> {member.secondary_duty_display}</p>
                    )}
                    <p><strong>Health:</strong> {member.health}/{member.max_health}</p>
                </div>
                <div className="member-stats">
                    <span>STR {member.strength}</span>
                    <span>DEX {member.dexterity}</span>
                    <span>CON {member.constitution}</span>
                    <span>INT {member.intelligence}</span>
                </div>
            </div>
        );
    };

    return (
        <div className="squad-customization">
            <div className="customization-header">
                <h2>Squad Customization</h2>
                <button onClick={onClose} className="btn-close">✕</button>
            </div>

            {error && <div className="alert alert-error">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}

            {/* Squad Info Section */}
            <div className="customization-section">
                <div className="section-header">
                    <h3>Squad Identity</h3>
                    {editMode !== 'squad' && (
                        <button onClick={handleSquadEdit} className="btn btn-edit">
                            ✏️ Edit
                        </button>
                    )}
                </div>

                {editMode === 'squad' ? (
                    renderSquadEditor()
                ) : (
                    <div className="squad-info-display">
                        <p><strong>Name:</strong> {squad.squad_name}</p>
                        <p><strong>Callsign:</strong> {squad.callsign}</p>
                    </div>
                )}
            </div>

            {/* Squad Leader */}
            {squad.squad_leader && (
                <div className="customization-section">
                    <h3>Squad Leader (HQ)</h3>
                    <div className="members-grid">
                        {renderMemberCard(squad.squad_leader)}
                    </div>
                </div>
            )}

            {/* Alpha Team */}
            {squad.alpha_team && squad.alpha_team.length > 0 && (
                <div className="customization-section">
                    <h3>Alpha Team</h3>
                    <div className="members-grid">
                        {squad.alpha_team.map(member => renderMemberCard(member))}
                    </div>
                </div>
            )}

            {/* Bravo Team */}
            {squad.bravo_team && squad.bravo_team.length > 0 && (
                <div className="customization-section">
                    <h3>Bravo Team</h3>
                    <div className="members-grid">
                        {squad.bravo_team.map(member => renderMemberCard(member))}
                    </div>
                </div>
            )}

            <div className="customization-footer">
                <button onClick={onClose} className="btn btn-primary">Done</button>
            </div>
        </div>
    );
};

export default SquadCustomization;
