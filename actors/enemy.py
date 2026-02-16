from dataclasses import dataclass, field
import random
from ui.text_randomizer import rt


# ---------------------------------------------------------
# ENEMY ABILITIES (Cinematic + Tactical)
# ---------------------------------------------------------

ENEMY_ABILITIES = {
    "strike": {
        "name": "Strike",
        "power": 1.0,
        "cooldown": 0,
        "description_key": "enemy_ability_strike"
    },
    "heavy_strike": {
        "name": "Heavy Strike",
        "power": 1.5,
        "cooldown": 2,
        "description_key": "enemy_ability_heavy"
    },
    "bleed": {
        "name": "Bleeding Bite",
        "power": 0.8,
        "cooldown": 3,
        "status": "bleed",
        "description_key": "enemy_ability_bleed"
    },
    "stun": {
        "name": "Stunning Blow",
        "power": 0.7,
        "cooldown": 4,
        "status": "stun",
        "description_key": "enemy_ability_stun"
    },
    "shadow_step": {
        "name": "Shadow Step",
        "power": 0.6,
        "cooldown": 3,
        "status": "dodge",
        "description_key": "enemy_ability_shadow"
    },
}


# ---------------------------------------------------------
# ENEMY TIER STAT TABLE (7 tiers)
# ---------------------------------------------------------

TIER_STATS = {
    1: {"hp": 12, "atk": 3, "def": 1, "speed": 2},
    2: {"hp": 20, "atk": 5, "def": 2, "speed": 3},
    3: {"hp": 28, "atk": 7, "def": 3, "speed": 4},
    4: {"hp": 40, "atk": 10, "def": 4, "speed": 5},
    5: {"hp": 55, "atk": 13, "def": 5, "speed": 6},
    6: {"hp": 75, "atk": 17, "def": 7, "speed": 7},
    7: {"hp": 120, "atk": 22, "def": 10, "speed": 8},  # Boss tier
}


# ---------------------------------------------------------
# ENEMY CLASS (Cinematic + Randomized)
# ---------------------------------------------------------

@dataclass
class Enemy:
    id: str
    name: str
    tier: int
    biome: str
    behavior: str  # "aggressive", "defensive", "opportunistic", etc.
    weaknesses: list = field(default_factory=list)
    abilities: list = field(default_factory=list)

    hp: int = 0
    max_hp: int = 0
    atk: int = 0
    defense: int = 0
    speed: int = 0

    cooldowns: dict = field(default_factory=dict)
    status_effects: dict = field(default_factory=dict)

    def __post_init__(self):
        stats = TIER_STATS[self.tier]
        self.max_hp = stats["hp"]
        self.hp = stats["hp"]
        self.atk = stats["atk"]
        self.defense = stats["def"]
        self.speed = stats["speed"]

        # Initialize cooldowns
        for ability in self.abilities:
            self.cooldowns[ability] = 0

    # -----------------------------------------------------
    # Cinematic encounter intro
    # -----------------------------------------------------
    def intro_line(self):
        return rt("enemy_appears", enemy=self.name, biome=self.biome)

    # -----------------------------------------------------
    # Cinematic taunt (optional)
    # -----------------------------------------------------
    def taunt(self):
        return rt("enemy_taunt", enemy=self.name)

    # -----------------------------------------------------
    # AI: Choose ability based on behavior + cooldowns
    # -----------------------------------------------------
    def choose_ability(self):
        available = [a for a in self.abilities if self.cooldowns[a] == 0]

        if not available:
            return "strike"

        if self.behavior == "aggressive":
            weighted = ["heavy_strike", "bleed"] + available
        elif self.behavior == "defensive":
            weighted = ["stun", "shadow_step"] + available
        else:
            weighted = available

        return random.choice(weighted)

    # -----------------------------------------------------
    # Cinematic attack line
    # -----------------------------------------------------
    def attack_line(self, ability_key):
        ability = ENEMY_ABILITIES[ability_key]
        desc_key = ability["description_key"]
        return rt(desc_key, enemy=self.name)

    # -----------------------------------------------------
    # Apply cooldowns each turn
    # -----------------------------------------------------
    def tick_cooldowns(self):
        for a in self.cooldowns:
            if self.cooldowns[a] > 0:
                self.cooldowns[a] -= 1

    # -----------------------------------------------------
    # Apply status effects (bleed, stun, dodge)
    # -----------------------------------------------------
    def apply_status(self):
        effects = []

        if "bleed" in self.status_effects:
            dmg = self.status_effects["bleed"]
            self.hp -= dmg
            effects.append(rt("combat_status_bleed", enemy=self.name))

        if "stun" in self.status_effects:
            effects.append(rt("combat_status_stun", enemy=self.name))

        return effects

    # -----------------------------------------------------
    # Debug summary
    # -----------------------------------------------------
    def summary(self):
        return (
            f"{self.name} (Tier {self.tier}, HP: {self.hp}/{self.max_hp}, "
            f"Behavior: {self.behavior}, Weaknesses: {self.weaknesses})"
        )
