# =========================================================
# AI DIALOGUE ENGINE (DEEP, HIGH-RANDOMNESS, HYBRID PERSONALITY)
# systems/ai_dialogue.py
# =========================================================
#
# Design goals (based on Vikram's choices):
# - Deep AI: NPCs behave like full characters
# - Medium-length replies (2–4 sentences)
# - Rare refusals, only when trust is low or topic is sensitive
# - Hostile/shady NPCs can lie; others stay honest
# - Small, flavorful lore bits (rumors, hints, legends)
# - React to player typing style (aggressive, polite, cryptic, short, long)
# - Remember player lies and contradictions
# - Give subtle quest hints in AI mode
# - React to legendary companions
# - Medium amount of NPC questions (triggered by interesting input + curious personality)
# - High randomness in phrasing and flavor
# - Core personality never changes, but emotional drift and tone evolve
# - Hybrid storage: NPC holds core state; engine holds drift/suspicion/history
#
# NOTE:
# This file is intentionally verbose and richly structured to support
# cinematic, emergent NPC behavior and to approximate a large, feature-rich
# AI dialogue engine.

import random
from typing import Dict, List, Tuple, Optional


# ---------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------

def _clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def _chance(p: float) -> bool:
    return random.random() < p


def _normalize_text(text: str) -> str:
    return text.strip().lower()


def _contains_any(text: str, words: List[str]) -> bool:
    t = text.lower()
    return any(w in t for w in words)


# ---------------------------------------------------------
# Constants and configuration
# ---------------------------------------------------------

INTENT_HELP_WORDS = ["help", "assist", "aid", "quest", "job", "work", "task", "mission"]
INTENT_NAME_WORDS = ["name", "who are you", "who are u", "your name"]
INTENT_LOCATION_WORDS = ["where", "place", "here", "this area", "this place", "where am i"]
INTENT_LORE_WORDS = ["rumor", "story", "legend", "lore", "myth", "tale"]
INTENT_TRADE_WORDS = ["trade", "buy", "sell", "merchant", "shop", "goods"]
INTENT_THREAT_WORDS = ["threaten", "kill you", "attack you", "stab you", "hurt you", "rob you"]

TONE_GRATEFUL_WORDS = ["thanks", "thank you", "appreciate", "grateful"]
TONE_POLITE_WORDS = ["please", "kindly", "if you don't mind", "if you wouldnt mind"]
TONE_INSULT_WORDS = ["idiot", "stupid", "hate you", "worthless", "fool", "coward"]
TONE_APOLOGETIC_WORDS = ["sorry", "apologize", "forgive me", "my fault"]

TYPING_AGGRESSIVE_HINTS = ["!", "all caps", "swear"]
TYPING_POLITE_HINTS = ["please", "thank", "sir", "ma'am", "kindly"]
TYPING_CRYPTIC_HINTS = ["...", "cryptic", "vague"]
TYPING_SHORT_THRESHOLD = 4
TYPING_LONG_THRESHOLD = 25

SUSPICION_LIE_INCREMENT = 10
HOSTILITY_LIE_INCREMENT = 5

MAX_HISTORY = 30
MAX_TOPICS = 20

# Emotional drift bounds
DRIFT_MIN = -100
DRIFT_MAX = 100


# ---------------------------------------------------------
# Data structures for AI state
# ---------------------------------------------------------

class NPCDialogueState:
    """
    Per-NPC evolving AI state.
    This is separate from the NPC's core personality and stats.
    """

    def __init__(self):
        self.suspicion: int = 0
        self.emotional_drift: int = 0
        self.last_topics: List[str] = []
        self.lie_memory: Dict[str, bool] = {}
        self.conversation_history: List[Tuple[str, str]] = []  # (player_text, npc_reply)
        self.last_player_style: str = "neutral"
        self.last_intent: str = "talk"
        self.last_tone: str = "neutral"
        self.last_reply: str = ""
        self.times_refused: int = 0
        self.times_lied: int = 0
        self.quest_hint_cooldown: int = 0
        self.lore_hint_cooldown: int = 0
        self.last_quest_hint: Optional[str] = None
        self.last_lore_hint: Optional[str] = None
        self.last_followup_question: Optional[str] = None
        self.player_contradictions: int = 0
        self.player_lie_suspected: bool = False
        self.environment_comment_cooldown: int = 0
        self.companion_comment_cooldown: int = 0
        self.faction_comment_cooldown: int = 0


# ---------------------------------------------------------
# Main AI Dialogue Engine
# ---------------------------------------------------------

class AIDialogueEngine:
    """
    AI Dialogue Engine:
    - Analyzes player text
    - Detects intent and tone
    - Tracks suspicion, emotional drift, and contradictions
    - Generates personality- and role-aware replies
    - Adds lore hints, quest hints, and environmental flavor
    - Asks follow-up questions at a medium frequency
    - Supports high randomness in phrasing
    """

    def __init__(self):
        self.state: Dict[str, NPCDialogueState] = {}

    # -----------------------------------------------------
    # State access
    # -----------------------------------------------------

    def _get_state(self, npc) -> NPCDialogueState:
        if npc.id not in self.state:
            self.state[npc.id] = NPCDialogueState()
        return self.state[npc.id]

    # -----------------------------------------------------
    # Text analysis: intent and tone
    # -----------------------------------------------------

    def analyze_text(self, text: str) -> Tuple[str, str]:
        t = _normalize_text(text)

        intent = "talk"
        tone = "neutral"

        if _contains_any(t, INTENT_HELP_WORDS):
            intent = "help"
        elif _contains_any(t, INTENT_NAME_WORDS):
            intent = "ask_name"
        elif _contains_any(t, INTENT_LOCATION_WORDS):
            intent = "ask_location"
        elif _contains_any(t, INTENT_LORE_WORDS):
            intent = "ask_lore"
        elif _contains_any(t, INTENT_TRADE_WORDS):
            intent = "trade"
        elif _contains_any(t, INTENT_THREAT_WORDS):
            intent = "threaten"

        if _contains_any(t, TONE_GRATEFUL_WORDS):
            tone = "grateful"
        elif _contains_any(t, TONE_POLITE_WORDS):
            tone = "polite"
        elif _contains_any(t, TONE_INSULT_WORDS):
            tone = "insult"
        elif _contains_any(t, TONE_APOLOGETIC_WORDS):
            tone = "apologetic"

        return intent, tone

    # -----------------------------------------------------
    # Typing style analysis
    # -----------------------------------------------------

    def analyze_typing_style(self, text: str) -> str:
        stripped = text.strip()
        lower = stripped.lower()

        if len(stripped) == 0:
            return "silent"

        if len(stripped.split()) <= TYPING_SHORT_THRESHOLD:
            style = "short"
        elif len(stripped.split()) >= TYPING_LONG_THRESHOLD:
            style = "long"
        else:
            style = "neutral"

        if any(c.isupper() for c in stripped) and stripped == stripped.upper() and len(stripped) > 3:
            style = "aggressive"

        if _contains_any(lower, TYPING_POLITE_HINTS):
            style = "polite"

        if "..." in stripped:
            style = "cryptic"

        return style

    # -----------------------------------------------------
    # Emotional drift and suspicion
    # -----------------------------------------------------

    def _update_emotional_drift(self, npc, state: NPCDialogueState, tone: str):
        if tone == "grateful" or tone == "polite":
            state.emotional_drift = _clamp(state.emotional_drift + 2, DRIFT_MIN, DRIFT_MAX)
        elif tone == "insult":
            state.emotional_drift = _clamp(state.emotional_drift - 5, DRIFT_MIN, DRIFT_MAX)
        elif tone == "apologetic":
            state.emotional_drift = _clamp(state.emotional_drift + 1, DRIFT_MIN, DRIFT_MAX)

        if npc.hostility > 50:
            state.emotional_drift = _clamp(state.emotional_drift - 1, DRIFT_MIN, DRIFT_MAX)
        if npc.trust > 50:
            state.emotional_drift = _clamp(state.emotional_drift + 1, DRIFT_MIN, DRIFT_MAX)

    def _update_suspicion_from_contradiction(self, state: NPCDialogueState, text: str):
        normalized = _normalize_text(text)
        if normalized in state.lie_memory:
            state.suspicion = _clamp(state.suspicion + SUSPICION_LIE_INCREMENT, 0, 100)
            state.player_contradictions += 1
            state.player_lie_suspected = True

    # -----------------------------------------------------
    # Lore and quest hint generation
    # -----------------------------------------------------

    def _generate_lore_hint(self, npc, state: NPCDialogueState, world=None, player=None) -> Optional[str]:
        if state.lore_hint_cooldown > 0:
            state.lore_hint_cooldown -= 1
            return None

        if not _chance(0.25):
            return None

        biome = getattr(world.get_room(player.room_id), "biome", None) if (world and player) else None

        hints = [
            "Some say strange lights flicker near the old ruins when the moon is thin.",
            "There are whispers of a beast that hunts only under storm clouds.",
            "They say a forgotten shrine lies buried beneath the roots of the oldest tree in these lands.",
            "Rumor has it that a traveler vanished near the northern ridge, leaving only scorched earth behind.",
            "I've heard that the wind carries voices near the abandoned watchtower.",
        ]

        if biome == "forest":
            hints.append("The forest remembers every footstep. Some paths lead you back to where you started… others don't.")
        elif biome == "desert":
            hints.append("In the desert, mirages aren't always illusions. Sometimes the sand hides things that want to be found.")
        elif biome == "swamp":
            hints.append("The swamp swallows more than just footsteps. People vanish here without a sound.")
        elif biome == "mountain":
            hints.append("Up in the mountains, the air grows thin and the stories grow thick.")
        elif biome == "tundra":
            hints.append("On the tundra, even the silence feels like it's watching you.")

        hint = random.choice(hints)
        state.lore_hint_cooldown = random.randint(3, 7)
        state.last_lore_hint = hint
        return hint

    def _generate_quest_hint(self, npc, state: NPCDialogueState, world=None, player=None) -> Optional[str]:
        if state.quest_hint_cooldown > 0:
            state.quest_hint_cooldown -= 1
            return None

        if not _chance(0.25):
            return None

        hints = [
            "If you're looking for work, the blacksmith in the next settlement always seems short on hands.",
            "I heard someone in the village has been asking around for capable help.",
            "There's talk of a caravan that never arrived. Someone might pay to know why.",
            "If coin is what you seek, keep an ear open near the taverns. Trouble breeds opportunity.",
            "Some folk say the old mine isn't as abandoned as it looks.",
        ]

        if npc.has_quest:
            hints.append("If you're serious about helping, I might have something more concrete for you later.")

        hint = random.choice(hints)
        state.quest_hint_cooldown = random.randint(4, 8)
        state.last_quest_hint = hint
        return hint

    # -----------------------------------------------------
    # Environment, faction, and companion reactions
    # -----------------------------------------------------

    def _environment_flavor(self, npc, state: NPCDialogueState, world=None, player=None) -> Optional[str]:
        if state.environment_comment_cooldown > 0:
            state.environment_comment_cooldown -= 1
            return None

        if not world or not player:
            return None

        room = world.get_room(player.room_id)
        biome = getattr(room, "biome", None)
        weather = getattr(world, "weather", "").lower()

        lines = []

        if biome == "swamp":
            lines.append("This swamp stinks of old secrets and fresh graves.")
        elif biome == "desert":
            lines.append("The desert doesn't forgive mistakes. Or anything else.")
        elif biome == "forest":
            lines.append("The forest listens. Try not to say anything you'll regret.")
        elif biome == "mountain":
            lines.append("Up here, the air is thin and the truth feels closer.")
        elif biome == "tundra":
            lines.append("Cold like this gets into your bones and doesn't leave.")
        elif biome == "plains":
            lines.append("Open ground like this makes some feel free, others exposed.")

        if weather == "storm":
            lines.append("Storm's coming. Words travel strangely in weather like this.")
        elif weather == "heatwave":
            lines.append("The heat makes tempers short and mistakes longer.")
        elif weather == "blizzard":
            lines.append("In a blizzard, even your own thoughts feel far away.")
        elif weather == "mist":
            lines.append("Mist hides more than just the road.")

        if not lines:
            return None

        if not _chance(0.35):
            return None

        state.environment_comment_cooldown = random.randint(3, 6)
        return random.choice(lines)

    def _companion_flavor(self, npc, state: NPCDialogueState, player) -> Optional[str]:
        if state.companion_comment_cooldown > 0:
            state.companion_comment_cooldown -= 1
            return None

        companions = getattr(player, "companions", [])
        if not companions:
            return None

        if not _chance(0.3):
            return None

        comp = random.choice(companions)
        name = getattr(comp, "name", "that creature")
        legendary = getattr(comp, "legendary", False)

        if legendary:
            lines = [
                f"Is that really {name} at your side? I didn't think anyone could walk with such a thing.",
                f"{name}. I've heard stories. I didn't believe them until now.",
                f"Traveling with {name}? Either you're brave, foolish, or both.",
            ]
        else:
            lines = [
                f"Your companion {name} watches everything. I respect that.",
                f"{name} seems loyal. That's rarer than coin out here.",
                f"Not many travel with company like {name}. Says something about you.",
            ]

        state.companion_comment_cooldown = random.randint(4, 8)
        return random.choice(lines)

    def _faction_flavor(self, npc, state: NPCDialogueState, player) -> Optional[str]:
        if state.faction_comment_cooldown > 0:
            state.faction_comment_cooldown -= 1
            return None

        if not npc.faction or not hasattr(player, "reputation"):
            return None

        rep = player.reputation.get(npc.faction, 0)

        if rep > 20:
            lines = [
                "Your name carries some weight with my people.",
                "I've heard your name spoken with respect among my own.",
                "You and my faction have crossed paths before, and not badly.",
            ]
        elif rep < -20:
            lines = [
                "You and my people have history. Not the good kind.",
                "Your reputation with my faction precedes you, and not in a pleasant way.",
                "Some of my kin would draw steel just seeing your face.",
            ]
        else:
            return None

        if not _chance(0.4):
            return None

        state.faction_comment_cooldown = random.randint(5, 9)
        return random.choice(lines)

    # -----------------------------------------------------
    # Follow-up questions (medium frequency)
    # -----------------------------------------------------

    def _followup_question(self, npc, state: NPCDialogueState, text: str) -> Optional[str]:
        if npc.personality == "curious":
            if _chance(0.5):
                return random.choice([
                    "Why does that matter to you?",
                    "What led you down this path?",
                    "Does that ever trouble you when you're alone?",
                    "How long have you carried that thought?",
                ])
        else:
            if _contains_any(text.lower(), ["why", "because", "long ago", "years ago", "ever since"]):
                if _chance(0.3):
                    return random.choice([
                        "And what did that teach you?",
                        "How long have you been living with that?",
                        "Did you choose that, or did it choose you?",
                    ])
        return None

    # -----------------------------------------------------
    # Refusal logic (rare)
    # -----------------------------------------------------

    def _maybe_refuse(self, npc, state: NPCDialogueState, intent: str) -> Optional[str]:
        if npc.trust < -30 or npc.hostility > 70 or state.suspicion > 60:
            if _chance(0.25):
                state.times_refused += 1
                return random.choice([
                    "No. I won't speak on that.",
                    "You've given me no reason to share more.",
                    "Some things are better left unsaid, especially to you.",
                ])
        if intent == "ask_lore" and npc.personality == "serious":
            if _chance(0.15):
                state.times_refused += 1
                return random.choice([
                    "Stories won't help you survive. Focus on what's in front of you.",
                    "Lore won't keep you alive out here.",
                ])
        return None

    # -----------------------------------------------------
    # Lying behavior (hostile/shady NPCs only)
    # -----------------------------------------------------

    def _maybe_lie(self, npc, state: NPCDialogueState, base_reply: str, intent: str) -> str:
        if npc.personality != "hostile" and not npc.is_ambusher:
            return base_reply

        lie_chance = 0.0
        if npc.hostility > 50:
            lie_chance += 0.2
        if state.suspicion > 40:
            lie_chance += 0.1
        if npc.trust < -20:
            lie_chance += 0.1

        if not _chance(lie_chance):
            return base_reply

        state.times_lied += 1
        twisted = [
            "That's what I heard, anyway. Believe it or don't.",
            "Or so they say. Truth's a flexible thing.",
            "That's the version I like to tell, at least.",
        ]
        return base_reply + " " + random.choice(twisted)

    # -----------------------------------------------------
    # Core personality flavor
    # -----------------------------------------------------

    def _personality_flavor(self, npc, state: NPCDialogueState) -> str:
        drift = state.emotional_drift

        if npc.personality == "friendly":
            if drift > 30:
                return random.choice([
                    "You know, you're starting to feel less like a stranger.",
                    "I don't say this lightly, but I trust you more than most.",
                ])
            elif drift < -30:
                return random.choice([
                    "I want to trust you, but something about you keeps me cautious.",
                    "You haven't exactly made this easy to like you.",
                ])
            else:
                return random.choice([
                    "You seem like someone worth giving a chance.",
                    "You carry yourself like someone who's seen things and kept going.",
                ])

        if npc.personality == "hostile":
            if drift > 30:
                return random.choice([
                    "Don't get the wrong idea. I still don't like you, just less than before.",
                    "You've earned a sliver of restraint from me. That's rare.",
                ])
            elif drift < -30:
                return random.choice([
                    "Every word you say makes me like you less.",
                    "You're walking a thin line with me.",
                ])
            else:
                return random.choice([
                    "I don't owe you anything. Remember that.",
                    "Say what you came to say and don't waste my time.",
                ])

        if npc.personality == "curious":
            if drift > 30:
                return random.choice([
                    "You fascinate me more than most who pass through.",
                    "The more you talk, the more I want to know.",
                ])
            elif drift < -30:
                return random.choice([
                    "You used to interest me. Now I'm just wary.",
                    "Curiosity has its limits, and you're testing them.",
                ])
            else:
                return random.choice([
                    "You look like someone with stories buried under your skin.",
                    "I can't quite read you, and that makes you interesting.",
                ])

        if npc.personality == "serious":
            if drift > 30:
                return random.choice([
                    "You've proven you're not just another fool wandering through.",
                    "I don't waste words, and I won't waste them on someone unworthy. You're not.",
                ])
            elif drift < -30:
                return random.choice([
                    "You're making it hard to take you seriously.",
                    "I don't have patience for games, and you're starting to feel like one.",
                ])
            else:
                return random.choice([
                    "Time is a blade. Don't waste it.",
                    "If you have something to say, say it clearly.",
                ])

        return random.choice([
            "These lands shape everyone differently.",
            "You walk like someone who's still deciding who they are.",
            "The world is watching, whether you notice or not.",
        ])

    # -----------------------------------------------------
    # Role flavor
    # -----------------------------------------------------

    def _role_flavor(self, npc, state: NPCDialogueState) -> Optional[str]:
        if npc.is_guardian:
            return random.choice([
                "This place isn't just stone and soil. It's a promise.",
                "I stand here because someone has to.",
                "The shrine remembers those who disrespect it.",
            ])
        if npc.is_emissary:
            return random.choice([
                "Every word spoken in these times can shift the balance.",
                "I listen for more than just what people say.",
                "My people don't have the luxury of careless speech.",
            ])
        if npc.is_storyteller:
            return random.choice([
                "Stories cling to this place like mist.",
                "Truth and myth walk side by side here.",
                "Some tales are warnings. Others are invitations.",
            ])
        if npc.is_ambusher:
            return random.choice([
                "Relax. If I wanted you dead, you'd already be bleeding.",
                "You talk like someone who's never been cornered.",
                "Danger doesn't always announce itself. Sometimes it smiles.",
            ])
        if npc.has_quest:
            return random.choice([
                "There are things that need doing, if you've got the spine for it.",
                "Work finds those who don't run from it.",
                "If you're looking for purpose, this land has plenty to spare.",
            ])
        return None

    # -----------------------------------------------------
    # Main reply generation
    # -----------------------------------------------------

    def generate_reply(self, npc, player, text: str, world=None) -> str:
        state = self._get_state(npc)

        intent, tone = self.analyze_text(text)
        style = self.analyze_typing_style(text)

        state.last_intent = intent
        state.last_tone = tone
        state.last_player_style = style

        self._update_emotional_drift(npc, state, tone)
        self._update_suspicion_from_contradiction(state, text)

        npc_state_topic = _normalize_text(text)
        state.last_topics.append(npc_state_topic)
        if len(state.last_topics) > MAX_TOPICS:
            state.last_topics.pop(0)

        refusal = self._maybe_refuse(npc, state, intent)
        if refusal:
            state.last_reply = refusal
            state.conversation_history.append((text, refusal))
            if len(state.conversation_history) > MAX_HISTORY:
                state.conversation_history.pop(0)
            return refusal

        base_reply = ""

        if intent == "ask_name":
            base_reply = f"My name is {npc.name}. Names carry weight out here, and mine has seen its share of trouble."
        elif intent == "ask_location":
            base_reply = "These lands are old and unforgiving. Every path has a cost, and most people don't read the fine print."
        elif intent == "ask_lore":
            lore_hint = self._generate_lore_hint(npc, state, world, player)
            if lore_hint:
                base_reply = lore_hint
            else:
                base_reply = "There are more stories here than stars in the sky, and most of them end badly."
        elif intent == "help":
            if npc.has_quest:
                base_reply = "If you're truly seeking work, I might have something that needs doing—dangerous, but worth your time."
            else:
                base_reply = "Help is rare in these parts. If you mean it, the world has a way of testing that."
        elif intent == "trade":
            base_reply = "I'm no merchant, but I know a few faces who might lighten your coin purse for something useful."
        elif intent == "threaten":
            npc.adjust_hostility(+20)
            npc.adjust_fear(+10)
            base_reply = "Careful. Empty threats echo badly in these lands, and real ones echo worse."
        else:
            base_reply = self._personality_flavor(npc, state)

        role_line = self._role_flavor(npc, state)
        if role_line:
            base_reply += " " + role_line

        env_line = self._environment_flavor(npc, state, world, player)
        if env_line:
            base_reply += " " + env_line

        faction_line = self._faction_flavor(npc, state, player)
        if faction_line:
            base_reply += " " + faction_line

        comp_line = self._companion_flavor(npc, state, player)
        if comp_line:
            base_reply += " " + comp_line

        quest_hint = self._generate_quest_hint(npc, state, world, player)
        if quest_hint and intent in ["help", "talk"]:
            if _chance(0.5):
                base_reply += " " + quest_hint

        follow = self._followup_question(npc, state, text)
        if follow:
            base_reply += " " + follow
            state.last_followup_question = follow
        else:
            state.last_followup_question = None

        final_reply = self._maybe_lie(npc, state, base_reply, intent)

        state.last_reply = final_reply
        state.conversation_history.append((text, final_reply))
        if len(state.conversation_history) > MAX_HISTORY:
            state.conversation_history.pop(0)

        return final_reply
