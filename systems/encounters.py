import random
from ui.text_effects import type_text, dramatic, pause
from ui.text_randomizer import rt
from systems.combat import start_combat
from actors.enemy import Enemy


# ---------------------------------------------------------
# BIOME-BASED ENEMY TABLES
# ---------------------------------------------------------

BIOME_ENEMIES = {
    "forest": [
        {"id": "wolf", "name": "Forest Wolf", "tier": 1, "behavior": "aggressive",
         "weaknesses": ["fire"], "abilities": ["strike", "bleed"]},
        {"id": "bandit", "name": "Forest Bandit", "tier": 2, "behavior": "opportunistic",
         "weaknesses": ["cold"], "abilities": ["strike", "heavy_strike"]},
        {"id": "alpha_wolf", "name": "Alpha Wolf", "tier": 3, "behavior": "aggressive",
         "weaknesses": ["fire"], "abilities": ["strike", "bleed", "stun"]},
    ],
    "plains": [
        {"id": "boar", "name": "Wild Boar", "tier": 1, "behavior": "aggressive",
         "weaknesses": ["piercing"], "abilities": ["strike", "heavy_strike"]},
        {"id": "raider", "name": "Plains Raider", "tier": 2, "behavior": "opportunistic",
         "weaknesses": ["cold"], "abilities": ["strike", "stun"]},
        {"id": "war_horse", "name": "War Horse", "tier": 3, "behavior": "defensive",
         "weaknesses": ["fire"], "abilities": ["strike", "heavy_strike"]},
    ],
    "swamp": [
        {"id": "slime", "name": "Swamp Slime", "tier": 1, "behavior": "defensive",
         "weaknesses": ["fire"], "abilities": ["strike"]},
        {"id": "ghoul", "name": "Swamp Ghoul", "tier": 2, "behavior": "aggressive",
         "weaknesses": ["holy"], "abilities": ["strike", "bleed"]},
        {"id": "bog_fiend", "name": "Bog Fiend", "tier": 3, "behavior": "aggressive",
         "weaknesses": ["fire"], "abilities": ["strike", "stun"]},
    ],
    "mountain": [
        {"id": "goblin", "name": "Mountain Goblin", "tier": 1, "behavior": "opportunistic",
         "weaknesses": ["fire"], "abilities": ["strike"]},
        {"id": "orc", "name": "Orc Warrior", "tier": 3, "behavior": "aggressive",
         "weaknesses": ["cold"], "abilities": ["strike", "heavy_strike"]},
        {"id": "troll", "name": "Mountain Troll", "tier": 4, "behavior": "defensive",
         "weaknesses": ["fire"], "abilities": ["strike", "stun"]},
    ],
    "desert": [
        {"id": "scorpion", "name": "Giant Scorpion", "tier": 2, "behavior": "aggressive",
         "weaknesses": ["cold"], "abilities": ["strike", "bleed"]},
        {"id": "sand_raider", "name": "Sand Raider", "tier": 3, "behavior": "opportunistic",
         "weaknesses": ["water"], "abilities": ["strike", "stun"]},
        {"id": "dune_wyrm", "name": "Dune Wyrm", "tier": 5, "behavior": "aggressive",
         "weaknesses": ["cold"], "abilities": ["strike", "heavy_strike", "bleed"]},
    ],
}


# ---------------------------------------------------------
# ENCOUNTER CHANCE
# ---------------------------------------------------------

def should_trigger_encounter():
    return random.random() < 0.25  # 25% chance


# ---------------------------------------------------------
# SPAWN ENEMY BASED ON BIOME
# ---------------------------------------------------------

def spawn_enemy(biome):
    if biome not in BIOME_ENEMIES:
        return None

    data = random.choice(BIOME_ENEMIES[biome])
    return Enemy(
        id=data["id"],
        name=data["name"],
        tier=data["tier"],
        biome=biome,
        behavior=data["behavior"],
        weaknesses=data["weaknesses"],
        abilities=data["abilities"],
    )


# ---------------------------------------------------------
# SPECIAL ROOM EVENTS
# ---------------------------------------------------------

def special_room_event(room):
    if "treasure" in room.tags:
        return rt("event_treasure")

    if "shrine" in room.tags:
        return rt("event_shrine")

    if "campfire" in room.tags:
        return rt("event_campfire")

    if "miniboss" in room.tags:
        return rt("event_miniboss")

    return None


# ---------------------------------------------------------
# AUTO ENCOUNTERS (NPCs, Animals, Enemies)
# ---------------------------------------------------------

def auto_encounter(player, world):
    room = world.get_room(player.room_id)
    biome = room.biome

    # -----------------------------------------------------
    # 0. BANDIT AMBUSH (NPC-based, faction-aware)
    # -----------------------------------------------------
    ambushers = [n for n in room.npcs if getattr(n, "is_ambusher", False)]

    if ambushers:
        bandit = random.choice(ambushers)

        # If player is on good terms with the bandit's faction, they might back off
        rep = 0
        if getattr(bandit, "faction", None) and hasattr(player, "reputation"):
            rep = player.reputation.get(bandit.faction, 0)

        dramatic(rt("bandit_ambush_intro", npc=bandit.name))

        if rep > 20:
            # Friendly / allied with bandit faction
            dramatic(
                f"{bandit.name} eyes your insignia and relaxes. "
                "'Didn't realize you were one of us. Move along.'"
            )
            return ""

        # Bandit taunts
        taunts = [
            f"{bandit.name} snarls: 'Hand it over, traveler.'",
            f"{bandit.name} grins wickedly.",
            f"{bandit.name} steps from the shadows with a blade drawn.",
        ]
        dramatic(random.choice(taunts))

        # Start combat using NPC as enemy
        enemy = Enemy(
            id="bandit_npc",
            name=bandit.name,
            tier=2,
            biome=biome,
            behavior="aggressive",
            weaknesses=["cold"],
            abilities=["strike", "heavy_strike"],
        )

        # Flavor: companions brace for the fight
        if getattr(player, "companions", None):
            dramatic(rt("combat_with_companions"))

        return start_combat(player, enemy)

    # -----------------------------------------------------
    # 1. Legendary beast encounter
    # -----------------------------------------------------
    for animal in room.animals:
        if getattr(animal, "legendary", False):
            dramatic(rt("legendary_intro", animal=animal.name))

            if getattr(player, "companions", None):
                dramatic(rt("legendary_with_companions", animal=animal.name))

            return start_combat(player, animal)

    # -----------------------------------------------------
    # 2. Animal encounter (personality-aware)
    # -----------------------------------------------------
    if room.animals and random.random() < 0.35:
        animal = random.choice(room.animals)

        dramatic(rt("animal_seen", animal=animal.name))

        reaction = animal.reaction_text()
        if reaction:
            dramatic(reaction)

        if getattr(animal, "hostile", False):
            if getattr(player, "companions", None):
                dramatic(rt("animal_hostile_with_companions", animal=animal.name))
            return start_combat(player, animal)

        return ""  # peaceful encounter

    # -----------------------------------------------------
    # 3. Special room events
    # -----------------------------------------------------
    event_msg = special_room_event(room)
    if event_msg:
        dramatic(event_msg)
        return ""

    # -----------------------------------------------------
    # 4. Emissary encounter (peaceful, faction reputation)
    # -----------------------------------------------------
    emissaries = [n for n in room.npcs if getattr(n, "is_emissary", False)]
    if emissaries and random.random() < 0.15:
        npc = random.choice(emissaries)
        dramatic(rt("emissary_meets", npc=npc.name, faction=npc.faction))

        # Simple diplomatic adjustment if player has reputation system
        if hasattr(player, "modify_reputation") and npc.faction:
            # Small positive nudge for a peaceful meeting
            msg = player.modify_reputation(npc.faction, +1)
            dramatic(msg)

        return ""

    # -----------------------------------------------------
    # 5. Shrine guardian warning (may escalate if hated)
    # -----------------------------------------------------
    guardians = [n for n in room.npcs if getattr(n, "is_guardian", False)]
    if guardians and random.random() < 0.20:
        npc = random.choice(guardians)
        dramatic(rt("guardian_warning", npc=npc.name))

        # If the faction hates you, guardian may attack
        rep = 0
        if npc.faction and hasattr(player, "reputation"):
            rep = player.reputation.get(npc.faction, 0)

        if rep < -30:
            dramatic(rt("guardian_hostile", npc=npc.name))
            enemy = Enemy(
                id="shrine_guardian",
                name=npc.name,
                tier=3,
                biome=biome,
                behavior="aggressive",
                weaknesses=["holy"],
                abilities=["strike", "stun"],
            )
            return start_combat(player, enemy)

        return ""

    # -----------------------------------------------------
    # 6. Storyteller peaceful encounter (with rumor)
    # -----------------------------------------------------
    storytellers = [n for n in room.npcs if getattr(n, "is_storyteller", False)]
    if storytellers and random.random() < 0.20:
        npc = random.choice(storytellers)
        dramatic(rt("storyteller_greeting", npc=npc.name))

        # Share a random rumor / micro-story
        rumor_keys = [
            "rumor_beast",
            "rumor_ruins",
            "rumor_shrine",
            "rumor_weather",
            "rumor_wanderer",
        ]
        rumor_key = random.choice(rumor_keys)
        dramatic(rt(rumor_key))

        return ""

    # -----------------------------------------------------
    # 7. Enemy encounter (biome-based)
    # -----------------------------------------------------
    if should_trigger_encounter():
        enemy = spawn_enemy(biome)
        if enemy:
            dramatic(rt("enemy_appears", enemy=enemy.name, biome=biome))

            if getattr(player, "companions", None):
                dramatic(rt("enemy_with_companions", enemy=enemy.name))

            return start_combat(player, enemy)

    return ""
