import os
import sys
import time
import shutil

# ---------------------------------------------------------
# CORE TYPEWRITER EFFECT
# ---------------------------------------------------------
def type_text(text, speed=0.02):
    """
    Cinematic typewriter effect.
    speed = delay per character.
    """
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(speed)
    print()


# ---------------------------------------------------------
# DRAMATIC LINE (slower, heavier)
# ---------------------------------------------------------
def dramatic(text):
    type_text(text, speed=0.04)
    time.sleep(0.4)


# ---------------------------------------------------------
# INSTANT PRINT (for debugging or fast UI)
# ---------------------------------------------------------
def instant(text):
    print(text)


# ---------------------------------------------------------
# CLEAR SCREEN
# ---------------------------------------------------------
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# ---------------------------------------------------------
# CINEMATIC BANNER
# ---------------------------------------------------------
def banner(text):
    clear_screen()
    width = shutil.get_terminal_size().columns
    line = "=" * width
    print(line)
    centered = text.center(width)
    print(centered)
    print(line)
    time.sleep(0.5)


# ---------------------------------------------------------
# PARAGRAPH REVEAL
# ---------------------------------------------------------
def reveal(text, speed=0.02):
    """
    Prints a paragraph line by line with a small pause.
    """
    for line in text.split("\n"):
        type_text(line, speed)
        time.sleep(0.2)


# ---------------------------------------------------------
# CINEMATIC PAUSE
# ---------------------------------------------------------
def pause(seconds=0.5):
    time.sleep(seconds)

