import random


class Quest:
    def __init__(self, id, giver_name, description, target_type, target_name,
                 reward_xp, reward_items):
        self.id = id
        self.giver_name = giver_name
        self.description = description
        self.target_type = target_type  # "animal", "npc", "item", "location"
        self.target_name = target_name
        self.reward_xp = reward_xp
        self.reward_items = reward_items
        self.completed = False
        self.turned_in = False

    def summary(self):
        status = "✓ Completed" if self.completed else "In Progress"
        return f"[{self.id}] {self.description} — {status}"


# ---------------------------------------------------------
# QUEST GENERATION
# ---------------------------------------------------------

def generate_random_quest(world, player, npc):
    """
    Generates a quest appropriate for the NPC's role.
    """

    quest_id = f"q_{npc.id}_{random.randint(1000,9999)}"

    # -----------------------------------------------------
    # STORYTELLER QUESTS
    # -----------------------------------------------------
    if getattr(npc, "is_storyteller", False):
        desc = "Seek out a place of old magic and return with what you learn."
        return Quest(
            quest_id,
            npc.name,
            desc,
            "location",
            "shrine",
            reward_xp=40,
            reward_items=[{"name": "Ancient Token", "type": "artifact"}],
        )

    # -----------------------------------------------------
    # SHRINE GUARDIAN QUESTS
    # -----------------------------------------------------
    if getattr(npc, "is_guardian", False):
        desc = "Cleanse a corrupted beast threatening the sacred grounds."
        target = pick_hostile_animal(world)
        if not target:
            return None
        return Quest(
            quest_id,
            npc.name,
            desc,
            "animal",
            target,
            reward_xp=50,
            reward_items=[{"name": "Blessed Charm", "type": "artifact"}],
        )

    # -----------------------------------------------------
    # EMISSARY QUESTS
    # -----------------------------------------------------
    if getattr(npc, "is_emissary", False):
        desc = f"Deliver a message to a member of the {npc.faction}."
        return Quest(
            quest_id,
            npc.name,
            desc,
            "npc",
            f"{npc.faction} Guard",
            reward_xp=35,
            reward_items=[{"name": "Faction Token", "type": "currency"}],
        )

    # -----------------------------------------------------
    # BANDIT QUESTS (rare)
    # -----------------------------------------------------
    if getattr(npc, "is_ambusher", False):
        desc = "Steal supplies from a nearby campfire."
        return Quest(
            quest_id,
            npc.name,
            desc,
            "location",
            "campfire",
            reward_xp=25,
            reward_items=[{"name": "Stolen Goods", "type": "junk"}],
        )

    # -----------------------------------------------------
    # GENERIC QUEST-GIVER QUESTS
    # -----------------------------------------------------
    quest_type = random.choice(["hunt", "deliver", "visit"])

    if quest_type == "hunt":
        target = pick_hostile_animal(world)
        if not target:
            return None
        desc = f"Hunt down a {target} that has been troubling the area."
        return Quest(
            quest_id,
            npc.name,
            desc,
            "animal",
            target,
            reward_xp=30,
            reward_items=[{"name": "Pouch of Coins", "type": "currency"}],
        )

    if quest_type == "deliver":
        desc = "Deliver a message to a wandering scout."
        return Quest(
            quest_id,
            npc.name,
            desc,
            "npc",
            "Scout",
            reward_xp=20,
            reward_items=[{"name": "Ration Pack", "type": "food"}],
        )

    if quest_type == "visit":
        desc = "Visit a hidden shrine and return with what you learn."
        return Quest(
            quest_id,
            npc.name,
            desc,
            "location",
            "shrine",
            reward_xp=25,
            reward_items=[{"name": "Shrine Token", "type": "artifact"}],
        )

    return None


# ---------------------------------------------------------
# HELPER: PICK HOSTILE ANIMAL
# ---------------------------------------------------------

def pick_hostile_animal(world):
    candidates = []
    for room in world.rooms.values():
        for a in room.animals:
            if getattr(a, "hostile", False):
                candidates.append(a.name)
    return random.choice(candidates) if candidates else None


# ---------------------------------------------------------
# QUEST COMPLETION CHECK
# ---------------------------------------------------------

def check_quest_completion(player, world):
    """
    Checks all active quests and marks them completed if conditions are met.
    """

    for quest in player.quests:
        if quest.completed:
            continue

        # ANIMAL QUEST
        if quest.target_type == "animal":
            if not animal_exists(world, quest.target_name):
                quest.completed = True

        # NPC QUEST
        elif quest.target_type == "npc":
            if npc_exists(world, quest.target_name):
                quest.completed = True

        # LOCATION QUEST
        elif quest.target_type == "location":
            room = world.get_room(player.room_id)
            if quest.target_name in room.tags:
                quest.completed = True

        # ITEM QUEST (future expansion)
        elif quest.target_type == "item":
            pass  # inventory system needed


# ---------------------------------------------------------
# COMPLETION HELPERS
# ---------------------------------------------------------

def animal_exists(world, name):
    for room in world.rooms.values():
        for a in room.animals:
            if a.name == name:
                return True
    return False


def npc_exists(world, name):
    for room in world.rooms.values():
        for n in room.npcs:
            if n.name == name:
                return True
    return False


# ---------------------------------------------------------
# TURNING IN QUESTS
# ---------------------------------------------------------

def turn_in_quest(player, npc):
    """
    Player turns in any completed quest belonging to this NPC.
    """

    completed = [
        q for q in player.quests
        if q.giver_name == npc.name and q.completed and not q.turned_in
    ]

    if not completed:
        return None

    quest = completed[0]
    quest.turned_in = True

    # Apply rewards
    player.xp += quest.reward_xp
    for item in quest.reward_items:
        player.inventory.append(item)

    # NPC trust boost
    if hasattr(npc, "adjust_trust"):
        npc.adjust_trust(+15)

    return quest
