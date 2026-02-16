import random
from ui.text_randomizer import rt


# ---------------------------------------------------------
# INTERNAL: MOVE ENTITY BETWEEN ROOMS
# ---------------------------------------------------------

def _move_entity_between_rooms(world, entity):
    if not hasattr(entity, "room_id"):
        return

    room = world.get_room(entity.room_id)
    exits = list(room.exits.values())
    if not exits:
        return

    new_room_id = random.choice(exits)
    new_room = world.get_room(new_room_id)

    # Remove from old room
    if entity in room.npcs:
        room.npcs.remove(entity)

    # Add to new room
    entity.room_id = new_room_id
    new_room.npcs.append(entity)


# ---------------------------------------------------------
# WANDERING ENTITIES
# ---------------------------------------------------------

def move_wandering_entities(world):
    # Wandering NPCs
    for npc in getattr(world, "wandering_npcs", []):
        _move_entity_between_rooms(world, npc)

    # Traveling merchants
    for merchant in getattr(world, "traveling_merchants", []):
        _move_entity_between_rooms(world, merchant)

    # Faction patrols (move as a group)
    for patrol in getattr(world, "faction_patrols", []):
        if not patrol:
            continue

        leader = patrol[0]
        room = world.get_room(leader.room_id)
        exits = list(room.exits.values())
        if not exits:
            continue

        new_room_id = random.choice(exits)
        new_room = world.get_room(new_room_id)

        for npc in patrol:
            if npc in room.npcs:
                room.npcs.remove(npc)
            npc.room_id = new_room_id
            new_room.npcs.append(npc)


# ---------------------------------------------------------
# HERD BEHAVIOR
# ---------------------------------------------------------

def herd_behavior(world):
    """
    Animals in the same room move together as a herd.
    """
    for room in world.rooms.values():
        if len(room.animals) < 2:
            continue

        exits = list(room.exits.values())
        if not exits:
            continue

        new_room_id = random.choice(exits)
        new_room = world.get_room(new_room_id)

        for a in list(room.animals):
            room.animals.remove(a)
            a.room_id = new_room_id
            new_room.animals.append(a)


# ---------------------------------------------------------
# PREDATOR HUNTING
# ---------------------------------------------------------

def predator_hunting(world):
    """
    Predators move toward adjacent rooms that contain prey.
    """
    for room in world.rooms.values():
        predators = [a for a in room.animals if a.hostile]
        if not predators:
            continue

        for predator in list(predators):
            # Already with prey?
            if any(not a.hostile for a in room.animals if a is not predator):
                continue

            # Search adjacent rooms for prey
            for exit_id in room.exits.values():
                next_room = world.get_room(exit_id)
                if any(not a.hostile for a in next_room.animals):
                    room.animals.remove(predator)
                    predator.room_id = exit_id
                    next_room.animals.append(predator)
                    break


# ---------------------------------------------------------
# RANDOM WORLD EVENTS (CINEMATIC)
# ---------------------------------------------------------

def random_world_event(world, player):
    """
    Small flavor/gameplay events based on room tags.
    Returns a cinematic text line or None.
    """
    room = world.get_room(player.room_id)
    roll = random.random()

    # Campfire ambience
    if roll < 0.05 and "campfire" in room.tags:
        return rt("event_campfire")

    # Shrine omen
    if roll < 0.03 and "shrine" in room.tags:
        return rt("event_shrine")

    # Treasure glint
    if roll < 0.02 and "treasure" in room.tags:
        return rt("event_treasure")

    # Miniboss pressure
    if roll < 0.01 and "miniboss" in room.tags:
        return rt("event_miniboss")

    # Global rare anomalies (1% chance anywhere)
    if roll < 0.01:
        return rt("event_anomaly")

    # Rare omens (2% chance anywhere)
    if roll < 0.02:
        return rt("event_omen")

    return None
