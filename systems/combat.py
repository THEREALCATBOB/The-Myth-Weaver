import random
from ui.text_effects import type_text, dramatic, pause
from ui.text_randomizer import rt


# ---------------------------------------------------------
# STATUS EFFECTS (Improved)
# ---------------------------------------------------------
def apply_status_effects(entity):
    messages = []
    stunned = False

    if not hasattr(entity, "status_effects"):
        entity.status_effects = []

    new_effects = []
    for effect in entity.status_effects:
        etype = effect["type"]
        duration = effect["duration"]

        if etype == "bleed":
            dmg = 2
            entity.hp -= dmg
            messages.append(rt("combat_status_bleed"))

        elif etype == "poison":
            dmg = 3
            entity.hp -= dmg
            messages.append(rt("combat_status_poison"))

        elif etype == "burn":
            dmg = 4
            entity.hp -= dmg
            messages.append(rt("combat_status_burn"))

        elif etype == "stun":
            stunned = True
            messages.append(rt("combat_status_stun"))

        duration -= 1
        if duration > 0:
            new_effects.append({"type": etype, "duration": duration})

    entity.status_effects = new_effects
    return messages, stunned


# ---------------------------------------------------------
# HIT / DAMAGE CALCULATION (Uses Player Effective Stats)
# ---------------------------------------------------------
def calculate_hit(attacker, defender):
    speed_diff = defender.speed - attacker.speed
    dodge_chance = max(0, min(40, 10 + speed_diff * 3))
    roll = random.randint(1, 100)

    if roll <= dodge_chance:
        return False, True, False

    block_chance = 10
    roll = random.randint(1, 100)
    if roll <= block_chance:
        return True, False, True

    return True, False, False


def calculate_damage(attacker, defender, base_mult=1.0, crit_chance=10, crit_mult=1.5):
    # Use effective stats if available
    atk = attacker.effective_atk() if hasattr(attacker, "effective_atk") else attacker.atk
    defense = defender.effective_defense() if hasattr(defender, "effective_defense") else defender.defense

    hit, dodged, blocked = calculate_hit(attacker, defender)

    if dodged:
        return 0, False, False, True

    if not hit:
        return 0, False, False, False

    base = atk + random.randint(0, 3)
    base = int(base * base_mult)
    reduction = defense // 2
    dmg = max(1, base - reduction)

    crit = random.randint(1, 100) <= crit_chance
    if crit:
        dmg = int(dmg * crit_mult)

    if blocked:
        dmg = max(1, dmg // 2)

    return dmg, crit, blocked, False


# ---------------------------------------------------------
# FOLLOWER PROTECTION
# ---------------------------------------------------------
def follower_protect(player, enemy):
    """Followers may block or intercept attacks."""
    if not getattr(player, "companions", None):
        return False

    if random.random() < 0.25:
        companion = random.choice(player.companions)
        dramatic(rt("combat_companion_protect", animal=companion.name))
        return True

    return False


# ---------------------------------------------------------
# PLAYER TURN
# ---------------------------------------------------------
def player_turn(player, enemy):
    dramatic(rt("combat_player_turn"))

    status_msgs, stunned = apply_status_effects(player)
    for msg in status_msgs:
        type_text(msg)
        pause()

    if player.hp <= 0:
        return "defeat"

    if stunned:
        dramatic(rt("combat_player_hesitate"))
        return None

    # Companion assist
    for companion in getattr(player, "companions", []):
        if getattr(companion, "hostile", False):
            continue
        if random.random() < 0.4:
            dmg = random.randint(2, 5)
            enemy.hp -= dmg
            dramatic(rt("combat_companion_attack", animal=companion.name))
            pause(0.2)

    type_text(rt("combat_player_choice"))
    choice = input("> ").strip().lower()

    if choice in ["1", "a", "attack"]:
        dmg, crit, blocked, dodged = calculate_damage(player, enemy)

        if dodged:
            dramatic(rt("combat_enemy_dodge", enemy=enemy.name))
        else:
            if blocked:
                type_text(rt("combat_enemy_block", enemy=enemy.name))
            if crit:
                dramatic(rt("combat_crit_player", enemy=enemy.name))
            type_text(rt("combat_player_damage", enemy=enemy.name))
            enemy.hp -= dmg

    elif choice in ["2", "s", "special"]:
        dmg, crit, blocked, dodged = calculate_damage(
            player, enemy, base_mult=1.5, crit_chance=20, crit_mult=2.0
        )

        if dodged:
            dramatic(rt("combat_enemy_dodge", enemy=enemy.name))
        else:
            if blocked:
                type_text(rt("combat_enemy_block", enemy=enemy.name))
            if crit:
                dramatic(rt("combat_crit_player", enemy=enemy.name))
            dramatic(rt("combat_player_special"))
            enemy.hp -= dmg

    elif choice in ["3", "m", "magic"]:
        base = player.effective_atk() + 5 + random.randint(0, 4)
        reduction = enemy.defense // 4
        dmg = max(2, base - reduction)

        if random.randint(1, 100) <= 25:
            dmg = int(dmg * 1.8)
            dramatic(rt("combat_magic_crit", enemy=enemy.name))

        dramatic(rt("combat_magic_hit", enemy=enemy.name))
        enemy.hp -= dmg

    elif choice in ["4", "d", "defend"]:
        player.defense += 3
        dramatic(rt("combat_player_defend"))

    else:
        dramatic(rt("combat_player_hesitate"))

    return None


# ---------------------------------------------------------
# ENEMY TURN
# ---------------------------------------------------------
def enemy_basic_attack(enemy, player):
    # Followers may intercept
    if follower_protect(player, enemy):
        return

    dmg, crit, blocked, dodged = calculate_damage(enemy, player)

    if dodged:
        dramatic(rt("combat_player_dodge"))
    else:
        if blocked:
            type_text(rt("combat_player_block"))
        if crit:
            dramatic(rt("combat_crit_enemy", enemy=enemy.name))
        type_text(rt("combat_enemy_damage", enemy=enemy.name))
        player.hp -= dmg


def enemy_special_ability(enemy, player):
    if not hasattr(player, "status_effects"):
        player.status_effects = []

    ability = random.choice(["heavy", "bleed", "stun"])

    if ability == "heavy":
        if follower_protect(player, enemy):
            return

        dmg, crit, blocked, dodged = calculate_damage(
            enemy, player, base_mult=1.6, crit_chance=15, crit_mult=2.0
        )

        if dodged:
            dramatic(rt("combat_player_dodge"))
        else:
            if blocked:
                type_text(rt("combat_player_block"))
            if crit:
                dramatic(rt("combat_crit_enemy", enemy=enemy.name))
            dramatic(rt("combat_enemy_heavy", enemy=enemy.name))
            player.hp -= dmg

    elif ability == "bleed":
        player.status_effects.append({"type": "bleed", "duration": 3})

    elif ability == "stun":
        player.status_effects.append({"type": "stun", "duration": 1})


def enemy_turn(player, enemy):
    dramatic(rt("combat_enemy_turn", enemy=enemy.name))

    status_msgs, stunned = apply_status_effects(enemy)
    for msg in status_msgs:
        type_text(msg)
        pause()

    if enemy.hp <= 0:
        return "victory"

    if stunned:
        dramatic(rt("combat_enemy_dodge", enemy=enemy.name))
        return None

    if random.randint(1, 100) <= 25:
        enemy_special_ability(enemy, player)
    else:
        enemy_basic_attack(enemy, player)

    if player.hp <= 0:
        return "defeat"

    return None


# ---------------------------------------------------------
# MAIN COMBAT LOOP (NPC AI reactions added)
# ---------------------------------------------------------
def start_combat(player, enemy, world=None):
    # Cinematic intro
    if getattr(enemy, "legendary", False):
        dramatic(rt("legendary_intro", animal=enemy.name))
    elif enemy.__class__.__name__ == "Enemy":
        dramatic(rt("enemy_appears", enemy=enemy.name, biome=getattr(enemy, "biome", "unknown")))
    else:
        dramatic(rt("animal_hostile", animal=enemy.name))

    if not hasattr(player, "status_effects"):
        player.status_effects = []
    if not hasattr(enemy, "status_effects"):
        enemy.status_effects = []

    player_first = player.speed >= enemy.speed

    while True:
        if player_first:
            result = player_turn(player, enemy)
            if result == "defeat":
                dramatic(rt("combat_defeat", enemy=enemy.name))
                if world:     
                    for npc in world.get_room(player.room_id).npcs:
                        npc.react_to_combat_outcome(player, "player_lost")

                player.last_action = "combat_loss"
                return "defeat"
            if enemy.hp <= 0:
                dramatic(rt("combat_victory", enemy=enemy.name))
                if world:
                    for npc in world.get_room(player.room_id).npcs:
                        npc.react_to_combat_outcome(player, "player_won")
                player.last_action = "combat_win"
                return "victory"

        result = enemy_turn(player, enemy)
        if result == "victory":
            dramatic(rt("combat_victory", enemy=enemy.name))
            if world:
                for npc in world.get_room(player.room_id).npcs:
                    npc.react_to_combat_outcome(player, "player_won")
            player.last_action = "combat_win"
            return "victory"
        if result == "defeat":
            dramatic(rt("combat_defeat", enemy=enemy.name))
            if world:
                for npc in world.get_room(player.room_id).npcs:
                    npc.react_to_combat_outcome(player, "player_lost")
            player.last_action = "combat_loss"
            return "defeat"

        if not player_first:
            result = player_turn(player, enemy)
            if result == "defeat":
                dramatic(rt("combat_defeat", enemy=enemy.name))
                if world:
                    for npc in world.get_room(player.room_id).npcs:
                        npc.react_to_combat_outcome(False)
                player.last_action = "combat_loss"
                return "defeat"
            if enemy.hp <= 0:
                dramatic(rt("combat_victory", enemy=enemy.name))
                if world:
                    for npc in world.get_room(player.room_id).npcs:
                        npc.react_to_combat_outcome(True)
                player.last_action = "combat_win"
                return "victory"
