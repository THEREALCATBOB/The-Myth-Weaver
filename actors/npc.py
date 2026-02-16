import random

class NPC:
    """
    A fully AI-driven NPC with:
    - Unique ID
    - Name
    - Personality
    - Faction (or None)
    - Role flags (patrol, guardian, emissary, legendary, merchant, etc.)
    - Cinematic intro system
    - AI conversation mode
    """

    def __init__(self, npc_id, name, personality, faction=None):
        self.npc_id = npc_id
        self.name = name
        self.personality = personality
        self.faction = faction

        # Location
        self.room_id = None

        # Role flags (default False)
        self.is_patrol = False
        self.is_guardian = False
        self.is_emissary = False
        self.is_legendary = False
        self.is_merchant = False
        self.is_guard = False
        self.is_storyteller = False
        self.is_questgiver = False
        self.is_ambusher = False

        # Conversation state
        self.has_done_intro = False
        self.in_ai_mode = False

        # Memory system (simple but expandable)
        self.memory = []

    # ============================================================
    # CINEMATIC INTRO SYSTEM
    # ============================================================

    def get_intro_lines(self):
        """
        Returns 10 cinematic intro lines based on:
        - Personality
        - Faction
        - Role
        - Hybrid grounded/mystical tone
        """

        base = []

        # Personality flavor
        if self.personality == "serious":
            base = [
                "Their eyes narrow as they study you.",
                "They stand tall, posture rigid and disciplined.",
                "A quiet intensity surrounds them.",
                "They nod once, acknowledging your presence.",
                "Their voice is low and steady.",
            ]
        elif self.personality == "friendly":
            base = [
                "They greet you with a warm smile.",
                "Their posture relaxes as you approach.",
                "They seem genuinely pleased to see you.",
                "A friendly spark lights their eyes.",
                "They wave casually, inviting conversation.",
            ]
        elif self.personality == "curious":
            base = [
                "They tilt their head, studying you with interest.",
                "Their eyes flicker with questions.",
                "They step closer, intrigued.",
                "They seem eager to learn who you are.",
                "Their expression is bright and inquisitive.",
            ]
        else:
            base = [
                "They regard you with a neutral expression.",
                "Their stance is unreadable.",
                "They acknowledge you with a faint nod.",
                "Their eyes reveal little.",
                "They wait silently for you to speak.",
            ]

        # Role flavor
        role_lines = []

        if self.is_patrol:
            role_lines = [
                "Their armor bears the markings of a patrol unit.",
                "They keep glancing at the horizon, alert for threats.",
                "Their stance is disciplined, trained.",
            ]
        elif self.is_guardian:
            role_lines = [
                "A faint aura surrounds them, as if the shrine itself empowers them.",
                "Their presence feels ancient and unwavering.",
            ]
        elif self.is_emissary:
            role_lines = [
                "Their clothing is ceremonial, marked with diplomatic symbols.",
                "They carry themselves with calm authority.",
            ]
        elif self.is_legendary:
            role_lines = [
                "The air shifts subtly around them — something powerful stirs.",
                "Their presence feels larger than life.",
            ]
        elif self.is_merchant:
            role_lines = [
                "Their pack is heavy with goods and trinkets.",
                "They offer a practiced merchant’s smile.",
            ]

        # Faction flavor
        faction_lines = []
        if self.faction:
            faction_lines = [
                f"You notice the insignia of the {self.faction}.",
                f"Their attire carries the colors of the {self.faction}.",
            ]

        # Combine and pick 10 unique lines
        all_lines = base + role_lines + faction_lines

        # Ensure at least 10 lines exist
        while len(all_lines) < 10:
            all_lines.append(random.choice(base))

        random.shuffle(all_lines)
        return all_lines[:10]

    def get_intro(self):
        """Returns one of the 10 intro lines with 10% chance each."""
        lines = self.get_intro_lines()
        return random.choice(lines)

    # ============================================================
    # CONVERSATION LOGIC
    # ============================================================

    def talk(self, player_message):
        """
        Handles conversation flow:
        - First call → cinematic intro
        - After intro → AI conversation mode
        """

        # First interaction → cinematic intro
        if not self.has_done_intro:
            self.has_done_intro = True
            return self.get_intro()

        # After intro → AI mode
        self.in_ai_mode = True

        # Store memory
        if player_message:
            self.memory.append(player_message)

        # Generate AI-style response (placeholder)
        # Your dialogue system will override this with actual AI calls.
        return self.generate_ai_response(player_message)

    # ============================================================
    # AI RESPONSE (placeholder for your dialogue system)
    # ============================================================

    def generate_ai_response(self, player_message):
        """
        This is a placeholder. Your dialogue system replaces this with
        actual AI-generated responses.
        """
        personality_flavor = {
            "serious": "Their tone remains steady and controlled.",
            "friendly": "They speak with warmth and openness.",
            "curious": "They lean in, eager to hear more.",
            "mysterious": "Their voice carries an enigmatic calm.",
            "stoic": "Their expression barely shifts.",
            "pragmatic": "They speak plainly, focused on practicality.",
        }

        flavor = personality_flavor.get(self.personality, "")

        return f"{flavor} They consider your words: '{player_message}'."

    # ============================================================
    # DEBUG / REPRESENTATION
    # ============================================================

    def __repr__(self):
        return f"<NPC {self.npc_id} {self.name} ({self.personality}) faction={self.faction} room={self.room_id}>"
