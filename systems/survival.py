import random
from ui.text_randomizer import rt


# =========================================================
# BIOME EFFECTS (CINEMATIC, EXTENDED)
# =========================================================

def apply_biome_effects(player, world, room):
    """
    Applies environmental effects based on biome.
    Returns a cinematic biome effect message (or None).
    """
    biome = room.biome
    msg_key = None

    # Desert: heat + dehydration
    if biome == "desert":
        player.thirst = min(100, player.thirst + 4)
        player.body_temp += 0.2
        msg_key = "biome_effect_desert"

    # Swamp: humidity + fatigue
    elif biome == "swamp":
        player.fatigue = min(100, player.fatigue + 3)
        msg_key = "biome_effect_swamp"

    # Mountain: cold + body temperature drop
    elif biome == "mountain":
        player.body_temp -= 0.3
        msg_key = "biome_effect_mountain"

    # Forest: mild fatigue
    elif biome == "forest":
        player.fatigue = min(100, player.fatigue + 1)
        msg_key = "biome_effect_forest"

    # Plains: neutral biome
    elif biome == "plains":
        msg_key = None

    # Tundra: severe cold
    elif biome == "tundra":
        player.body_temp -= 0.4
        player.fatigue = min(100, player.fatigue + 2)
        msg_key = "biome_effect_tundra"

    # Jungle: humidity + fatigue + thirst
    elif biome == "jungle":
        player.fatigue = min(100, player.fatigue + 3)
        player.thirst = min(100, player.thirst + 3)
        msg_key = "biome_effect_jungle"

    # Volcanic: heat + thirst
    elif biome == "volcanic":
        player.body_temp += 0.4
        player.thirst = min(100, player.thirst + 4)
        msg_key = "biome_effect_volcanic"

    # Ruins: mild fatigue, no temp change
    elif biome == "ruins":
        player.fatigue = min(100, player.fatigue + 1)
        msg_key = "biome_effect_ruins"

    # Coast: mild thirst from salt air
    elif biome == "coast":
        player.thirst = min(100, player.thirst + 2)
        msg_key = "biome_effect_coast"

    # Deep forest: fatigue + slight chill
    elif biome == "deep_forest":
        player.fatigue = min(100, player.fatigue + 2)
        player.body_temp -= 0.1
        msg_key = "biome_effect_deep_forest"

    # Crystal caverns: mild cold
    elif biome == "crystal_caverns":
        player.body_temp -= 0.2
        msg_key = "biome_effect_crystal_caverns"

    # Corrupted lands: fatigue + small HP chip
    elif biome == "corrupted_lands":
        player.fatigue = min(100, player.fatigue + 2)
        player.hp -= 1
        msg_key = "biome_effect_corrupted_lands"

    # Weather overlays (heatwave, blizzard, sandstorm, etc.)
    weather = getattr(world, "weather", "").lower()
    if weather == "heatwave":
        player.thirst = min(100, player.thirst + 2)
        player.body_temp += 0.2
    elif weather == "blizzard":
        player.body_temp -= 0.3
        player.fatigue = min(100, player.fatigue + 1)
    elif weather == "sandstorm":
        player.fatigue = min(100, player.fatigue + 2)
    elif weather == "mist":
        player.fatigue = min(100, player.fatigue + 1)

    # Body temperature self‑correction (slow)
    if player.body_temp < 36.5:
        player.body_temp += 0.1
    if player.body_temp > 37.5:
        player.body_temp -= 0.1

    # Return cinematic text if available
    if msg_key:
        return rt(msg_key, biome=biome)

    return None


# =========================================================
# SURVIVAL TICK (HUNGER / THIRST / FATIGUE)
# =========================================================

def update_survival(player, world):
    """
    Updates hunger, thirst, fatigue, and checks for danger.
    Returns (status, warning_message)
    """
    warning_key = None

    # Base natural increases
    hunger_inc = 1
    thirst_inc = 2
    fatigue_inc = 1

    # Mount reduces fatigue and thirst slightly
    if getattr(player, "mount", None):
        thirst_inc = max(0, thirst_inc - 1)
        fatigue_inc = max(0, fatigue_inc - 1)

    # Companions make travel feel easier (small fatigue reduction)
    if getattr(player, "companions", None):
        fatigue_inc = max(0, fatigue_inc - 1)

    player.hunger = min(100, player.hunger + hunger_inc)
    player.thirst = min(100, player.thirst + thirst_inc)
    player.fatigue = min(100, player.fatigue + fatigue_inc)

    # Starvation
    if player.hunger >= 100:
        player.hp -= 2
        warning_key = "warning_starving"

    # Dehydration
    if player.thirst >= 100:
        player.hp -= 3
        warning_key = "warning_dehydrated"

    # Exhaustion
    if player.fatigue >= 100:
        player.hp -= 1
        warning_key = "warning_exhausted"

    # Hypothermia
    if player.body_temp <= 35.0:
        player.hp -= 2
        warning_key = "warning_hypothermia"

    # Heatstroke
    if player.body_temp >= 39.0:
        player.hp -= 2
        warning_key = "warning_heatstroke"

    # Death check
    if player.hp <= 0:
        return "defeat", rt("warning_death")

    if warning_key:
        return None, rt(warning_key)

    return None, None


# =========================================================
# CAMPING / RESTING
# =========================================================

def camp(player, world, room):
    """
    Rest to reduce fatigue and restore HP.
    Camping always advances time.
    """
    player.fatigue = max(0, player.fatigue - 40)
    player.hp = min(player.max_hp, player.hp + 12)
    player.body_temp = 37.0  # reset to normal

    world.advance_time(6)

    # Memory hook if available
    if hasattr(player, "record_action"):
        player.record_action("camp")

    # Campfire bonus
    if "campfire" in getattr(room, "tags", []):
        return rt("rest_campfire")

    return rt("rest_camp")


# =========================================================
# FOOD SPOILAGE
# =========================================================

def tick_spoilage(player):
    """
    Spoils food over time.
    5% chance per day for each food item.
    """
    new_inv = []
    for item in player.inventory:
        if item.get("type") == "food":
            if random.random() < 0.05:
                # Food spoiled — cinematic message if key exists
                try:
                    rt("food_spoil", item=item.get("name", "food"))
                except KeyError:
                    pass
                continue
        new_inv.append(item)

    player.inventory = new_inv


# =========================================================
# EATING FOOD
# =========================================================

def eat_food(player, item_name):
    """
    Eat food from inventory.
    """
    item = player.remove_item(item_name)
    if not item:
        return rt("error_no_item")

    if item.get("type") != "food":
        return rt("error_not_food")

    # Restore survival stats
    player.hunger = max(0, player.hunger - 35)
    player.thirst = max(0, player.thirst - 15)
    player.hp = min(player.max_hp, player.hp + 6)

    # Memory hook
    if hasattr(player, "record_action"):
        player.record_action("eat")

    return rt("eat_food", item=item_name)
