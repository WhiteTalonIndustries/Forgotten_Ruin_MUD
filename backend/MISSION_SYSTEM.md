## Mission System Documentation

### Overview

The mission system provides a cinematic, three-act narrative structure for both public (server-impacting) and private (personal) missions. Missions follow a TV/movie format with hooks, three acts, and satisfying conclusions.

### Mission Types

#### Public Missions
- **Server Impact**: Affect game world state
- **Rewards**: Award XP, currency, items, and reputation
- **Persistence**: Tracked across all players
- **Consequences**: Failure can have lasting effects
- **Examples**: Main story missions, faction quests, zone events

#### Private Missions
- **Personal Narrative**: No server impact
- **No Rewards**: Don't award XP or assets
- **Learning Tool**: Perfect for practice and experimentation
- **Reusable**: Can be repeated without cooldown
- **Examples**: Training scenarios, personal challenges, story experiments

### Three-Act Structure

Every mission follows a cinematic narrative structure:

```
HOOK → ACT 1 → ACT 2 → ACT 3 → CONCLUSION
```

#### Hook
- **Purpose**: Grab player attention and provide motivation
- **Elements**:
  - Compelling title
  - Dramatic opening scene
  - Clear stakes
  - Emotional investment
- **Example**: "Captain Reynolds briefs you on enemy movements..."

#### Act 1: Setup
- **Purpose**: Establish situation and rising action
- **Elements**:
  - Journey to location
  - Initial challenges
  - Setup for main conflict
  - 2-3 objectives
- **Example**: Travel to observation point, establish overwatch

#### Act 2: Confrontation
- **Purpose**: Main conflict and complications
- **Elements**:
  - Primary challenge
  - Unexpected twists
  - Player choices
  - 3-4 objectives
- **Example**: Gather intelligence while avoiding enemy patrols

#### Act 3: Climax
- **Purpose**: Resolution of conflict
- **Elements**:
  - Climactic confrontation
  - Final challenges
  - Victory or defeat
  - 2-3 objectives
- **Example**: Extract under fire, deliver intelligence

#### Conclusion
- **Purpose**: Satisfying wrap-up
- **Types**:
  - Success: Full mission completion
  - Partial: Some objectives met
  - Failure: Mission failed
- **Example**: Debriefing with command, rewards distributed

### Mission Models

#### Mission (Base Definition)
```python
Mission:
  - key: Unique identifier
  - name: Display name
  - mission_type: recon, raid, rescue, etc.
  - is_public: True for server impact, False for private
  - difficulty: trivial to impossible
  - required_level: Minimum player level
  - required_squad_size: Minimum squad members

  # Narrative Structure
  - hook_title, hook_description
  - act1_title, act1_description, act1_objectives
  - act2_title, act2_description, act2_objectives
  - act3_title, act3_description, act3_objectives
  - conclusion_success, conclusion_failure, conclusion_partial

  # Rewards (public only)
  - reward_xp, reward_currency, reward_items, reward_reputation

  # Parameters
  - time_limit: Optional time limit in seconds
  - can_fail, can_abandon, is_repeatable
  - cooldown_hours: Time before repeating
```

#### PlayerMission (Instance)
```python
PlayerMission:
  - player: Player reference
  - mission: Mission reference
  - status: available, active, in_progress, completed, failed, abandoned
  - current_act: 0 (hook) to 4 (complete)

  # Progress
  - objectives_completed: Dict of objective completions
  - events_triggered: List of triggered events
  - choices_made: List of player choices

  # Timing
  - accepted_at, started_at, completed_at
  - time_limit_expires

  # Completion
  - success_level: full, partial, failure
  - rewards_claimed: Boolean
  - xp_awarded, currency_awarded, items_awarded
```

#### MissionEvent (Optional)
```python
MissionEvent:
  - mission: Parent mission
  - key: Event identifier
  - event_type: dialogue, combat, choice, discovery, ambush, etc.
  - act: Which act (1, 2, or 3)
  - trigger_type: When event occurs
  - trigger_conditions: Dict of trigger conditions
  - description: What happens
  - choices: Player choice options
  - outcomes: Dict of possible outcomes
```

### API Endpoints

#### List Missions
```
GET /api/v1/missions/
Returns: {
  available: [...],  // Missions player can start
  active: [...],     // Currently active missions
  completed: [...]   // Completed missions
}
```

#### Mission Detail
```
GET /api/v1/missions/<key>/
Returns: Full mission details including:
  - Hook and narrative
  - Current act (if active)
  - Objectives with completion status
  - Rewards (if public)
  - Conclusion (if completed)
```

#### Accept Mission
```
POST /api/v1/missions/<key>/accept/
Returns: Mission accepted with hook and Act 1 details
```

#### Complete Objective
```
POST /api/v1/player-missions/<id>/objectives/<key>/complete/
Returns: Progress update, auto-advances acts when complete
```

#### Abandon Mission
```
POST /api/v1/player-missions/<id>/abandon/
Returns: Confirmation (if allowed)
```

#### Create Private Mission
```
POST /api/v1/missions/create-private/
Body: {
  name, mission_type, difficulty,
  hook_title, hook_description,
  act1_title, act1_description, act1_objectives,
  act2_title, act2_description, act2_objectives,
  act3_title, act3_description, act3_objectives,
  conclusion_success, conclusion_failure
}
Returns: Created mission
```

#### Trigger Event
```
POST /api/v1/player-missions/<id>/events/<key>/trigger/
Returns: Event details and choices (if applicable)
```

#### Make Choice
```
POST /api/v1/player-missions/<id>/events/<key>/choice/
Body: { choice: "Choice text" }
Returns: Outcome of choice
```

### Creating Missions

#### Public Mission Example
```python
Mission.objects.create(
    key='mission_recon_north',
    name='Northern Recon Patrol',
    mission_type='recon',
    is_public=True,  # Server impact, awards XP

    difficulty='moderate',
    required_level=1,
    required_squad_size=2,

    given_by_npc=captain_reynolds,

    # Hook
    hook_title='Eyes on the Enemy',
    hook_description='Captain Reynolds needs intelligence...',

    # Act 1
    act1_title='Insertion',
    act1_description='You move north under cover...',
    act1_objectives=[
        {
            'key': 'reach_observation_point',
            'description': 'Reach the observation point',
            'required': True
        },
        {
            'key': 'establish_overwatch',
            'description': 'Set up observation post',
            'required': True
        }
    ],

    # Act 2
    act2_title='Intelligence Gathering',
    act2_description='From your position, you observe...',
    act2_objectives=[
        {
            'key': 'count_hostiles',
            'description': 'Count enemy forces',
            'required': True
        },
        {
            'key': 'identify_leaders',
            'description': 'Identify orc chieftain',
            'required': True
        }
    ],

    # Act 3
    act3_title='Exfiltration',
    act3_description='With intel gathered, extract...',
    act3_objectives=[
        {
            'key': 'withdraw_undetected',
            'description': 'Withdraw without detection',
            'required': True
        },
        {
            'key': 'return_to_outpost',
            'description': 'Return to base',
            'required': True
        }
    ],

    # Conclusions
    conclusion_success='Mission accomplished. Intelligence delivered...',
    conclusion_failure='Mission failed. Compromise...',

    # Rewards
    reward_xp=500,
    reward_currency=100,
    reward_items=[{'item_key': 'tactical_binoculars', 'quantity': 1}],

    # Parameters
    time_limit=7200,  # 2 hours
    can_fail=True,
    can_abandon=True,
    is_repeatable=True,
    cooldown_hours=24,
)
```

#### Private Mission Example
```python
Mission.objects.create(
    key='mission_personal_training',
    name='Personal Combat Training',
    mission_type='patrol',
    is_public=False,  # Private - no server impact

    difficulty='easy',
    required_level=1,

    hook_title='Test Your Skills',
    hook_description='You decide to test your combat skills...',

    # ... acts and objectives ...

    # No rewards for private missions
    reward_xp=0,
    reward_currency=0,
    reward_items=[],

    # Can be repeated freely
    is_repeatable=True,
    cooldown_hours=0,
)
```

### Mission Flow

#### Player Workflow
1. **Browse Available Missions**
   - GET /api/v1/missions/
   - See missions they qualify for

2. **View Mission Details**
   - GET /api/v1/missions/<key>/
   - Read hook and requirements

3. **Accept Mission**
   - POST /api/v1/missions/<key>/accept/
   - Creates PlayerMission instance
   - Starts at Hook (act 0)

4. **Complete Act 1**
   - POST objectives complete
   - System auto-advances to Act 2

5. **Complete Act 2**
   - POST objectives complete
   - System auto-advances to Act 3

6. **Complete Act 3**
   - POST objectives complete
   - Mission completes automatically
   - Rewards distributed (if public)

7. **Read Conclusion**
   - GET mission detail shows conclusion
   - Success/Partial/Failure based on completion

#### System Workflow
```
Mission Created → Available to Players
  ↓
Player Accepts → PlayerMission Created (status: active, act: 0)
  ↓
Player Reads Hook → Advances to Act 1 (act: 1, status: in_progress)
  ↓
Act 1 Objectives Complete → Auto-advance to Act 2 (act: 2)
  ↓
Act 2 Objectives Complete → Auto-advance to Act 3 (act: 3)
  ↓
Act 3 Objectives Complete → Mission Complete (act: 4, status: completed)
  ↓
Rewards Distributed (if public) → Conclusion Shown
```

### Objective Structure

Objectives are stored as JSON in each act:
```json
[
  {
    "key": "objective_unique_key",
    "description": "What player needs to do",
    "required": true  // false for optional objectives
  },
  {
    "key": "optional_objective",
    "description": "Bonus objective",
    "required": false
  }
]
```

### Time Limits

Missions can have optional time limits:
- Set `time_limit` in seconds
- PlayerMission tracks `time_limit_expires`
- System checks on objective completion
- Exceeding limit causes failure (if `can_fail=True`)

### Failure and Abandonment

#### Failure
- Only if `can_fail=True`
- Can be triggered by:
  - Time limit exceeded
  - Critical objective failed
  - Player death/defeat
  - Mission-specific conditions

#### Abandonment
- Only if `can_abandon=True`
- Player can quit mission
- No rewards
- Mission marked as abandoned

### Repeatability

#### One-Time Missions
```python
is_repeatable=False
```
- Can only be completed once
- Not available after completion

#### Repeatable Missions
```python
is_repeatable=True
cooldown_hours=24
```
- Can be repeated after cooldown
- Each instance is separate
- Cooldown prevents spam

### Events and Choices

Missions can include optional events:

#### Event Types
- **dialogue**: NPC conversations
- **combat**: Combat encounters
- **choice**: Player decisions
- **discovery**: Finding something
- **ambush**: Surprise enemy attack
- **reinforcements**: Ally or enemy reinforcements
- **betrayal**: NPC betrays player
- **custom**: Any custom event

#### Choice Events
```python
MissionEvent.objects.create(
    mission=mission,
    key='moral_choice',
    event_type='choice',
    act=2,
    trigger_type='objective_complete',
    trigger_conditions={'objective_key': 'find_enemy'},

    description='You find wounded enemy soldiers...',

    choices=[
        {
            'text': 'Help the wounded',
            'outcome': 'mercy',
            'requirements': {}
        },
        {
            'text': 'Eliminate them',
            'outcome': 'ruthless',
            'requirements': {}
        },
        {
            'text': 'Leave them',
            'outcome': 'neutral',
            'requirements': {}
        }
    ],

    outcomes={
        'mercy': {
            'description': 'You provide medical aid...',
            'effects': {'reputation_change': {'locals': +5}}
        },
        'ruthless': {
            'description': 'You eliminate the threat...',
            'effects': {'reputation_change': {'rangers': +2}}
        },
        'neutral': {
            'description': 'You move on...',
            'effects': {}
        }
    }
)
```

### Mission Variables

PlayerMission supports custom variables:
```python
player_mission.set_variable('enemies_killed', 0)
player_mission.increment_variable('enemies_killed')
count = player_mission.get_variable('enemies_killed', default=0)
```

Use for:
- Tracking enemy kills
- Counting rescued hostages
- Timer values
- Custom conditions

### Best Practices

#### Writing Missions

1. **Compelling Hook**
   - Start with drama
   - Establish stakes
   - Make it personal

2. **Progressive Difficulty**
   - Act 1: Setup and introduction
   - Act 2: Main challenge with twist
   - Act 3: Climactic resolution

3. **Clear Objectives**
   - Use active voice
   - Be specific
   - Mark optional objectives

4. **Satisfying Conclusion**
   - Address all story threads
   - Acknowledge player choices
   - Reward appropriately

5. **Balance**
   - Public missions: Meaningful rewards
   - Private missions: Focus on narrative
   - Consider difficulty vs rewards

#### Technical Considerations

1. **Objective Keys**
   - Use descriptive keys: `count_hostiles` not `obj1`
   - Be consistent across missions

2. **Time Limits**
   - Only use when narratively appropriate
   - Test actual time needed
   - Add buffer for player variance

3. **Required Squad Size**
   - Balance challenge with accessibility
   - Solo (1), Small Team (2-4), Full Squad (5+)

4. **Repeatability**
   - Daily missions: 24 hour cooldown
   - Weekly missions: 168 hour cooldown
   - Story missions: Not repeatable

5. **Failure Consequences**
   - Make failures meaningful
   - Don't permanently lock content
   - Allow recovery paths

### Example Mission Types

#### Recon Mission
- Stealth-focused
- Intelligence gathering
- Low combat
- Time-sensitive

#### Raid Mission
- High combat
- Objective destruction
- Scavenging
- Fast-paced

#### Rescue Mission
- Time-critical
- Protect NPCs
- Fighting withdrawal
- High stakes

#### Escort Mission
- Protect VIP
- Multiple checkpoints
- Ambush potential
- Patience required

#### Investigation Mission
- Clue gathering
- Dialogue-heavy
- Multiple solutions
- Mental challenge

### Testing Missions

```bash
# Create example missions
python create_example_missions.py

# List missions
curl http://localhost:8000/api/v1/missions/

# Get mission detail
curl http://localhost:8000/api/v1/missions/mission_recon_north/

# Accept mission (requires auth)
curl -X POST http://localhost:8000/api/v1/missions/mission_recon_north/accept/ \
  -H "Authorization: Bearer <token>"

# Complete objective
curl -X POST http://localhost:8000/api/v1/player-missions/<id>/objectives/reach_observation_point/complete/ \
  -H "Authorization: Bearer <token>"
```

### Future Enhancements

Potential additions to mission system:
- Dynamic mission generation from templates
- Branching narratives based on choices
- Multi-player cooperative missions
- Competitive PvP missions
- Seasonal event missions
- Faction-specific missions
- Procedurally generated missions
- Mission chains/campaigns

### Summary

The mission system provides:
- ✅ Cinematic three-act structure
- ✅ Public (server impact) and private (personal) missions
- ✅ Comprehensive objective tracking
- ✅ Event system with player choices
- ✅ Flexible reward system
- ✅ Time limits and failure states
- ✅ Repeatability with cooldowns
- ✅ RESTful API endpoints
- ✅ Full narrative framework

Perfect for creating immersive, story-driven content that feels like playing through a TV episode or movie.
