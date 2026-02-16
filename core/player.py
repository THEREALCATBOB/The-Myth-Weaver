from ui.text_randomizer import rt


class Player:
    def __init__(self, name, room_id):
        self.name = name
        self.room_id = room_id

        # Core stats
        self.level = 1
        self.xp = 0
        self.max_hp = 30
        self.hp = self.max_hp
        self.atk = 5
        self.defense = 2
        self.speed = 3

        # Survival
        self.hunger = 0
        self.thirst = 0
        self.fatigue = 0
        self.body_temp = 37.0

        # Systems
        self.inventory = []
        self.companions = []      # animals or NPC followers
        self.mount = None
        self.status_effects = []
        self.faction = None
        self.reputation = {}      # faction_name -> value

        # QUEST SYSTEM
        self.quests = []          # list of Quest objects
        self.last_quest_giver = None

        # MEMORY HOOKS FOR NPC AI
        self.last_action = None   # "help", "threaten", "gift", etc.

    # ---------------------------------------------------------
    # DYNAMIC COMBAT STATS (followers + survival)
    # ---------------------------------------------------------
    def effective_atk(self):
        atk = self.atk

        # Followers boost morale
        if self.companions:
            atk += len(self.companions)

        # Hunger/thirst penalties
        if self.hunger > 70:
            atk -= 2
        if self.thirst > 70:
            atk -= 2

        return max(1, atk)

    def effective_defense(self):
        defense = self.defense

        if self.companions:
            defense += len(self.companions)

        if self.fatigue > 70:
            defense -= 2

        return max(0, defense)

    # ---------------------------------------------------------
    # LEVELING (Cinematic)
    # ---------------------------------------------------------
    def gain_xp(self, amount):
        self.xp += amount

        leveled_up = False
        messages = []

        while self.xp >= self.level * 20:
            self.xp -= self.level * 20
            self.level += 1
            leveled_up = True

            # Stat increases
            self.max_hp += 5
            self.hp = self.max_hp
            self.atk += 1
            self.defense += 1

            messages.append(rt("player_level_up", level=self.level))

        return messages if leveled_up else []

    # ---------------------------------------------------------
    # INVENTORY (Cinematic)
    # ---------------------------------------------------------
    def add_item(self, item):
        self.inventory.append(item)
        return rt("inventory_add", item=item["name"])

    def remove_item(self, item_name):
        for i, item in enumerate(self.inventory):
            if item["name"].lower() == item_name.lower():
                return self.inventory.pop(i)
        return None

    # ---------------------------------------------------------
    # REPUTATION (Cinematic + stat influence)
    # ---------------------------------------------------------
    def modify_reputation(self, faction_name, delta):
        old = self.reputation.get(faction_name, 0)
        new = max(-100, min(100, old + delta))
        self.reputation[faction_name] = new

        # Small stat effects
        if new > 50:
            self.atk = max(self.atk, self.atk + 0)  # placeholder for buffs
        elif new < -50:
            self.defense = max(0, self.defense - 0)  # placeholder for debuffs

        if delta > 0:
            return rt("rep_gain", faction=faction_name, amount=delta)
        elif delta < 0:
            return rt("rep_loss", faction=faction_name, amount=abs(delta))
        else:
            return rt("rep_neutral", faction=faction_name)

    # ---------------------------------------------------------
    # QUEST SYSTEM
    # ---------------------------------------------------------

    def add_quest(self, quest):
        """Add a new quest to the player's quest log."""
        self.quests.append(quest)
        self.last_quest_giver = quest.giver_name
        return rt("quest_received", quest=quest.description)

    def active_quests(self):
        return [q for q in self.quests if not q.completed]

    def completed_quests(self):
        return [q for q in self.quests if q.completed and not q.turned_in]

    def quest_log(self):
        if not self.quests:
            return rt("quest_log_empty")

        lines = []
        for q in self.quests:
            status = "✓ Completed" if q.completed else "In Progress"
            lines.append(f"{q.id}: {q.description} — {status}")

        return "\n".join(lines)

    def has_quest_from(self, npc_name):
        return any(q.giver_name == npc_name and not q.turned_in for q in self.quests)

    def turn_in_quest(self, quest, npc):
        """Apply quest rewards and mark as turned in."""
        quest.turned_in = True

        # XP reward
        self.xp += quest.reward_xp

        # Item rewards (cinematic)
        for item in quest.reward_items:
            self.add_item(item)

        # NPC trust boost
        if hasattr(npc, "adjust_trust"):
            npc.adjust_trust(+15)

        # Level-up check
        msgs = self.gain_xp(0)

        # Memory hook
        self.last_action = "quest_turn_in"

        return rt("quest_turned_in", quest=quest.description)

    # ---------------------------------------------------------
    # PLAYER ACTION MEMORY (NPCs react to this)
    # ---------------------------------------------------------
    def record_action(self, action: str):
        """
        Store the last meaningful action the player took.
        NPCs can read this to adjust trust/fear/hostility.
        """
        self.last_action = action
