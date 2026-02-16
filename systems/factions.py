class FactionSystem:
    def __init__(self):
        self.reputation = {}  # faction_name -> value
        self.wars = set()     # (faction_a, faction_b)

    def modify_reputation(self, faction_name, delta):
        self.reputation[faction_name] = self.reputation.get(faction_name, 0) + delta

    def get_reputation(self, faction_name):
        return self.reputation.get(faction_name, 0)

    def set_war(self, faction_a, faction_b):
        key = tuple(sorted([faction_a, faction_b]))
        self.wars.add(key)

    def at_war(self, faction_a, faction_b):
        key = tuple(sorted([faction_a, faction_b]))
        return key in self.wars
