import random
from ui.text_randomizer import rt


class Animal:
    def __init__(self, name, hostile, biome, room_id, legendary=False, den_id=None):
        self.name = name
        self.hostile = hostile
        self.biome = biome
        self.room_id = room_id
        self.legendary = legendary
        self.den_id = den_id

        # Personalities: timid, aggressive, curious, territorial
        self.personality = random.choice(["timid", "aggressive", "curious", "territorial"])

        # Stats
        if legendary:
            self.hp = 120
            self.atk = 15
            self.defense = 8
            self.speed = 6
            self.tier = 5
        elif hostile:
            self.hp = random.randint(20, 35)
            self.atk = random.randint(3, 6)
            self.defense = random.randint(1, 3)
            self.speed = random.randint(2, 4)
            self.tier = 1
        else:
            self.hp = random.randint(10, 20)
            self.atk = 0
            self.defense = 0
            self.speed = random.randint(1, 3)
            self.tier = 0

        self.status_effects = []

        # Taming system
        self.trust = 0
        self.tamed = False
        self.mountable = name in ["Horse", "Camel", "Wolf", "Thunder Ram"]

        self.can_flee = not hostile
        self.can_be_tamed = not hostile or self.personality in ["curious", "timid"]
        self.is_animal = True

        self.pack_id = None  # for pack AI

    # ---------------------------------------------------------
    # FEEDING (Cinematic)
    # ---------------------------------------------------------
    def feed(self, item):
        if not self.can_be_tamed:
            return rt("tame_fail", animal=self.name)

        gain = random.randint(10, 25)
        self.trust += gain

        if self.trust >= 100:
            self.tamed = True
            return rt("tame_success", animal=self.name)

        return rt("feed_react", animal=self.name)

    # ---------------------------------------------------------
    # MOUNTING (Cinematic)
    # ---------------------------------------------------------
    def attempt_mount(self):
        if not self.tamed:
            return rt("tame_fail", animal=self.name)

        if not self.mountable:
            return rt("mount_fail", animal=self.name)

        return rt("mount_success", animal=self.name)

    # ---------------------------------------------------------
    # PERSONALITY REACTION (Cinematic)
    # ---------------------------------------------------------
    def reaction_text(self):
        key = f"animal_react_{self.personality}"

        # If the key doesn't exist, fall back to a generic reaction
        return rt(key, animal=self.name)

    # ---------------------------------------------------------
    # AI BEHAVIOR (Personality + Legendary)
    # ---------------------------------------------------------
    def decide_action(self, player):
        if self.legendary:
            return "attack"

        if self.personality == "timid":
            return "flee"

        if self.personality == "territorial":
            return "attack"

        if self.personality == "curious":
            return random.choice(["flee", "idle", "idle", "attack"])

        if self.personality == "aggressive":
            return "attack"

        return "idle"

    # ---------------------------------------------------------
    # LOOT TABLE (Legendary + Normal)
    # ---------------------------------------------------------
    def drop_loot(self):
        if self.legendary:
            return [
                {"name": "Legendary Hide", "type": "material"},
                {"name": "Ancient Bone", "type": "material"},
                {"name": "Beast Core", "type": "artifact"},
            ]

        loot = []
        if random.random() < 0.6:
            loot.append({"name": "Raw Meat", "type": "food"})
        if random.random() < 0.4:
            loot.append({"name": "Animal Hide", "type": "material"})
        if random.random() < 0.3:
            loot.append({"name": "Bone", "type": "material"})
        if random.random() < 0.1:
            loot.append({"name": "Rare Beast Claw", "type": "rare"})
        return loot

    # ---------------------------------------------------------
    # LEGENDARY SPAWNER (Cinematic)
    # ---------------------------------------------------------
    @staticmethod
    def spawn_legendary(biome, room_id):
        if biome == "forest":
            name = "Forest Guardian"
        elif biome == "desert":
            name = "Sand Wyrm"
        elif biome == "mountain":
            name = "Thunder Ram"
        elif biome == "swamp":
            name = "Swamp Leviathan"
        else:
            name = "Ancient Beast"

        beast = Animal(name, True, biome, room_id, legendary=True)
        return beast

    # ---------------------------------------------------------
    # DEBUG SUMMARY
    # ---------------------------------------------------------
    def summary(self):
        return (
            f"{self.name} (Legendary: {self.legendary}, Hostile: {self.hostile}, "
            f"Personality: {self.personality}, HP: {self.hp}, Trust: {self.trust})"
        )
