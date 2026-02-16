from typing import Dict
from actors.npc import NPC
from ui.text_randomizer import rt
from ui.text_effects import type_text, dramatic, pause


# ============================================================
# DIALOGUE TREES
# ============================================================

DIALOGUE_TREES: Dict[str, Dict[str, dict]] = {
    "intro": {
        "start": {
            "text_key": "dialogue_intro_generic",
            "choices": {
                "choice_pass_through": ("neutral_reply", +0, 0),
                "choice_no_harm": ("friendly_reply", +5, -2),
                "choice_none_business": ("hostile_reply", -5, +5),
            },
        },
        "neutral_reply": {
            "text_key": "dialogue_neutral_reply",
            "choices": {
                "choice_who_are_you": ("ask_name", +2, 0),
                "choice_goodbye": ("end", 0, 0),
            },
        },
        "friendly_reply": {
            "text_key": "dialogue_friendly_reply",
            "choices": {
                "choice_offer_help": ("offer_help", +5, -2),
                "choice_safe_travels": ("end", 0, 0),
            },
        },
        "hostile_reply": {
            "text_key": "dialogue_hostile_reply",
            "choices": {
                "choice_sorry": ("neutral_reply", +3, -3),
                "choice_back_off": ("end", -5, +10),
            },
        },
        "ask_name": {
            "text_key": "dialogue_ask_name",
            "choices": {
                "choice_help": ("offer_help", +3, 0),
                "choice_goodbye": ("end", 0, 0),
            },
        },
        "offer_help": {
            "text_key": "dialogue_offer_help",
            "choices": {
                "choice_tell_more": ("unlock_quest", +5, 0),
                "choice_not_interested": ("end", 0, 0),
            },
        },
        "unlock_quest": {
            "text_key": "dialogue_unlock_quest",
            "choices": {
                "choice_accept": ("give_quest", +5, -2),
                "choice_later": ("end", 0, 0),
            },
        },
        "give_quest": {
            "text_key": "dialogue_give_quest",
            "choices": {
                "choice_return_soon": ("end", 0, 0),
            },
        },
        "end": {
            "text_key": "dialogue_end",
            "choices": {}
        },
    }
}


# ============================================================
# CORE HELPERS
# ============================================================

def start_dialogue(npc: NPC) -> str:
    """Entry point for structured intro."""
    return "start"


def get_node(tree_name: str, node_key: str) -> dict:
    return DIALOGUE_TREES[tree_name][node_key]


def _trust_hostility_suffix(npc: NPC) -> str:
    if npc.trust > 50:
        return " Their tone is warm."
    if npc.trust < -20:
        return " Their voice is tense."
    if npc.hostility > 50:
        return " There's an edge in their words."
    return ""


def _mood_suffix(npc: NPC) -> str:
    mood = npc.mood()
    if mood == "hostile":
        return " They look like they'd rather be rid of you."
    if mood == "warm":
        return " They seem genuinely at ease in your presence."
    if mood == "uneasy":
        return " Something in their posture says they're on edge."
    if mood == "cold":
        return " There's a distance in their eyes."
    return ""


def _role_faction_companion_flavor(npc: NPC, player, world=None) -> str:
    lines = []

    # Role flavor
    if npc.is_guardian:
        lines.append(f"{npc.name} stands like a sentinel, duty etched into every movement.")
    if npc.is_emissary:
        lines.append(f"{npc.name} weighs you with the quiet caution of someone who speaks for others.")
    if npc.is_storyteller:
        lines.append(f"{npc.name}'s eyes flicker like they're holding back a dozen stories.")
    if npc.is_ambusher:
        lines.append(f"{npc.name} watches your hands more than your face.")

    # Faction flavor
    if npc.faction and hasattr(player, "reputation"):
        rep = player.reputation.get(npc.faction, 0)
        if rep > 20:
            lines.append(f"They've clearly heard decent things about you among {npc.faction}.")
        elif rep < -20:
            lines.append(f"Your name doesn't sit well with {npc.faction}, and it shows.")

    # Companion flavor
    if hasattr(player, "companions") and player.companions:
        for comp in player.companions:
            if getattr(comp, "legendary", False):
                lines.append(f"Their gaze keeps drifting back to {comp.name}, half awe, half fear.")
                break

    return " ".join(lines)


def _inventory_flavor(player) -> str:
    if not hasattr(player, "inventory"):
        return ""
    if not player.inventory:
        return ""
    # Simple: react to rare/legendary tags if present
    rare = [item for item in player.inventory if getattr(item, "rarity", "") in ("rare", "legendary")]
    if rare:
        return " Their eyes linger on the gear you carry."
    return ""


def _injury_flavor(player) -> str:
    if not hasattr(player, "hp") or not hasattr(player, "max_hp"):
        return ""
    ratio = player.hp / max(player.max_hp, 1)
    if ratio < 0.3:
        return " They can't help but notice how badly you're hurt."
    if ratio < 0.6:
        return " They glance at your wounds more than once."
    return ""


def _time_of_day_flavor(world) -> str:
    # Flexible: support either world.time_of_day or world.hour
    tod = getattr(world, "time_of_day", None)
    hour = getattr(world, "hour", None)

    if tod:
        if tod == "night":
            return " The darkness between you makes every word feel heavier."
        if tod == "dawn":
            return " The first light of day softens the edges of the conversation."
        if tod == "dusk":
            return " The fading light makes everything feel a little more fragile."
    elif hour is not None:
        if 22 <= hour or hour < 5:
            return " It's late, and fatigue hangs in the air."
        if 5 <= hour < 9:
            return " Morning chill still clings to the world."
        if 18 <= hour < 22:
            return " Evening shadows stretch long around you."

    return ""


# ============================================================
# RENDERING STRUCTURED NODES
# ============================================================

def render_node(npc: NPC, node: dict, player=None, world=None):
    text_key = node["text_key"]
    base = rt(text_key, npc=npc.name)

    suffix = _trust_hostility_suffix(npc) + _mood_suffix(npc)
    flavor = ""
    if player is not None:
        flavor_parts = [
            _role_faction_companion_flavor(npc, player, world),
            _inventory_flavor(player),
            _injury_flavor(player),
        ]
        if world is not None:
            flavor_parts.append(_time_of_day_flavor(world))
        flavor = " ".join(p for p in flavor_parts if p)

    line = base + suffix
    if flavor:
        line += " " + flavor

    dramatic(line)
    pause(0.2)


def render_choices(node: dict):
    if not node["choices"]:
        return None

    type_text(rt("dialogue_choice_prompt"))

    keys = list(node["choices"].keys())
    for i, choice_key in enumerate(keys, 1):
        type_text(f"{i}. {rt(choice_key)}")

    raw = input("> ").strip()
    if raw.isdigit():
        idx = int(raw) - 1
        if 0 <= idx < len(keys):
            return keys[idx]

    return None


# ============================================================
# PROCESSING CHOICES
# ============================================================

def process_choice(npc: NPC, tree_name: str, node_key: str, choice_key: str):
    node = get_node(tree_name, node_key)
    next_key, trust_change, hostility_change = node["choices"][choice_key]

    npc.adjust_trust(trust_change)
    npc.adjust_hostility(hostility_change)

    npc.remember(f"choice:{tree_name}:{node_key}:{choice_key}")

    # Storyteller hook (placeholder)
    if npc.is_storyteller and next_key == "end":
        if npc.recalls("rumor_key"):
            dramatic(rt("rumor_key"))

    # Quest hook
    if next_key == "give_quest":
        npc.has_quest = True
        npc.remember("gave_quest")
        npc.adjust_trust(+10)

    # Emissary respect/insult memory
    if npc.is_emissary:
        if trust_change > 0:
            npc.remember("player_respected_emissary")
        if hostility_change > 0:
            npc.remember("player_insulted_emissary")

    # Guardian reaction
    if npc.is_guardian and hostility_change > 0:
        dramatic(f"{npc.name} warns you not to disrespect the shrine.")

    # Ambusher reaction
    if npc.is_ambusher and hostility_change > 0:
        dramatic(f"{npc.name} grins. 'Keep talking like that and see what happens.'")

    # Follower hook
    if npc.trust > 60 and not npc.is_follower and next_key == "end":
        dramatic(f"{npc.name} steps closer. 'If you need company… I could travel with you.'")
        npc.following_player = True

    return next_key


# ============================================================
# STRUCTURED INTRO → AI MODE
# ============================================================

def run_intro_dialogue(npc: NPC, player, world=None, tree_name: str = "intro"):
    current_key = start_dialogue(npc)

    while True:
        node = get_node(tree_name, current_key)
        render_node(npc, node, player=player, world=world)

        if not node["choices"]:
            break

        choice_key = render_choices(node)
        if not choice_key:
            dramatic(rt("dialogue_invalid_choice"))
            break

        current_key = process_choice(npc, tree_name, current_key, choice_key)
        if current_key == "end":
            end_node = get_node(tree_name, "end")
            render_node(npc, end_node, player=player, world=world)
            break


# ============================================================
# AI CONVERSATION LOOP
# ============================================================

def enter_ai_conversation(npc: NPC, player, world=None):
    dramatic(f"{npc.name} watches you closely. 'Speak freely now.'")

    while True:
        text = input("You: ").strip()
        if not text:
            dramatic("You say nothing.")
            continue

        if text.lower() in ["bye", "goodbye", "leave", "stop", "farewell"]:
            dramatic(f"{npc.name} nods slightly and looks away.")
            break

        reply = npc.speak(player, text, world)
        dramatic(reply)


# ============================================================
# NPC-INITIATED CONVERSATIONS & AMBIENT CHATTER
# ============================================================

def maybe_npc_initiates_conversation(npc: NPC, player, world=None):
    """
    Call this occasionally (e.g., after movement) to let followers or
    high-trust NPCs start talking on their own.
    """
    import random

    if not getattr(npc, "following_player", False):
        return

    if npc.trust < 30:
        return

    if random.random() > 0.15:
        return

    opener = npc.speak(player, "…", world)
    dramatic(f"{npc.name} breaks the silence.")
    dramatic(opener)


def ambient_chatter_in_room(room, player, world=None):
    """
    Light AI-driven ambient chatter from NPCs in the room.
    Call this after describe_room or on a timer.
    """
    import random

    if not room.npcs:
        return

    for npc in room.npcs:
        if random.random() > 0.1:
            continue
        line = npc.speak(player, "ambient", world)
        dramatic(line)


# ============================================================
# HIGH-LEVEL ENTRY POINT
# ============================================================

def talk_to_npc(npc: NPC, player, world=None):
    """
    High-level function:
        1. Run structured intro tree once
        2. Then enter AI-driven free-text conversation
    """
    if not npc.recalls("intro_done"):
        run_intro_dialogue(npc, player, world)
        npc.remember("intro_done")

    enter_ai_conversation(npc, player, world)
