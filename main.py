import sys
import pygame
from pygame.locals import *
from pynput import keyboard, mouse
import os
import pkg_resources  # Added: Import pkg_resources

# Set the working directory to the script's path
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Pre-initialize the mixer with a smaller buffer size to reduce latency
pygame.mixer.pre_init(44100, -16, 2, 512)

# Initialize Pygame
pygame.init()

# Get the base directory (location of the script or temporary folder when bundled)
base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Load sound effects
sound_effects = {
    'enter': pygame.mixer.Sound(os.path.join(base_dir, 'sounds/enter.wav')),
    'backspace': pygame.mixer.Sound(os.path.join(base_dir, 'sounds/backspace.wav')),
    'space': pygame.mixer.Sound(os.path.join(base_dir, 'sounds/space.wav')),
    'tab': pygame.mixer.Sound(os.path.join(base_dir, 'sounds/letter3.wav')),
    'general': pygame.mixer.Sound(os.path.join(base_dir, 'sounds/letter1.wav')),
    'click': pygame.mixer.Sound(os.path.join(base_dir, 'sounds/letter2.wav')),

}

key_mapping = {
    keyboard.Key.enter: 'enter',
    keyboard.Key.backspace: 'backspace',
    keyboard.Key.space: 'space',
    keyboard.Key.tab: 'tab',
}

pressed_keys = set()  # Added: Maintain a set of pressed keys


def play_sound(key_name):
    if key_name in sound_effects:
        sound_effects[key_name].play()


def on_press(key):
    if key not in pressed_keys:  # Added: Check if the key is already pressed
        try:
            key_name = key_mapping.get(key, 'general')
            play_sound(key_name)
            # Added: Add the key to the set of pressed keys
            pressed_keys.add(key)
        except AttributeError:
            pass


def on_release(key):
    # Added: Remove the key from the set of pressed keys
    pressed_keys.discard(key)
    if key == keyboard.Key.esc:
        sys.exit()


def on_mouse_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:  # Added: Check if left mouse button is clicked
        play_sound('click')

# Main loop


def main():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as key_listener, \
            mouse.Listener(on_click=on_mouse_click) as mouse_listener:  # Updated: Add mouse listener
        key_listener.join()
        mouse_listener.join()


if __name__ == "__main__":
    main()
