from dataclasses import dataclass, field
import random


NEMESIS_TITLES = [
    "the Cruel",
    "the Unbroken",
    "the Tracker",
    "the Silent",
    "the Blood‑Marked",
    "the Relentless",
    "the Shadow",
    "the Iron‑Fanged",
    "the Pale",
    "the Storm‑Born",
]


@dataclass
class Nemesis:
    id: str
    name: str
    title: str = field(default_factory=lambda: random.choice(NEMESIS_TITLES))
    level: int = 1
    hatred: int = 0
    last_seen_room: str = ""
    alive: bool = True

    def full_name(self) -> str:
        return f"{self.name} {self.title}"

    def grow(self):
        """Nemesis grows stronger when they escape or survive."""
        self.level += 1
        self.hatred = min(100, self.hatred + random.randint(10, 25))

    def weaken(self):
        """Nemesis weakens if the player defeats them but they survive."""
        self.level = max(1, self.level - 1)
        self.hatred = max(0, self.hatred - random.randint(10, 20))

    def is_enraged(self) -> bool:
        return self.hatred > 60


@dataclass
class NemesisSystem:
    nemesis: Nemesis = None

    def create_nemesis(self, room_id: str):
        """Creates a new nemesis if none exists."""
        if self.nemesis is not None:
            return

        name = random.choice([
            "Vorak", "Syrin", "Karn", "Morgath", "Ravik",
            "Thalor", "Zyra", "Kelran", "Vesh", "Orin"
        ])

        self.nemesis = Nemesis(
            id="nemesis_1",
            name=name,
            last_seen_room=room_id
        )

    def update_location(self, room_id: str):
        """Tracks where the nemesis was last seen."""
        if self.nemesis:
            self.nemesis.last_seen_room = room_id

    def encounter_chance(self, player_room: str) -> bool:
        """Chance of ambush if nemesis is nearby."""
        if not self.nemesis or not self.nemesis.alive:
            return False

        if self.nemesis.last_seen_room != player_room:
            return False

        base = 10 + self.nemesis.level * 5
        if self.nemesis.is_enraged():
            base += 20

        return random.randint(1, 100) <= base

    def nemesis_summary(self) -> str:
        if not self.nemesis:
            return "No nemesis currently stalks you."

        n = self.nemesis
        return (
            f"=== NEMESIS ===\n"
            f"{n.full_name()}\n"
            f"Level: {n.level}\n"
            f"Hatred: {n.hatred}\n"
            f"Last seen: {n.last_seen_room}\n"
            f"Status: {'Alive' if n.alive else 'Defeated'}"
        )
