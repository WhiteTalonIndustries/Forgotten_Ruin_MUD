#!/usr/bin/env python
"""
Expand NPC Dialogue for Ranger Outpost Alpha

Creates rich, interactive dialogue trees for all NPCs with quest chains,
branching conversations, and dynamic responses based on player progress.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from game.models import NPC

# Color codes for output
class Color:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Color.GREEN}✓ {msg}{Color.END}")

def print_info(msg):
    print(f"{Color.BLUE}→ {msg}{Color.END}")

def print_section(msg):
    print(f"\n{Color.YELLOW}{'='*70}\n{msg}\n{'='*70}{Color.END}")

# Expanded dialogue trees for each NPC
expanded_dialogues = {
    'captain_reynolds': {
        'greeting': '''Ranger. The situation out there is FUBAR, but we hold the line. What do you need?''',

        'topics': {
            'situation': '''Ten thousand years after we left, and Earth is a fantasy hellscape. Orcs, magic,
dragons - the works. But we're US Army Rangers. We don't surrender, we adapt.

The Dark Army is massing. They want us eliminated. But every day we hold is a victory.
Every patrol we send out is a statement: Rangers don't quit.''',

            'orders': '''Right now we need intel. Patrol the perimeter, engage any orc scouts, and
report back. Every piece of information keeps us alive another day.

I've got specific missions if you're ready. Just ask about 'missions' and I'll brief you.''',

            'enemy': '''The Dark Army is massing to the north. Orcs mostly, but we've confirmed dark
wizard activity and wraith rider cavalry. They want this outpost eliminated.

We estimate 500+ hostiles within a day's march. They're organized - that makes them
dangerous. Traditional orc tactics are bad enough, but these ones are coordinated.

The Lich Pharaoh commands them from the west. That undead son of a bitch is the real
threat. The orcs are just the hammer he's swinging at us.''',

            'magic': '''Yeah, magic is real. Took me a month to accept that. Now I treat it like any
other weapon system. Learn it, counter it, use it if we can.

Doc Martinez has figured out divine healing. Some of our blades have been enchanted.
We're adapting. That's what Rangers do.

Dark wizards throw lightning and fire. It's devastating, but they're squishy. Headshots
work just fine. Learn to prioritize targets and you'll survive.''',

            'missions': '''I've got several operations that need attention:

RECON PATROL: Scout the northern orc encampments. Count hostiles, identify leaders,
report defensive positions. Ask about 'recon' for details.

SUPPLY RAID: Hit an orc supply depot. We need their resources, and denying them
supplies weakens their offensive capability. Ask about 'raid' for details.

RESCUE OPERATION: We have a Ranger patrol pinned down. They need extraction.
Time sensitive. Ask about 'rescue' for details.

WIZARD HUNT: A dark wizard coven is conducting rituals. We need them neutralized
before they complete whatever they're planning. Ask about 'wizard' for details.

What's your poison, Ranger?''',

            'recon': '''Reconnaissance mission to the northern orc encampments.

MISSION BRIEF:
- Proceed north to grid reference 437-862
- Observe orc positions without engaging
- Count hostiles, identify leaders, note defensive positions
- Report back with intelligence

RULES OF ENGAGEMENT:
- Stealth is priority one
- Break contact if detected
- Do not engage unless absolutely necessary
- Conserve ammunition

This is a pure intel-gathering op. We need eyes on the enemy, not a firefight.
Can you handle it?''',

            'raid': '''Supply raid on an orc logistics depot.

MISSION BRIEF:
- Target is a fortified supply depot at grid reference 445-870
- Estimated 20-30 orc guards
- Mission objectives: Destroy supplies, eliminate guards, scavenge what we can use
- Explosives authorized

RULES OF ENGAGEMENT:
- Weapons free on all hostiles
- Controlled fire, make shots count
- Grab any useful supplies before exfil
- Set charges on their ammo dump before you leave

This is a direct action mission. Get in, hit them hard, and get out. You ready?''',

            'rescue': '''Emergency rescue operation for pinned-down patrol.

MISSION BRIEF:
- Havoc-One-Three is pinned down at grid reference 429-856
- 4 Rangers, 2 wounded, running low on ammunition
- Surrounded by orc forces, estimated 30+ hostiles
- Time sensitive - they can't hold much longer

RULES OF ENGAGEMENT:
- Weapons free, priority is Ranger extraction
- Expect heavy resistance
- Coordinate with the pinned squad via radio
- Provide covering fire and get them out

Our people are in trouble. Rangers don't leave Rangers behind. Move fast.''',

            'wizard': '''Neutralize dark wizard ritual site.

MISSION BRIEF:
- Intel reports a dark wizard coven conducting rituals at grid reference 441-865
- 4-6 wizards confirmed, unknown orc security force
- The ritual must be stopped - if they complete it, we're in serious trouble
- Prioritize wizard targets

RULES OF ENGAGEMENT:
- Wizards are primary targets - take them out first
- Interrupt any ritual casting immediately
- Expect magical attacks: lightning, fire, death magic
- Iron weapons are more effective against magic users

This is high-risk. Wizards are dangerous, but we can't let them complete their ritual.
You up for it?''',

            'rangers': '''Rangers lead the way. That's not just a motto - it's who we are.

We're the best light infantry in the world. When the situation is impossible, when
everyone else has failed, they call in the Rangers. We've never failed a mission.

This situation is FUBAR. We're ten thousand years from home, fighting orcs and wizards
in a fantasy hellscape. But we're still Rangers. We adapt, we fight, and we hold the line.

Every man and woman in this outpost is a volunteer. We knew the risks. Now we're here,
and we're not going anywhere. This is our stand.''',

            'outpost': '''Ranger Outpost Alpha is our main base of operations. We built it from scratch
after we realized we weren't going home.

The fortifications are a mix of modern field engineering and improvised medieval
defenses. Hesco barriers, sandbags, and a wooden palisade. It's not Fort Benning,
but it keeps the orcs out.

We've got around 100 Rangers here, plus some civilian refugees under our protection.
We run continuous patrols, maintain watch rotations, and train constantly.

This outpost is more than just a base - it's proof that Rangers don't quit. It's a
statement to the Dark Army: you want us? Come and get us.''',

            'training': '''Talk to SSG Kim about training. She runs the combat programs with an iron fist.

You need both modern tactics and melee combat skills to survive out there. Kim will
make sure you have both.''',

            'supplies': '''SGT Walsh runs the quartermaster's office. Everything is rationed - we can't
waste resources.

Bring him salvage and he'll trade for supplies. We need everything: ammunition, medical
supplies, food, even scrap metal for repairs.

Remember: supply discipline keeps us alive. Don't waste ammunition. Don't take more
than you need. We're all in this together.''',

            'medical': '''SFC Martinez is our senior medic. He's part doctor, part wizard at this point.

He combines modern medicine with magical healing. Sounds crazy, but it works. Prayer
works here. Healing potions are real. Doc uses everything he can to keep Rangers alive.

If you're hurt, see Doc. Don't try to tough it out. A minor wound can kill you out here
if it gets infected.''',
        }
    },

    'sergeant_kim': {
        'greeting': '''You here to train or to waste my time? This isn't a game - what you learn here keeps you breathing.''',

        'topics': {
            'training': '''We drill modern tactics and melee combat. You need both out there. Orcs don't go
down from one round, and they love close combat. Be ready.

I run three training programs:

MARKSMANSHIP: Modern rifle skills. Controlled pairs, target prioritization, tactical
reloads. Ask about 'marksmanship' for details.

CLOSE COMBAT: Blade work and hand-to-hand. When your rifle runs dry or magic disables
it, you need a blade. Ask about 'melee' for details.

TACTICS: Squad-level maneuvers, room clearing, ambush drills. Ask about 'tactics' for details.

What do you need to work on?''',

            'marksmanship': '''Marksmanship training - making every shot count.

In our old world, ammunition was plentiful. Here, every round is precious. You need to
make shots count.

FUNDAMENTALS:
- Controlled pairs: Two shots center mass
- Aim for center mass on orcs, head shots on wizards
- Know your range - M4A1 is effective to 500 meters
- Tactical reloads: Don't run your magazine dry

ENEMY-SPECIFIC:
- Orcs: Tough, but not invincible. 2-3 rounds center mass will drop them
- Trolls: Keep firing, aim for vitals, they regenerate so keep shooting
- Wizards: Head shots. They're squishy. One round ends them
- Wraith Riders: Iron rounds work better, aim for the rider not the mount

Practice on the range. Get comfortable with your weapon. It's what keeps you alive.''',

            'melee': '''Close combat training - blade work and hand-to-hand fighting.

Ammunition runs out. Magic can disable firearms. When that happens, you need a blade
and the skill to use it.

BLADE FUNDAMENTALS:
- Keep your blade sharp - blunt weapons are useless
- Thrust to vitals: throat, heart, gut
- Slash to disable: arms, legs, neck
- Maintain distance - longer reach is an advantage

ORC COMBAT:
- They're strong and aggressive
- Use their momentum against them
- Go for vitals - they can take punishment
- Don't try to overpower them, outfight them

I teach a hybrid system: military combatives mixed with practical sword work. It's not
pretty, but it's effective. Come to the training grounds and I'll work with you.''',

            'tactics': '''Tactical training - squad-level operations.

Modern Ranger tactics still work, even against orcs and wizards. Fire and maneuver.
Suppression and assault. Cover and concealment. The fundamentals don't change.

SQUAD TACTICS:
- Maintain dispersion - don't bunch up
- Use cover and concealment
- Communicate constantly
- Support by fire while maneuvering

ENEMY-SPECIFIC TACTICS:
- Orcs: They charge. Use that. Let them come to your kill zone
- Wizards: Prioritize them. One wizard can kill a whole squad
- Wraith Riders: They flank fast. Watch your sectors, maintain all-around security
- Mixed forces: Kill wizards first, suppress orcs, watch for cavalry

We run tactical drills constantly. Join the next one. Experience beats theory every time.''',

            'combat': '''Modern doctrine still applies: fire discipline, cover, maneuver. But add in defending
against magical attacks and fighting with blades. It's brutal.

The key is adaptation. Yes, you're fighting orcs and wizards now. But the fundamentals
remain: shoot straight, move smart, stay alive.

Every Ranger here has killed in combat. We've all adapted to this nightmare world.
You can too. Just train hard and stay focused.''',

            'survival': '''First rule: Don't go solo. Second rule: Conserve ammunition. Third rule: Always
have a blade ready. Magic can disable your rifle, but a sword doesn't jam.

SURVIVAL BASICS:
- Never patrol alone - minimum two-person teams
- Check your equipment before every mission
- Carry backup weapons - rifle, pistol, blade
- Know your escape routes
- Report in regularly via radio

COMMON MISTAKES:
- Underestimating orcs - they're savage but not stupid
- Ignoring wizard threats - they'll kill you from range
- Running out of ammunition - carry enough, conserve fire
- Going loud when stealth is smarter - don't pick fights you don't need

Rangers who follow these rules tend to survive. Those who don't... well, we remember
them.''',

            'rangers': '''Rangers are the best infantry in the world. We volunteered for this. We knew the
risks. Now we're here, and we're adapting.

I've trained soldiers for ten years. This is the toughest training environment I've
ever seen. But Rangers rise to the challenge. We always do.

Every Ranger here is willing to die for the soldier next to them. That's not rhetoric -
it's truth. We look out for each other. That's how we survive.''',

            'orcs': '''Orcs are savage, strong, and they love close combat. But they're not invincible.

CHARACTERISTICS:
- 6-7 feet tall, green-skinned, tusked
- Extremely strong and aggressive
- Prefer melee but will use crude ranged weapons
- Tough - can take multiple rounds before going down

TACTICS:
- They charge aggressively
- Limited small-unit tactics, but they follow leaders
- Swarm attacks - they'll try to overwhelm you with numbers
- Fearless in combat, will fight to the death

COUNTERS:
- Maintain distance, use your rifle advantage
- Controlled pairs - 2-3 rounds center mass
- Target leaders first - it disrupts their coordination
- Fall back if they close distance, don't let them swarm you
- Have a blade ready for close combat

Know your enemy. Respect their capabilities. Then kill them.''',

            'respect': '''I have no respect for weakness. Out here, weakness kills you and the Rangers around you.

I respect competence. Skill. Dedication. The willingness to train hard so you fight easy.

Every Ranger in this outpost has earned my respect by surviving in this hellscape.
By not quitting when things got impossible. By keeping their skills sharp and their
heads in the game.

You want my respect? Train hard. Fight smart. Stay alive. That's all I ask.''',
        }
    },

    'doc_martinez': {
        'greeting': '''Need patching up? I handle everything from bullet wounds to curse removal. Modern combat medicine adapted for a fantasy war zone.''',

        'topics': {
            'healing': '''I treat conventional injuries and magical ones using modern medical protocols.

TRAUMA CARE:
- Gunshot wounds: standard TCCC protocols still apply
- Blast injuries: treat for hemorrhage, airways, breathing
- Broken bones: splinting, reduction, immobilization
- Burns: conventional and magical burns require different treatment

SURGICAL CAPABILITIES:
- Field surgery when necessary
- Limited anesthesia - mostly local blocks
- Suturing, debridement, emergency procedures
- Post-op care with limited resources

MEDICATIONS I STOCK:
- Antibiotics: Cipro, Doxy, Augmentin (limited quantities)
- Pain management: Morphine, Fentanyl lollipops, Tylenol, Ibuprofen
- IV fluids: Lactated Ringer's, Normal Saline
- Hemostatic agents: Combat Gauze, QuikClot
- Antidotes: for specific venoms and toxins

MAGICAL TREATMENT:
- Divine healing for critical cases
- Curse removal protocols
- Treatment for necrotic damage

Modern medicine first. Magic when medicine isn't enough.''',

            'supplies': '''Medical supplies are critically limited. Every item counts.

CURRENT INVENTORY:
- Trauma kits: tourniquets, Israeli bandages, hemostatic agents
- Antibiotics: 6-month supply at current usage rate
- IV supplies: adequate for now, but non-renewable
- Pain medication: morphine and fentanyl in limited quantities
- Surgical supplies: sutures, scalpels, instruments (reusable)
- Bandages and dressings: constantly running low

CONSERVATION MEASURES:
- Reuse and sterilize when possible
- Ration antibiotics strictly (only for serious infections)
- Save morphine for severe trauma
- Use local substitutes when available

WHAT I NEED:
- Medical salvage from old world ruins
- Pharmaceutical supplies (any condition)
- Surgical equipment
- Anything sterile or sterilizable

Bring me medical salvage and I'll trade supplies or treatment credit.''',

            'magic': '''Magic is real, and it causes injuries I never trained for. But I've adapted.

MAGICAL INJURIES:
- Curses: cause various symptoms, require dispel magic
- Lightning burns: from dark wizard attacks, deeper than thermal burns
- Necrotic damage: tissue death from undead or death magic
- Magical poison: conventional antidotes don't work

TREATMENT PROTOCOLS:
- Curses: I can use divine magic to dispel most
- Magical burns: treat symptomatically, monitor for secondary effects
- Necrotic damage: surgical debridement plus divine healing
- Magical poison: depends on source, some require specific counter-agents

DIVINE HEALING:
- Yes, prayer works here
- I can channel healing for serious injuries
- Limited uses - it's exhausting
- Works on physical trauma and some magical conditions

I'm still a medic first. Science and evidence-based medicine. But I've learned to use
every tool available, including magic.''',

            'medications': '''My pharmaceutical inventory is limited and irreplaceable.

ANTIBIOTICS:
- Cipro 500mg: for general infections
- Doxycycline: respiratory infections, some venoms
- Augmentin: for complicated infections
- Availability: CRITICAL - running low

PAIN MANAGEMENT:
- Morphine: severe pain, limited supply
- Fentanyl lollipops: breakthrough pain, field use
- Tylenol/Ibuprofen: mild to moderate pain
- Local anesthetics: lidocaine for procedures

EMERGENCY MEDICATIONS:
- Epinephrine: anaphylaxis, cardiac arrest
- Atropine: chemical exposure, some poisons
- Naloxone: opioid overdose
- Various antidotes: snakebite, scorpion, toxins

RATIONING:
- Life-threatening conditions get priority
- Minor infections: let immune system handle it
- Pain management: tough it out unless severe
- No prophylactic antibiotics

Every pill I give out is one less for the next casualty. I ration strictly.''',

            'treatment': '''Treatment philosophy: modern medicine adapted for impossible circumstances.

TRIAGE SYSTEM:
- Immediate: life-threatening, can be saved
- Delayed: serious but stable
- Minor: walking wounded
- Expectant: unsurvivable with available resources

TREATMENT PRIORITIES:
1. Control hemorrhage (tourniquets, pressure, hemostatic agents)
2. Ensure airway and breathing
3. Treat for shock (IV fluids, keep warm)
4. Prevent infection (clean wounds, antibiotics when critical)
5. Pain management (as supplies allow)
6. Definitive care (surgery, advanced treatment)

MAGICAL COMPLICATIONS:
- Some injuries require magical treatment
- I use divine healing for otherwise fatal injuries
- Curse removal when necessary
- Adapt protocols based on what works

We save who we can with what we have. That's combat medicine.''',

            'casualties': '''We've taken casualties. Every loss weighs on me.

KILLED IN ACTION:
- Combat injuries I couldn't treat
- Magical attacks beyond my capabilities
- Overwhelming trauma (too many casualties at once)
- Delayed treatment (couldn't reach them in time)

NON-BATTLE LOSSES:
- Infections when antibiotics ran out
- Complications from injuries
- Disease (limited prevention capabilities)
- Magical curses I couldn't remove

LESSONS LEARNED:
- Built treatment protocols for magical injuries
- Learned divine healing to save critical cases
- Improved triage and casualty evacuation
- Better inventory management

Our casualty rate is improving. I'm getting better at keeping Rangers alive in this
nightmare world. But I'll never forget the ones I couldn't save.''',

            'rangers': '''Rangers are the toughest patients and the worst patients simultaneously.

TOUGH:
- Will fight through injuries that would drop anyone else
- High pain tolerance
- Strong will to survive
- Physical conditioning helps recovery

STUBBORN:
- Downplay injuries to stay in the fight
- Refuse evacuation
- Skip follow-up care
- Return to duty too early

I have to fight Rangers to get them to accept treatment sometimes. They'll lie about
symptoms, minimize pain levels, do anything to avoid being pulled from missions.

I respect their dedication. But my job is keeping them alive, not enabling their
death wishes. Sometimes I pull rank. Sometimes I report them to Captain Reynolds.

Whatever it takes to keep them breathing.''',

            'advice': '''Medical advice for Rangers in the field:

1. CARRY YOUR IFAK (Individual First Aid Kit):
   - Tourniquet (CAT or SOFTT)
   - Pressure dressing (Israeli bandage)
   - Hemostatic gauze (Combat Gauze)
   - Nasopharyngeal airway
   - Chest seal (for sucking chest wounds)

2. KNOW YOUR TCCC (Tactical Combat Casualty Care):
   - Massive hemorrhage: tourniquet high and tight
   - Airway: NPA or surgical airway if trained
   - Breathing: chest seal for penetrating wounds
   - Circulation: IV access if possible
   - Hypothermia prevention: keep casualties warm

3. COMBAT MEDIC WHEN AVAILABLE:
   - Each squad should have a designated combat medic
   - They carry additional supplies
   - They have advanced training

4. WHEN TO EVACUATE:
   - Penetrating torso wounds
   - Uncontrolled hemorrhage
   - Head trauma with LOC
   - Magical injuries (curses, necrotic damage)
   - Any injury you can't treat in the field

5. PREVENT INFECTIONS:
   - Clean wounds thoroughly
   - Don't close dirty wounds
   - Change dressings regularly
   - Report signs of infection immediately (red, hot, swollen, pus)

Stay safe. Follow protocols. Don't make me patch you up.''',
        }
    },

    'specialist_jackson': {
        'greeting': '''Need weapons maintenance? Modifications? I keep Ranger equipment combat-ready. What do you need?''',

        'topics': {
            'repairs': '''I can repair any weapon or armor. Modern stuff is easy if I have parts. Old-world
scavenged gear I can usually figure out.

WHAT I REPAIR:
- M4A1 carbines: cleaning, parts replacement, barrel swaps
- M249 LMGs: gas system, barrels, feed trays
- Pistols: Glocks mostly, standard maintenance
- Armor: plate carriers, plates, load-bearing equipment
- Blades: sharpening, handle repair, balance adjustment

COST:
- Free for critical repairs
- Materials cost for major repairs
- Bring me salvage and I'll cut you a deal

Keep your equipment maintained. A malfunction in combat can get you killed.''',

            'modifications': '''I add bayonet lugs to carbines, reinforce armor with scavenged plates, even try
to enchant equipment. Gotta use every advantage.

AVAILABLE MODS:
- Bayonet lugs: Turn your rifle into a spear for close combat
- Extended magazines: When I can build them
- Suppressor threading: For stealth operations
- Optics mounting: Red dots, scopes, whatever we can scavenge
- Armor reinforcement: Add salvaged plates for better protection
- Blade modifications: Better grip, balanced for throwing, etc.

EXPERIMENTAL:
- Enchanted blades: Working with local magic users
- Rune-etched armor: Might provide magical protection
- Blessed ammunition: Allegedly works better against undead

Some of this is proven. Some is experimental. But we try everything.''',

            'forge': '''Yeah, I learned blacksmithing. When you can't order parts from supply, you make them.
I forge blades too - Rangers need backup weapons.

HOW IT WORKS:
- I scavenge steel from ruins
- Use a coal forge - old-school but effective
- Hammer out parts and blades
- Heat treat and finish

WHAT I FORGE:
- Replacement parts for weapons
- Combat knives - simple but effective
- Swords - when Rangers need them
- Arrowheads and bolts - for scavenged crossbows
- Tools and hardware

It's not high-tech, but it works. Rangers can't afford to be picky. If it functions,
it's good enough.''',

            'enchantment': '''I'm experimenting with magical weapon enhancement. Results are... mixed.

THE THEORY:
- Some metals hold enchantments better than others
- Runes carved into blades can add properties
- Blessings from priests work on weapons
- Some creatures' parts can enhance weapons

WHAT I'VE DONE:
- Blessed blades: Work better against undead
- Rune-etched swords: One seems to cut better, might be placebo
- Silver-inlaid knife: Allegedly works on werewolves (unconfirmed)
- Fire-enchanted sword: Glows and burns, definitely works

LIMITATIONS:
- I'm not a wizard, I'm a gunsmith learning magic
- Some enchantments fade over time
- Quality varies wildly
- It's expensive

If you want an enchanted weapon, bring me materials and I'll try. No guarantees.''',

            'ammunition': '''Ammunition is our most precious resource. We're shooting more than we're finding.

CURRENT STOCKPILE:
- 5.56mm: Main rifle ammunition, supply is critical
- 7.62mm: For M249s, even more limited
- 9mm: Pistol ammunition, limited supply
- 40mm: Grenades for M320 launchers, very limited
- .50 cal: For the few heavy weapons we have, extremely rare

CONSERVATION:
- Controlled pairs, don't spray and pray
- Make every shot count
- Use blades when possible to conserve ammo
- Scavenge from dead enemies when you can

ALTERNATIVES:
- I'm experimenting with reloading brass
- Salvaging gunpowder from old sources
- Making crossbow bolts as a backup
- Arrows for scavenged bows

We need to find more ammunition or find alternatives. This is a critical problem.''',

            'scavenging': '''Bring me salvage and I'll make it worth your while.

WHAT I NEED:
- Steel and metal: For forging and repairs
- Weapon parts: Modern or old-world
- Ammunition: Any caliber
- Tools: Anything useful
- Magical components: Gems, runes, enchanted items

WHAT I'LL PAY:
- Trade credit for supplies
- Weapon modifications
- Custom gear
- Priority service

This world is full of ruins. Old-world technology is out there. Bring me what you find
and I'll put it to use.''',

            'rangers': '''Rangers need reliable equipment. That's my job.

I was a 91F - small arms repairer - before we got stranded. I kept weapons running.
Now I do that plus blacksmithing, enchanting, and whatever else keeps Rangers armed.

Every weapon I repair might save a Ranger's life. Every blade I forge might be the
difference in close combat. I take that seriously.

Rangers depend on me. I won't let them down.''',

            'advice': '''Equipment advice for Rangers:

1. MAINTAIN YOUR WEAPONS:
   - Clean after every mission
   - Check for damage or wear
   - Replace parts before they fail
   - Bring me anything that's not right

2. CARRY BACKUP WEAPONS:
   - Rifle, pistol, and blade minimum
   - Magic can disable firearms
   - Ammunition runs out
   - Be prepared

3. KNOW YOUR EQUIPMENT:
   - How to clear malfunctions
   - How to field strip and reassemble
   - How to make field repairs
   - When to bring it to me

4. UPGRADE WHEN POSSIBLE:
   - Better optics improve accuracy
   - Bayonet lugs add close combat capability
   - Armor modifications save lives
   - Enchantments provide an edge

5. RESPECT YOUR GEAR:
   - It keeps you alive
   - We can't replace it easily
   - Treat it well

Good equipment and good maintenance. That's the formula.''',
        }
    },

    'sergeant_walsh': {
        'greeting': '''Quartermaster. Here for supplies? Everything is rationed and tracked. What do you need?''',

        'topics': {
            'supplies': '''We have 5.56mm ammunition, MREs, medical supplies, and scavenged equipment.
Everything is rationed - take only what you need for your mission.

AVAILABLE SUPPLIES:
- 5.56mm ammunition: 30 rounds per Ranger per mission
- 7.62mm ammunition: For SAW gunners only
- MREs: 3 per day for extended missions
- Water purification tablets
- Basic medical supplies
- Rope, tape, basic gear

RATIONING:
- Based on mission requirements
- Captain Reynolds approves special requests
- No hoarding - supplies are for everyone
- Turn in unused supplies after missions

We're not running a store. This is survival logistics. Take what you need, not what
you want.''',

            'salvage': '''Bring me salvage from the ruins and I'll trade for it. Old-world tech, monster parts,
anything useful. We need resources.

WHAT I BUY:
- Old-world technology: Electronics, tools, weapons
- Precious metals: Gold, silver, copper
- Gems and jewelry: Trade goods
- Monster parts: Some have value to locals
- Weapons and armor: From enemy dead
- Anything rare or valuable

PRICES:
- Fair market value
- I pay in trade credit or supplies
- Rangers get better rates than civilians
- Bulk salvage gets bonus credit

This world is full of ruins and dead enemies. Loot everything. Bring it to me.
I'll find a use for it or trade it away.''',

            'trade': '''I buy and sell at fair rates. Rangers get first priority. Civilians can trade after
Ranger needs are met.

HOW IT WORKS:
- I maintain a inventory of supplies
- Rangers can purchase at cost
- Civilians pay market rates
- I trade with local settlements for supplies we need

WHAT I SELL:
- Basic supplies: Food, water, gear
- Ammunition: Limited quantities
- Weapons and armor: Scavenged gear
- Healing potions: Bought from local healers
- Miscellaneous equipment

WHAT I BUY:
- Anything I can resell or trade
- Salvage from missions
- Loot from combat
- Resources from gathering

Come to me for supplies before missions. Turn in salvage after. Simple system.''',

            'economy': '''We run a mixed economy: military logistics plus market trading.

INTERNAL (RANGER):
- Supplies issued based on need
- Basic necessities provided
- Special requests go through command
- Combat salvage can be kept or sold

EXTERNAL (CIVILIANS & LOCALS):
- We trade for supplies we can't produce
- I maintain relationships with local merchants
- We protect trade caravans in exchange for goods
- Market rates for civilian trading

CHALLENGES:
- Limited production capability
- Scarcity of critical supplies
- Dependence on scavenging
- Trade with locals who fear us

We make it work. Rangers don't starve and we keep enough supplies for operations.
That's what matters.''',

            'local_trade': '''We trade with local settlements. It's... complicated.

TRADING PARTNERS:
- Small villages under Ranger protection
- Independent merchants
- Healers and alchemists
- Occasionally neutral factions

WHAT WE TRADE:
- Military protection
- Scavenged old-world technology
- Monster parts from kills
- Captured weapons from enemies

WHAT WE GET:
- Food and water
- Healing potions
- Local goods
- Intelligence on enemy movements

COMPLICATIONS:
- Many locals fear us (armed strangers from the past)
- Dark Army threatens anyone who trades with us
- Currency differences (they use gold, we use trade credit)
- Cultural misunderstandings

But trade keeps us supplied and builds relationships. Over time, more locals are
willing to work with us.''',

            'food': '''Food situation is stable but not ideal.

WHAT WE HAVE:
- MREs: Original supply, running low
- Local food: Bought or traded from settlements
- Hunted game: Rangers supplement with hunting
- Foraged plants: Some Rangers know edible plants

CONCERNS:
- MREs will run out eventually
- Dependent on local trade
- Some local food is... strange
- Hunting takes time and resources

LONG-TERM:
- Need to establish farming
- Build better trade relationships
- Learn to live off the land
- Reduce dependence on MREs

We won't starve, but we're transitioning to local food sources. It's an adjustment.''',

            'rangers': '''Rangers are disciplined. They follow supply protocols. Makes my job easier.

In a regular unit, I'd be dealing with missing gear, unauthorized trading, supply theft.
Not with Rangers. They understand supply discipline keeps everyone alive.

When I say ammunition is rationed, Rangers accept it. When I say turn in unused supplies,
they comply. No arguments, no theft, no bullshit.

That's Ranger professionalism. Even ten thousand years from home, in a fantasy hellscape,
they maintain standards.

Makes me proud to serve with them.''',

            'advice': '''Quartermaster advice:

1. TAKE ONLY WHAT YOU NEED:
   - Don't hoard supplies
   - Turn in unused gear after missions
   - Let others access what they need

2. SCAVENGE EVERYTHING:
   - Loot enemy dead
   - Search ruins
   - Bring salvage to me for credit
   - Waste nothing

3. MAINTAIN YOUR GEAR:
   - Damaged gear costs resources to replace
   - Take care of what you have
   - Report losses properly

4. TRADE SMART:
   - Don't sell critical gear
   - Know the value of what you have
   - Build relationships with merchants
   - Rangers help each other with good deals

5. PLAN AHEAD:
   - Request supplies before missions
   - Don't wait until you're out
   - Anticipate needs
   - Coordinate with your squad

Supply discipline is survival. Remember that.''',
        }
    },

    'corporal_chen': {
        'greeting': '''Intel shop. I track enemy movements and capabilities. What do you need to know?''',

        'topics': {
            'enemy': '''Dark Army forces are massing north. We've identified orc warbands, dark wizard covens,
and wraith rider cavalry. They're organized - that makes them dangerous.

CURRENT INTELLIGENCE:

ORC FORCES:
- Estimated 500+ within strike distance
- Multiple warbands, each 30-50 strong
- Coordinated by chieftains
- Supported by dark wizards

DARK WIZARDS:
- At least 3 confirmed covens
- Each coven has 4-6 wizards
- Conducting rituals (purpose unknown)
- Provide magical support to orc forces

WRAITH RIDERS:
- Fast cavalry units
- Estimated 50+ riders
- Conduct raids and reconnaissance
- Extremely dangerous

LICH PHARAOH:
- Commands the Dark Army
- Location: Western territories
- Capabilities: Unknown, presumed extreme
- Rarely observed directly

The big picture: We're significantly outnumbered and they're organized. This isn't
random monster attacks - it's a coordinated military campaign.''',

            'intel': '''Every patrol reports back. Every encounter gets analyzed. I build the big picture
from the pieces. That's how we stay ahead.

INTELLIGENCE CYCLE:
1. Collection: Patrols observe and report
2. Processing: I collate and organize data
3. Analysis: Identify patterns and threats
4. Dissemination: Brief command and Rangers

SOURCES:
- Ranger patrols (primary source)
- Local informants (limited but valuable)
- Enemy prisoners (rare - orcs don't surrender)
- Captured documents (when available)
- Aerial reconnaissance (when we can risk it)

CHALLENGES:
- Limited resources for collection
- Enemy uses magic (hard to anticipate)
- Hostile territory limits reconnaissance
- Some threats are unknown (dragons, etc.)

But intelligence is our edge. We're outnumbered, so we need to be smarter.''',

            'magic': '''I study magical threats like I would any other weapon system. Document capabilities,
identify counters, develop tactics. Magic isn't mystical - it's just another tool to
understand.

MAGICAL THREATS ANALYSIS:

DARK WIZARD CAPABILITIES:
- Lightning spells: Range 50-100m, lethal
- Fire spells: Area effect, devastating
- Death magic: Necrotic damage, hard to treat
- Curses: Various effects, require dispel

COUNTERS:
- Priority targeting: Kill wizards first
- Interrupt casting: They need time to cast
- Cover: Magical attacks can be blocked
- Dispel magic: Doc Martinez can remove some curses

WRAITH CAPABILITIES:
- Intangibility: Can phase through objects
- Fear effect: Causes panic
- Life drain: Touch attack
- Speed: Extremely fast

COUNTERS:
- Iron weapons: More effective than steel
- Blessed ammunition: Works on undead
- Hold formation: Don't let fear break you
- Concentrated fire: They can be killed

I document everything. Build threat assessments. Help Rangers understand what they're
fighting.''',

            'reports': '''I need intelligence from patrols. What you observe matters.

WHAT TO REPORT:
- Enemy positions and numbers
- Enemy types and equipment
- Defensive positions and fortifications
- Movement patterns and patrol routes
- Any unusual activity
- Terrain and obstacles

HOW TO REPORT:
- Grid references for all observations
- Accurate counts (estimate if necessary)
- Clear descriptions
- Sketch maps if possible
- Time and date of observation

WHY IT MATTERS:
- I build a picture of enemy disposition
- Identify threats before they become critical
- Plan operations based on solid intel
- Track changes over time

Every Ranger is an intelligence collector. Observe, remember, report. Your observations
might save lives.''',

            'orcs': '''Orcs are our primary threat. I've been studying them extensively.

BIOLOGY:
- 6-7 feet tall, 200-300 pounds
- Green skin, tusks, yellow eyes
- Extremely strong and tough
- Carnivorous

BEHAVIOR:
- Aggressive and violent
- Tribal culture with chieftains
- Respect strength
- Will eat prisoners (confirmed)

TACTICS:
- Frontal assaults with numerical superiority
- Swarm tactics - overwhelm with numbers
- Use crude weapons: clubs, axes, spears
- Some use scavenged bows and crossbows
- Follow chieftains (kill the leader, disrupt the unit)

INTELLIGENCE LEVEL:
- Not stupid - cunning in combat
- Can plan ambushes
- Use terrain effectively
- Learn from encounters

MORALE:
- Fearless - will fight to death
- Leadership-dependent (kill leaders to break them)
- Dark Army orcs are more disciplined than typical

Rangers need to stop thinking of orcs as monsters and start thinking of them as enemy
combatants. Dangerous, organized, and committed.''',

            'missions': '''I can provide intelligence for mission planning.

SERVICES:
- Enemy disposition in target areas
- Terrain analysis
- Threat assessments
- Recommended approach routes
- Exfiltration planning

Tell me where you're going and I'll tell you what we know about it. Knowledge is your
edge out there.''',

            'lich_pharaoh': '''The Lich Pharaoh is the primary strategic threat.

WHAT WE KNOW:
- Undead entity of extreme power
- Commands the Dark Army
- Located in western territories
- Ancient - predates current civilization
- Goal appears to be conquest and domination

CAPABILITIES (ESTIMATED):
- Powerful magic user
- Commands undead forces
- Influence extends hundreds of miles
- Can raise and control vast armies
- Possibly immortal

STRATEGY:
- Uses orc forces as frontline troops
- Dark wizards provide magical support
- Wraith riders for fast strikes
- Appears to be planning a major offensive

ORDERS:
- Avoid direct contact
- Do not enter western territories
- If encountered, disengage immediately
- Report any intelligence

This is a threat beyond our current capabilities. We're fighting his forces, but
eventually we'll have to face him. That day is going to be... difficult.''',

            'rangers': '''Rangers are professional intelligence collectors whether they know it or not.

Every patrol observes and reports. Every contact provides data. Over time, I build
a comprehensive picture of the enemy and the terrain.

Rangers take this seriously. They understand that intelligence saves lives. They
observe carefully, report accurately, and don't embellish.

That discipline is why our intelligence is solid. I trust Ranger reports. They're
trained observers and they don't bullshit me.

Good intelligence and good soldiers - that's how we survive against impossible odds.''',
        }
    },

    'pfc_rodriguez': {
        'greeting': '''Ranger. Perimeter is quiet for now, but stay alert. Things can go sideways fast out here.''',

        'topics': {
            'guard': '''I pull watch rotation. We keep eyes on the perimeter 24/7. Orcs love night attacks,
and wraith riders move fast. Can't let our guard down.

WATCH ROTATION:
- 4 hour shifts
- Two Rangers per post
- Night vision when available
- Radio check-ins every hour

RESPONSIBILITIES:
- Observe perimeter
- Challenge approaching personnel
- Report suspicious activity
- Sound alarm if enemy approaches

SECTORS:
- North: Most dangerous, faces orc territory
- East: Dragon territory, usually quiet
- South: Civilian settlements, friendly
- West: Lich Pharaoh territory, no one approaches from there

It's boring until it's not. Then it's life or death in seconds. Stay alert.''',

            'threat': '''Biggest threat is complacency. You start thinking you're safe, that's when the orcs hit.
Stay alert, stay alive.

COMMON THREATS:
- Orc scout parties: Probing defenses
- Wraith rider raids: Fast hit and run
- Infiltrators: Rare but it happens
- Wildlife: Some creatures are dangerous

WARNING SIGNS:
- Unusual animal behavior
- Silence (animals go quiet when orcs are near)
- Movement in the tree line
- Strange lights or sounds (magic)

RESPONSE:
- Report immediately
- Sound alarm if confirmed threat
- Engage only if necessary
- Fall back to secondary positions if overwhelmed

Most shifts are boring. But you can't assume that means you're safe. The one time you
relax is the one time they attack.''',

            'rangers': '''Rangers are the best infantry in the world. This situation is FUBAR, but we don't quit.
We adapt and we fight.

I'm proud to be a Ranger. Even here, ten thousand years from home, surrounded by enemies
that shouldn't exist, we hold the line.

We don't have to be here. We volunteered. We knew the risks. Now we're here and we're
not backing down.

That's what Rangers do. When the mission is impossible, when everyone else has failed,
they call us. And we don't fail.

This situation is impossible. But we're still here. Still fighting. Still winning.

Rangers lead the way. Always have, always will.''',

            'perimeter': '''The perimeter defenses are solid but not impenetrable.

DEFENSES:
- Hesco barriers and sandbags
- Wooden palisade (improvised)
- Fighting positions with fields of fire
- Wire obstacles in some areas
- Guard towers at key points

GAPS:
- Not enough Rangers to cover everything
- Some sections are weaker than others
- Wire obstacles are incomplete
- Limited night vision equipment

ENEMY TACTICS:
- Orcs test defenses regularly
- Probing attacks to find weaknesses
- Sometimes full assaults
- Wraith riders try to bypass and attack from behind

We hold because Rangers are disciplined and skilled. But the defenses help.

If you see weakness in the perimeter, report it. We improve defenses constantly.''',

            'orcs': '''Orcs attack regularly. Probing attacks mostly, testing our defenses.

TYPICAL ATTACKS:
- Small scout parties: 5-10 orcs
- Probing attacks: 20-30 orcs
- Coordinated assaults: 50+ orcs (rare but devastating)

TACTICS:
- Test defenses to find weak points
- Sometimes night attacks
- Use crude weapons but effective
- Will withdraw if they take casualties

RESPONSE:
- Controlled fire, make shots count
- Target leaders if identifiable
- Hold position unless ordered to fall back
- Call for support if needed

Most attacks we repel easily. But we can't get complacent. One day they'll come in force
and we'll need every Ranger on the line.''',

            'stories': '''I've seen some shit out here.

One time, wraith riders hit the perimeter at midnight. Came out of nowhere, ghostly
cavalry moving impossibly fast. We opened fire but they phased through the barriers.

Killed two Rangers before we figured out iron rounds work better. We switched ammunition
and drove them off, but it was close.

Another time, an orc warband hit us at dawn. Fifty strong, coordinated assault. They
had a dark wizard throwing lightning. It was chaos.

We held, but barely. Lost three Rangers that day. The wizard died with a round through
his skull. Orcs broke when their magical support went down.

Every day is a fight to survive. But we're winning. We're still here. That counts for
something.''',

            'advice': '''Guard duty advice:

1. STAY ALERT:
   - Don't daydream
   - Scan your sector constantly
   - Watch for movement and unusual activity
   - Listen as well as look

2. KNOW YOUR SECTOR:
   - Fields of fire
   - Dead ground where enemies can hide
   - Range to key terrain features
   - Escape routes if you need to fall back

3. MAINTAIN YOUR WEAPON:
   - Keep it clean and ready
   - Know your ammunition status
   - Have backup magazines ready
   - Blade accessible for close combat

4. COMMUNICATE:
   - Radio check-ins on schedule
   - Report anything unusual
   - Coordinate with adjacent posts
   - Know how to sound the alarm

5. TRUST YOUR INSTINCTS:
   - If something feels wrong, it probably is
   - Don't dismiss suspicions
   - Report concerns
   - Better safe than dead

Guard duty keeps everyone alive. Take it seriously.''',
        }
    },
}

# Update NPCs with expanded dialogue
print_section("Expanding NPC Dialogue Trees")

updated_count = 0
for npc_key, dialogue_data in expanded_dialogues.items():
    try:
        npc = NPC.objects.get(key=npc_key)
        npc.dialogue_tree = dialogue_data
        npc.save()
        print_success(f"Updated dialogue for: {npc.name}")
        updated_count += 1
    except NPC.DoesNotExist:
        print(f"⚠ Warning: NPC '{npc_key}' not found")

# Print summary
print_section("Dialogue Expansion Complete!")
print_success(f"Updated {updated_count} NPCs with expanded dialogue")
print()
print_info("NPCs now have rich, interactive dialogue including:")
print("  - Multiple conversation topics")
print("  - Quest chains and missions")
print("  - Tactical advice and training")
print("  - Deep lore and worldbuilding")
print("  - Dynamic responses and context")
print()
print(f"{Color.YELLOW}Try these example conversations:{Color.END}")
print("  > talk captain_reynolds missions")
print("  > talk captain_reynolds recon")
print("  > talk sergeant_kim training")
print("  > talk sergeant_kim marksmanship")
print("  > talk doc_martinez potions")
print("  > talk specialist_jackson enchantment")
print("  > talk sergeant_walsh economy")
print("  > talk corporal_chen lich_pharaoh")
print("  > talk pfc_rodriguez stories")
print()
