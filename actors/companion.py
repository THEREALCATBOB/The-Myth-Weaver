from dataclasses import dataclass, field
import random


COMPANION_TRAITS = [
    "brave",
    "loyal",
    "cautious",
    "reckless",
    "clever",
    "protective",
    "vengeful",
    "optimistic",
    "quiet",
]


@dataclass
class Companion:
    id: str
    name: str
    trait: str = field(default_factory=lambda: random.choice(COMPANION_TRAITS))
    trust: int = 50  # baseline trust
    loyalty: int = 50  # affects betrayal chance later
    following: bool = True

    # Combat stats (Wave 3 will use these)
    attack: int = 3
    defense: int = 1
    hp: int = 20
    max_hp: int = 20

    def adjust_trust(self, amount: int):
        self.trust = max(0, min(100, self.trust + amount))

    def adjust_loyalty(self, amount: int):
        self.loyalty = max(0, min(100, self.loyalty + amount))

    def is_loyal(self) -> bool:
        return self.loyalty > 40 and self.trust > 40

    def summary(self) -> str:
        return (
            f"{self.name} ({self.trait})\n"
            f"Trust: {self.trust} | Loyalty: {self.loyalty}\n"
            f"HP: {self.hp}/{self.max_hp} | ATK: {self.attack} | DEF: {self.defense}"
        )
