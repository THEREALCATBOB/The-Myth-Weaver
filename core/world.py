import random
from dataclasses import dataclass, field
from actors.animal import Animal

# ============================================================
# CONSTANTS
# ============================================================

BIOMES = ["forest", "plains", "swamp", "mountain", "desert"]

FACTIONS = {
    "Forest Clan": {
        "home_biome": "forest",
        "personality": "serious",
        "aggression": 0.6,
    },
    "Mountain Tribe": {
        "home_biome": "mountain",
        "personality": "stoic",
        "aggression": 0.7,
    },
    "Desert Nomads": {
        "home_biome": "desert",
        "personality": "pragmatic",
        "aggression": 0.5,
    },
    "Swamp Covenant": {
        "home_biome": "swamp",
        "personality": "mysterious",
        "aggression": 0.4,
    },
    "Plains Alliance": {
        "home_biome": "plains",
        "personality": "friendly",
        "aggression": 0.3,
    },
}

WEATHERS = ["clear", "rain", "storm", "fog", "snow"]

# Light debug logging
DEBUG = True


# ============================================================
# ROOM STRUCTURE
# ============================================================

@dataclass
class Room:
    id: int
    name: str
    description: str
    biome: str

    resources: list = field(default_factory=list)
    hazards: list = field(default_factory=list)

    npcs: list = field(default_factory=list)
    animals: list = field(default_factory=list)

    exits: dict = field(default_factory=dict)
    locked_exits: dict = field(default_factory=dict)

    tags: set = field(default_factory=set)  # camp, shrine, treasure, miniboss, den

    # War simulation metadata
    faction_control: str | None = None
    contested: bool = False


# ============================================================
# WORLD CLASS
# ============================================================

class World:
    def __init__(self, size=15):
        # Player chooses size at game start
        self.size = size
        self.rooms: dict[int, Room] = {}
        self.start_room_id: int | None = None

        # World state
        self.day = 1
        self.time_of_day = 8
        self.season = "Spring"
        self.weather = "clear"
        self.temperature = 20.0

        # Faction war state
        self.faction_territories = {f: set() for f in FACTIONS.keys()}
        self.faction_strength = {f: 100 for f in FACTIONS.keys()}  # morale/war power

        # NPC systems (populated in Section 2)
        self.wandering_npcs = []
        self.faction_patrols = []
        self.traveling_merchants = []
        self.traveling_storytellers = []
        self.quest_givers = []
        self.faction_emissaries = []
        self.bandit_ambushers = []

        # Animal systems
        self.animal_dens = []
        self.migration_routes = {}

        if DEBUG:
            print(f"[DEBUG] World initialized with size {self.size}x{self.size}")

    # ============================================================
    # POPULATE WORLD — ONE CALL TO SPAWN EVERYTHING
    # ============================================================

    def populate_world(self):
        """Runs all NPC and faction systems after base world generation."""
        # Faction territory setup
        self.assign_faction_territories()

        # NPC ecosystems
        self.spawn_ambient_npcs()
        self.spawn_shrine_guardians()
        self.spawn_camps()
        self.spawn_patrols()
        self.spawn_caravans()
        self.spawn_emissaries()
        self.spawn_legendary_npcs()

        if DEBUG:
            print("[DEBUG] World population complete.")





    # ============================================================
    # WORLD GENERATION
    # ============================================================

    def generate(self):
        width = self.size
        height = self.size

        room_id = 0
        for y in range(height):
            for x in range(width):
                biome = random.choice(BIOMES)
                name = f"{biome.title()} Area {room_id}"
                desc = self._biome_description(biome)

                room = Room(
                    id=room_id,
                    name=name,
                    description=desc,
                    biome=biome,
                )

                # Exits
                if x > 0:
                    room.exits["west"] = room_id - 1
                if x < width - 1:
                    room.exits["east"] = room_id + 1
                if y > 0:
                    room.exits["north"] = room_id - width
                if y < height - 1:
                    room.exits["south"] = room_id + width

                # Resources + hazards
                room.resources = self._generate_resources(biome)
                room.hazards = self._generate_hazards(biome)

                # Animals
                self._spawn_animals(room)

                # Special tags (shrines, camps, treasure)
                self._maybe_mark_special(room)

                self.rooms[room_id] = room
                room_id += 1

        self.start_room_id = 0

        # After rooms exist, set up migration routes
        self._setup_migration_routes()

        if DEBUG:
            print("[DEBUG] Base world generation complete.")

    # ============================================================
    # BIOME DESCRIPTIONS
    # ============================================================

    def _biome_description(self, biome: str) -> str:
        match biome:
            case "forest":
                return "Tall trees crowd around you, their leaves whispering in the wind."
            case "plains":
                return "Open grasslands stretch out in all directions under a wide sky."
            case "swamp":
                return "The ground squelches underfoot, and the air is thick and damp."
            case "mountain":
                return "Jagged rocks and steep slopes dominate the rugged landscape."
            case "desert":
                return "Endless dunes of sand shimmer beneath the harsh sun."
        return "An unremarkable stretch of land."

    # ============================================================
    # RESOURCES + HAZARDS
    # ============================================================

    def _generate_resources(self, biome: str) -> list:
        return {
            "forest": ["berries", "wood"],
            "plains": ["herbs", "game"],
            "swamp": ["mushrooms"],
            "mountain": ["ore", "stone"],
            "desert": ["cactus", "scrap"],
        }.get(biome, [])

    def _generate_hazards(self, biome: str) -> list:
        return {
            "swamp": ["poisonous gas"],
            "mountain": ["loose rocks"],
            "desert": ["heatstroke"],
        }.get(biome, [])

    # ============================================================
    # ANIMAL SPAWNING
    # ============================================================

    def _spawn_animals(self, room: Room):
        biome = room.biome

        # 75% chance to spawn animals
        if random.random() < 0.75:

            pools = {
                "forest": [
                    ("Deer", False), ("Rabbit", False),
                    ("Wolf", True), ("Boar", True)
                ],
                "plains": [
                    ("Horse", False), ("Bison", False),
                    ("Wild Dog", True)
                ],
                "swamp": [
                    ("Frog", False),
                    ("Giant Leech", True), ("Crocodile", True)
                ],
                "mountain": [
                    ("Goat", False), ("Eagle", False),
                    ("Mountain Lion", True)
                ],
                "desert": [
                    ("Lizard", False),
                    ("Scorpion", True), ("Sand Wolf", True)
                ],
            }

            pool = pools.get(biome, [("Strange Bird", False)])

            # 1–3 animals per room
            count = random.randint(1, 3)
            for _ in range(count):
                name, hostile = random.choice(pool)
                animal = Animal(name=name, hostile=hostile, biome=biome, room_id=room.id)
                room.animals.append(animal)

        # 10% chance of a den
        if random.random() < 0.1:
            room.tags.add("den")
            self.animal_dens.append(room.id)

    # ============================================================
    # SPECIAL ROOM TAGS
    # ============================================================

    def _maybe_mark_special(self, room: Room):
        if random.random() < 0.04:
            room.tags.add("campfire")
        if random.random() < 0.03:
            room.tags.add("shrine")
        if random.random() < 0.03:
            room.tags.add("treasure")
        if random.random() < 0.01:
            room.tags.add("miniboss")

    # ============================================================
    # MIGRATION ROUTES
    # ============================================================

    def _setup_migration_routes(self):
        self.migration_routes = {b: [] for b in BIOMES}
        for room_id, room in self.rooms.items():
            self.migration_routes[room.biome].append(room_id)

        if DEBUG:
            print("[DEBUG] Migration routes established.")
    # ============================================================
    # NPC SYSTEMS — SPAWN TABLES + HELPERS
    # ============================================================

    def _random_room_id(self):
        return random.choice(list(self.rooms.keys()))

    def _rooms_in_biome(self, biome):
        return [rid for rid, r in self.rooms.items() if r.biome == biome]

    def _spawn_npc(self, npc_id, name, personality, faction, room_id, **flags):
        """Centralized NPC creation — ensures compatibility with your AI NPC class."""
        from actors.npc import NPC

        npc = NPC(
            npc_id=npc_id,
            name=name,
            personality=personality,
            faction=faction,
        )
        npc.room_id = room_id

        # Apply role flags (guardian, emissary, storyteller, ambusher, questgiver)
        for k, v in flags.items():
            setattr(npc, k, v)

        # Add to room
        self.rooms[room_id].npcs.append(npc)
        return npc

    # ============================================================
    # FACTION TERRITORY GENERATION (SEMI-RANDOMIZED)
    # ============================================================

    def assign_faction_territories(self):
        """Each faction gets 8–15 starting rooms in its preferred biome."""
        for faction, data in FACTIONS.items():
            biome = data["home_biome"]
            candidates = self._rooms_in_biome(biome)

            if not candidates:
                continue

            # Semi-randomized: choose a random cluster
            territory_size = random.randint(8, 15)
            chosen = random.sample(candidates, min(territory_size, len(candidates)))

            for rid in chosen:
                self.rooms[rid].faction_control = faction
                self.faction_territories[faction].add(rid)

        if DEBUG:
            print("[DEBUG] Faction territories assigned.")

    # ============================================================
    # AMBIENT NPCS (BIOME-SPECIFIC)
    # ============================================================

    def spawn_ambient_npcs(self):
        """Biome-based ambient NPCs that wander and talk to the player."""
        for room_id, room in self.rooms.items():
            if random.random() > 0.55:
                continue

            biome = room.biome

            biome_npcs = {
                "forest": ["Wanderer", "Herbalist", "Scout"],
                "plains": ["Traveler", "Hunter", "Nomad"],
                "swamp": ["Bog Walker", "Hermit", "Mire Scout"],
                "mountain": ["Climber", "Miner", "Ridge Scout"],
                "desert": ["Drifter", "Sand Scout", "Nomad"],
            }

            name = random.choice(biome_npcs.get(biome, ["Traveler"]))
            personality = random.choice(["curious", "friendly", "neutral"])

            npc_id = f"ambient_{room_id}_{random.randint(1000,9999)}"
            self._spawn_npc(
                npc_id=npc_id,
                name=name,
                personality=personality,
                faction=None,
                room_id=room_id,
            )

    # ============================================================
    # SHRINES + GUARDIANS
    # ============================================================

    def spawn_shrine_guardians(self):
        """Spawn mystic guardians at shrine rooms."""
        for room_id, room in self.rooms.items():
            if "shrine" not in room.tags:
                continue

            npc_id = f"guardian_{room_id}"
            self._spawn_npc(
                npc_id=npc_id,
                name="Shrine Guardian",
                personality="serious",
                faction="Swamp Covenant" if room.biome == "swamp" else "Mystics",
                room_id=room_id,
                is_guardian=True,
            )

    # ============================================================
    # CAMPS (FACTION + NEUTRAL)
    # ============================================================

    def spawn_camps(self):
        """Spawn faction camps and neutral camps."""
        for faction in FACTIONS.keys():
            # 2–4 camps per faction
            count = random.randint(2, 4)
            for i in range(count):
                rid = self._random_room_id()
                room = self.rooms[rid]

                room.tags.add("camp")
                room.faction_control = faction
                self.faction_territories[faction].add(rid)

                # Camp defenders
                for j in range(random.randint(2, 4)):
                    npc_id = f"{faction}_camp_{i}_{j}"
                    self._spawn_npc(
                        npc_id=npc_id,
                        name=f"{faction} Defender",
                        personality="serious",
                        faction=faction,
                        room_id=rid,
                    )

        if DEBUG:
            print("[DEBUG] Camps spawned.")

    # ============================================================
    # PATROLS
    # ============================================================

    def spawn_patrols(self):
        """Spawn patrol groups for each faction."""
        for faction, data in FACTIONS.items():
            biome = data["home_biome"]
            biome_rooms = self._rooms_in_biome(biome)

            if not biome_rooms:
                continue

            # 2–4 patrols per faction
            for i in range(random.randint(2, 4)):
                start = random.choice(biome_rooms)
                patrol = []

                for j in range(random.randint(3, 5)):
                    npc_id = f"patrol_{faction}_{i}_{j}"
                    npc = self._spawn_npc(
                        npc_id=npc_id,
                        name=f"{faction} Guard",
                        personality="serious",
                        faction=faction,
                        room_id=start,
                        is_patrol=True,
                    )
                    patrol.append(npc)

                self.faction_patrols.append(patrol)

        if DEBUG:
            print("[DEBUG] Patrols spawned.")

    # ============================================================
    # CARAVANS
    # ============================================================

    def spawn_caravans(self):
        """Spawn traveling merchants with guards."""
        for i in range(random.randint(2, 4)):
            start = self._random_room_id()

            # Merchant
            merchant_id = f"caravan_merchant_{i}"
            merchant = self._spawn_npc(
                npc_id=merchant_id,
                name="Caravan Trader",
                personality="friendly",
                faction="Free Traders",
                room_id=start,
                is_merchant=True,
            )

            # Guards
            guards = []
            for j in range(random.randint(1, 3)):
                guard_id = f"caravan_guard_{i}_{j}"
                guard = self._spawn_npc(
                    npc_id=guard_id,
                    name="Caravan Guard",
                    personality="serious",
                    faction="Free Traders",
                    room_id=start,
                    is_guard=True,
                )
                guards.append(guard)

            self.traveling_merchants.append((merchant, guards))

        if DEBUG:
            print("[DEBUG] Caravans spawned.")

    # ============================================================
    # EMISSARIES
    # ============================================================

    def spawn_emissaries(self):
        """Spawn emissaries who travel between factions."""
        for faction, data in FACTIONS.items():
            biome = data["home_biome"]
            biome_rooms = self._rooms_in_biome(biome)

            if not biome_rooms:
                continue

            for i in range(2):
                rid = random.choice(biome_rooms)
                npc_id = f"emissary_{faction}_{i}"

                npc = self._spawn_npc(
                    npc_id=npc_id,
                    name=f"{faction} Emissary",
                    personality="serious",
                    faction=faction,
                    room_id=rid,
                    is_emissary=True,
                )

                self.faction_emissaries.append(npc)

        if DEBUG:
            print("[DEBUG] Emissaries spawned.")

    # ============================================================
    # LEGENDARY NPCS
    # ============================================================

    def spawn_legendary_npcs(self):
        """Each biome has a small chance to spawn a legendary NPC."""
        legendary_templates = {
            "forest": ("Elder Ranger", "wise"),
            "plains": ("Storm Rider", "bold"),
            "swamp": ("Bog Prophet", "mysterious"),
            "mountain": ("Stone Sentinel", "stoic"),
            "desert": ("Sand Wraith", "silent"),
        }

        for biome, rooms in self.migration_routes.items():
            if not rooms:
                continue

            if random.random() < 0.35:  # 35% chance per biome
                rid = random.choice(rooms)
                name, personality = legendary_templates[biome]

                npc_id = f"legendary_{biome}_{rid}"
                npc = self._spawn_npc(
                    npc_id=npc_id,
                    name=name,
                    personality=personality,
                    faction=None,
                    room_id=rid,
                    is_legendary=True,
                )

                if DEBUG:
                    print(f"[DEBUG] Legendary NPC spawned: {name} in room {rid}")
    # ============================================================
    # FACTION WAR SIMULATION
    # ============================================================

    def simulate_faction_war(self):
        """Runs once per day or when triggered by world events."""
        # Each faction attempts to expand or defend territory
        for faction in FACTIONS.keys():
            self._faction_attempt_expand(faction)
            self._faction_attempt_defend(faction)

        # Patrol clashes
        self._resolve_patrol_clashes()

        # Camps may be destroyed or captured
        self._resolve_camp_conflicts()

        # Emissaries attempt diplomacy
        self._resolve_emissary_actions()

        if DEBUG:
            print("[DEBUG] Faction war simulation step complete.")

    # ------------------------------------------------------------
    # Territory Expansion
    # ------------------------------------------------------------

    def _faction_attempt_expand(self, faction):
        """Faction tries to expand into adjacent neutral or enemy rooms."""
        controlled = list(self.faction_territories[faction])
        random.shuffle(controlled)

        for rid in controlled[:5]:  # limit expansion attempts
            room = self.rooms[rid]

            for direction, neighbor_id in room.exits.items():
                neighbor = self.rooms[neighbor_id]

                # Skip if already controlled
                if neighbor.faction_control == faction:
                    continue

                # Chance to expand depends on aggression
                aggression = FACTIONS[faction]["aggression"]
                if random.random() < aggression * 0.25:
                    previous = neighbor.faction_control
                    neighbor.faction_control = faction
                    self.faction_territories[faction].add(neighbor_id)

                    if previous and previous != faction:
                        self.faction_territories[previous].discard(neighbor_id)

                    if DEBUG:
                        print(f"[DEBUG] {faction} expanded into room {neighbor_id}")

    # ------------------------------------------------------------
    # Territory Defense
    # ------------------------------------------------------------

    def _faction_attempt_defend(self, faction):
        """Faction reinforces key rooms."""
        controlled = list(self.faction_territories[faction])
        if not controlled:
            return

        # Reinforce 1–2 random rooms
        for rid in random.sample(controlled, min(2, len(controlled))):
            room = self.rooms[rid]

            # Add a defender
            npc_id = f"{faction}_defender_{rid}_{random.randint(1000,9999)}"
            self._spawn_npc(
                npc_id=npc_id,
                name=f"{faction} Defender",
                personality="serious",
                faction=faction,
                room_id=rid,
            )

            if DEBUG:
                print(f"[DEBUG] {faction} reinforced room {rid}")

    # ------------------------------------------------------------
    # Patrol Clashes
    # ------------------------------------------------------------

    def _resolve_patrol_clashes(self):
        """If two patrols from different factions meet, they clash."""
        patrol_positions = {}

        for patrol in self.faction_patrols:
            if not patrol:
                continue
            rid = patrol[0].room_id
            patrol_positions.setdefault(rid, []).append(patrol)

        for rid, patrols in patrol_positions.items():
            if len(patrols) < 2:
                continue

            # Multiple patrols in same room → conflict
            factions_present = {p[0].faction for p in patrols}
            if len(factions_present) < 2:
                continue

            # Resolve conflict
            winner = random.choice(list(factions_present))
            losers = [f for f in factions_present if f != winner]

            # Remove losing patrols
            for patrol in patrols:
                if patrol[0].faction in losers:
                    for npc in patrol:
                        self.rooms[rid].npcs.remove(npc)
                    patrol.clear()

            if DEBUG:
                print(f"[DEBUG] Patrol clash in room {rid}. Winner: {winner}")

    # ------------------------------------------------------------
    # Camp Conflicts
    # ------------------------------------------------------------

    def _resolve_camp_conflicts(self):
        """Enemy factions may destroy or capture camps."""
        for rid, room in self.rooms.items():
            if "camp" not in room.tags:
                continue

            factions_present = {npc.faction for npc in room.npcs if npc.faction}

            if len(factions_present) <= 1:
                continue

            # Conflict
            winner = random.choice(list(factions_present))
            losers = [f for f in factions_present if f != winner]

            # Remove losing NPCs
            room.npcs = [npc for npc in room.npcs if npc.faction == winner]

            # Camp changes hands
            previous = room.faction_control
            room.faction_control = winner

            if previous and previous != winner:
                self.faction_territories[previous].discard(rid)
            self.faction_territories[winner].add(rid)

            if DEBUG:
                print(f"[DEBUG] Camp conflict in room {rid}. Winner: {winner}")

    # ------------------------------------------------------------
    # Emissary Diplomacy
    # ------------------------------------------------------------

    def _resolve_emissary_actions(self):
        """Emissaries attempt diplomacy or get intercepted."""
        for npc in self.faction_emissaries:
            rid = npc.room_id
            room = self.rooms[rid]

            factions_present = {n.faction for n in room.npcs if n.faction}

            # If emissary meets enemy patrol → intercepted
            if any(f != npc.faction for f in factions_present):
                if DEBUG:
                    print(f"[DEBUG] Emissary {npc.npc_id} intercepted in room {rid}")
                room.npcs.remove(npc)
                continue

            # Otherwise, emissary strengthens morale
            self.faction_strength[npc.faction] += 1

    # ============================================================
    # NPC MOVEMENT SYSTEMS
    # ============================================================

    def move_patrols(self):
        """Patrols move randomly within their biome."""
        for patrol in self.faction_patrols:
            if not patrol:
                continue

            leader = patrol[0]
            current = self.rooms[leader.room_id]

            # Choose a random exit
            if not current.exits:
                continue

            new_rid = random.choice(list(current.exits.values()))

            # Move entire patrol
            for npc in patrol:
                npc.room_id = new_rid

            if DEBUG:
                print(f"[DEBUG] Patrol moved to room {new_rid}")

    def move_caravans(self):
        """Caravans move slowly across the world."""
        for merchant, guards in self.traveling_merchants:
            current = self.rooms[merchant.room_id]

            if not current.exits:
                continue

            new_rid = random.choice(list(current.exits.values()))
            merchant.room_id = new_rid

            for g in guards:
                g.room_id = new_rid

            if DEBUG:
                print(f"[DEBUG] Caravan moved to room {new_rid}")

    def move_emissaries(self):
        """Emissaries wander toward random faction territories."""
        for npc in self.faction_emissaries:
            current = self.rooms[npc.room_id]

            if not current.exits:
                continue

            new_rid = random.choice(list(current.exits.values()))
            npc.room_id = new_rid

            if DEBUG:
                print(f"[DEBUG] Emissary moved to room {new_rid}")

    # ============================================================
    # TIME + WEATHER
    # ============================================================

    def advance_time(self, hours: int):
        self.time_of_day += hours
        while self.time_of_day >= 24:
            self.time_of_day -= 24
            self.day += 1

            # Daily war simulation
            self.simulate_faction_war()

        # Temperature
        if 6 <= self.time_of_day <= 18:
            self.temperature = 18 + random.uniform(-2, 5)
        else:
            self.temperature = 8 + random.uniform(-3, 3)

        # Weather change
        if random.random() < 0.2:
            self.weather = random.choice(WEATHERS)

    # ============================================================
    # ROOM ACCESS
    # ============================================================

    def get_room(self, room_id: int) -> Room:
        return self.rooms[room_id]

    # ============================================================
    # ASCII MINIMAP
    # ============================================================

    def ascii_minimap(self, player_room_id: int) -> str:
        width = self.size
        height = self.size
        lines = []

        for y in range(height):
            row = []
            for x in range(width):
                rid = y * width + x
                room = self.rooms[rid]

                if rid == player_room_id:
                    row.append("P")
                elif "miniboss" in room.tags:
                    row.append("M")
                elif "treasure" in room.tags:
                    row.append("T")
                elif "shrine" in room.tags:
                    row.append("S")
                elif "camp" in room.tags:
                    row.append("C")
                elif "den" in room.tags:
                    row.append("D")
                elif room.faction_control:
                    # First letter of faction
                    row.append(room.faction_control[0])
                else:
                    row.append(".")

            lines.append("".join(row))

        return "\n".join(lines)
