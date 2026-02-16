from ui.text_effects import type_text, dramatic, banner, reveal, clear_screen, pause
from ui.text_randomizer import rt, TEXT_VARIANTS
from core.world import World
from core.player import Player
from systems.survival import apply_biome_effects, update_survival
from systems.encounters import auto_encounter
from systems.world_events import (
    move_wandering_entities,
    herd_behavior,
    predator_hunting,
    random_world_event,
)
from systems.combat import start_combat
from systems.dialogue import talk_to_npc  # NEW: high-level NPC talk entry
import random


# ---------------------------------------------------------
# ROOM DESCRIPTION
# ---------------------------------------------------------
def describe_room(world, player):
    room = world.get_room(player.room_id)

    # Weather flavor
    weather_key = f"weather_{world.weather.lower()}"
    if weather_key in TEXT_VARIANTS:
        dramatic(rt(weather_key))

    # Cinematic room title
    dramatic(rt("room_title", name=room.name))

    # Handcrafted biome description
    reveal(room.description)

    # Biome‑specific flavor
    biome_key = f"biome_{room.biome}"
    if biome_key in TEXT_VARIANTS:
        dramatic(rt(biome_key))

    # Room metadata (kept as clear UI text)
    type_text(f"Biome: {room.biome}")

    if room.resources:
        type_text(f"Resources: {', '.join(room.resources)}")

    if room.hazards:
        type_text(f"Hazards: {', '.join(room.hazards)}")

    if room.animals:
        names = {a.name for a in room.animals}
        type_text(f"Animals: {', '.join(names)}")

    if room.npcs:
        names = {n.name for n in room.npcs}
        type_text(f"NPCs: {', '.join(names)}")

    # Special tags -> cinematic event text
    if "campfire" in room.tags:
        dramatic(rt("event_campfire"))
    if "shrine" in room.tags:
        dramatic(rt("event_shrine"))
    if "treasure" in room.tags:
        dramatic(rt("event_treasure"))
    if "miniboss" in room.tags:
        dramatic(rt("event_miniboss"))
    if "den" in room.tags:
        dramatic(rt("event_ruins"))

    # Compact summary
    tags = []
    if "campfire" in room.tags:
        tags.append("Campfire")
    if "shrine" in room.tags:
        tags.append("Shrine")
    if "treasure" in room.tags:
        tags.append("Treasure")
    if "miniboss" in room.tags:
        tags.append("Mini-boss Lair")
    if "den" in room.tags:
        tags.append("Animal Den")

    if tags:
        type_text(f"Special: {', '.join(tags)}")

    # NPC ambient reactions to biome/weather
    if room.npcs:
        for npc in room.npcs:
            if world.weather == "storm" and hasattr(npc, "adjust_fear"):
                npc.adjust_fear(+2)
            if room.biome == "corrupted_lands" and hasattr(npc, "adjust_fear"):
                npc.adjust_fear(+3)


# ---------------------------------------------------------
# ANIMAL HELPERS
# ---------------------------------------------------------
def find_animal_in_room(world, player, name):
    room = world.get_room(player.room_id)
    for a in room.animals:
        if a.name.lower() == name.lower():
            return a
    return None


def feed_animal(player, world, name):
    animal = find_animal_in_room(world, player, name)
    if not animal:
        return rt("error_generic")
    player.record_action("feed")
    return rt("feed_react", animal=animal.name)


def tame_animal(player, world, name):
    animal = find_animal_in_room(world, player, name)
    if not animal:
        return rt("error_generic")

    if not getattr(animal, "tamed", False):
        return rt("tame_fail", animal=animal.name)

    if animal not in player.companions:
        player.companions.append(animal)

    player.record_action("tame")
    return rt("tame_success", animal=animal.name)


def mount_animal(player, world, name):
    animal = find_animal_in_room(world, player, name)
    if not animal:
        return rt("error_generic")

    msg = animal.attempt_mount()
    if "mount" in msg.lower():
        player.mount = animal
        player.record_action("mount")

    return msg


# ---------------------------------------------------------
# FOLLOWER MOVEMENT
# ---------------------------------------------------------
def move_followers(world, player, old_room_id, new_room_id):
    old_room = world.get_room(old_room_id)
    new_room = world.get_room(new_room_id)

    moving = []
    for npc in list(old_room.npcs):
        if getattr(npc, "following_player", False):
            moving.append(npc)

    for npc in moving:
        old_room.npcs.remove(npc)
        npc.room_id = new_room_id
        new_room.npcs.append(npc)
        dramatic(f"{npc.name} follows you.")


# ---------------------------------------------------------
# MOVEMENT + WORLD TICK
# ---------------------------------------------------------
def handle_move(direction, world, player):
    room = world.get_room(player.room_id)

    if direction not in room.exits:
        dramatic(rt("warning"))
        return

    old_room_id = player.room_id
    player.room_id = room.exits[direction]
    world.advance_time(1)

    # Mounted bonus
    if player.mount:
        world.advance_time(-0.5)
        player.fatigue = max(0, player.fatigue - 1)

    new_room = world.get_room(player.room_id)

    # Move followers with player
    move_followers(world, player, old_room_id, player.room_id)

    biome_msg = apply_biome_effects(player, world, new_room)
    status, warning = update_survival(player, world)

    # --- WORLD SIMULATION TICK ---
    move_wandering_entities(world)
    herd_behavior(world)
    predator_hunting(world)
    event_msg = random_world_event(world, player)

    clear_screen()

    dramatic(rt("enter_room", name=new_room.name))
    describe_room(world, player)

    if biome_msg:
        dramatic(rt("biome_effect", biome=new_room.biome))

    if warning:
        dramatic(rt("warning"))

    if event_msg:
        dramatic(event_msg)

    # Auto encounter
    result = auto_encounter(player, world)
    if isinstance(result, str):
        dramatic(result)


# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
def main():
    clear_screen()
    dramatic(rt("start_message"))
    pause(0.5)
    banner("Text RPG")

    name = input("Enter your name: ").strip() or "Wanderer"
    world = World(size=10)
    world.generate()
    world.populate_world()

    player = Player(name, world.start_room_id)
    player.mount = None

    clear_screen()
    describe_room(world, player)

    while True:
        type_text(
            "\nCommands: n/s/e/w, look, map, talk, quests, feed <animal>, tame <animal>, mount <animal>, rest, quit"
        )
        cmd = input("> ").strip().lower()

        # Movement
        if cmd in ["n", "north"]:
            handle_move("north", world, player)
        elif cmd in ["s", "south"]:
            handle_move("south", world, player)
        elif cmd in ["e", "east"]:
            handle_move("east", world, player)
        elif cmd in ["w", "west"]:
            handle_move("west", world, player)

        # Look
        elif cmd == "look":
            describe_room(world, player)

        # Map
        elif cmd == "map":
            type_text("\nMinimap:")
            for line in world.ascii_minimap(player.room_id).split("\n"):
                type_text(line, 0.001)

        # Quest log
        elif cmd == "quests":
            from systems.quests import check_quest_completion
            check_quest_completion(player, world)
            log = player.quest_log()
            type_text("\nQuests:")
            for line in log.split("\n"):
                type_text(line)

        # TALK TO NPCs
        elif cmd == "talk":
            room = world.get_room(player.room_id)

            if not room.npcs:
                dramatic("There is no one here to talk to.")
                continue

            # Choose NPC if multiple
            if len(room.npcs) > 1:
                type_text("Who do you want to talk to?")
                for i, npc in enumerate(room.npcs, 1):
                    type_text(f"{i}. {npc.name}")
                choice = input("> ").strip()
                if not choice.isdigit() or not (1 <= int(choice) <= len(room.npcs)):
                    dramatic("You hesitate and say nothing.")
                    continue
                npc = room.npcs[int(choice) - 1]
            else:
                npc = room.npcs[0]

            # Cinematic first impression / description
            dramatic(npc.describe())
            dramatic(npc.greet())  # uses NPC's personality + role greetings

            # Hostility-triggered combat
            if npc.is_openly_hostile():
                from actors.enemy import Enemy
                dramatic(f"{npc.name} snarls and reaches for a weapon.")
                enemy = Enemy(
                    id=f"{npc.id}_hostile",
                    name=npc.name,
                    tier=2,
                    biome=world.get_room(player.room_id).biome,
                    behavior="aggressive",
                    weaknesses=["cold"],
                    abilities=["strike", "heavy_strike"],
                )
                start_combat(player, enemy, world)
                continue

            # High-level dialogue: structured intro → AI free-text
            talk_to_npc(npc, player, world)

            # Quest turn-in
            from systems.quests import turn_in_quest
            quest = turn_in_quest(player, npc)
            if quest:
                dramatic(rt("quest_turned_in", quest=quest.description))
                msgs = player.gain_xp(0)
                for m in msgs:
                    dramatic(m)

        # Animal commands
        elif cmd.startswith("feed "):
            target = cmd.replace("feed ", "").strip()
            dramatic(feed_animal(player, world, target))

        elif cmd.startswith("tame "):
            target = cmd.replace("tame ", "").strip()
            dramatic(tame_animal(player, world, target))

        elif cmd.startswith("mount "):
            target = cmd.replace("mount ", "").strip()
            dramatic(mount_animal(player, world, target))

        # Rest
        elif cmd == "rest":
            dramatic(rt("rest"))
            pause(1.0)
            player.fatigue = max(0, player.fatigue - 20)
            player.hp = min(player.max_hp, player.hp + 10)
            world.advance_time(6)
            type_text(rt("rest_recover"))

        # Quit
        elif cmd == "quit":
            dramatic(rt("quit"))
            break

        # Unknown command
        else:
            dramatic(rt("warning"))


if __name__ == "__main__":
    main()
