import tkinter as tk
from PIL import Image, ImageTk
import time
import threading
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import random
import os
import pygame
import wmi
import sys
import hashlib
import json

# Made by LionClient. Hi thanks for using my clicker :))) make sure to not rat your fork!


clicking = False
jitter_enabled = False
sound_enabled = False
cps_randomization_enabled = False
custom_cps = 14
mouse = Controller()

pygame.init()

click_sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Click.wav")
click_sound = pygame.mixer.Sound(click_sound_path) if os.path.exists(click_sound_path) else None

TOGGLE_KEY = KeyCode(char="z")  

def play_click_sound():
    if sound_enabled and click_sound:
        pygame.mixer.Sound.play(click_sound)

def clicker():
    while True:
        if clicking:
            mouse.click(Button.left, 1)
            play_click_sound()
            if jitter_enabled:
                add_mouse_jitter()

            cps = custom_cps  
            if cps_randomization_enabled:
                cps = random.uniform(15, 25)  

            delay = 1 / cps
            time.sleep(delay)

def add_mouse_jitter():
    x, y = mouse.position
    x += random.uniform(-2, 5)
    y += random.uniform(-2, 5)
    mouse.position = (x, y)

def _toggle_event(key):
    global clicking, TOGGLE_KEY
    if hasattr(key, 'char') and key.char == TOGGLE_KEY.char:
        clicking = not clicking
        update_label()

def toggle_jitter():
    global jitter_enabled
    jitter_enabled = not jitter_enabled
    update_label()

def toggle_sound():
    global sound_enabled
    sound_enabled = not sound_enabled
    update_label()

def toggle_cps_randomization():
    global cps_randomization_enabled
    cps_randomization_enabled = not cps_randomization_enabled
    update_label()

def set_toggle_key(new_key):
    global TOGGLE_KEY
    TOGGLE_KEY = new_key
    update_label()

def set_cps(new_cps):
    global custom_cps
    custom_cps = new_cps
    update_label()

def listener_thread():
    with Listener(on_press=_toggle_event) as listener:
        listener.join()

def update_label():
    label_text.set(f"Jitter: {'ON' if jitter_enabled else 'OFF'} | Click Sounds: {'ON' if sound_enabled else 'OFF'} | CPS Randomization: {'ON' if cps_randomization_enabled else 'OFF'} | Toggle Key: {TOGGLE_KEY.char} | CPS: {custom_cps}")

def main():
    global label_text
    window = tk.Tk()
    window.title("LionClicker3.0")
    window.geometry("750x750")

    background_image = Image.open("uten navn.png")
    background_photo = ImageTk.PhotoImage(background_image)

    background_label = tk.Label(window, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    label_text = tk.StringVar()
    label_text.set("Jitter: OFF | Click Sounds: OFF | CPS Randomization: OFF | Toggle Key: z | CPS: 14")

    jitter_label = tk.Label(window, textvariable=label_text)
    jitter_label.pack(pady=10)

    toggle_jitter_button = tk.Button(window, text="Jitter", command=toggle_jitter)
    toggle_jitter_button.pack(pady=5)

    toggle_sound_button = tk.Button(window, text="Click Sounds", command=toggle_sound)
    toggle_sound_button.pack(pady=5)

    toggle_cps_randomization_button = tk.Button(window, text="CPS Randomization", command=toggle_cps_randomization)
    toggle_cps_randomization_button.pack(pady=5)

    toggle_key_label = tk.Label(window, text="Select Toggle Key:")
    toggle_key_label.pack(pady=5)

    toggle_key_entry = tk.Entry(window)
    toggle_key_entry.pack(pady=5)

    set_toggle_key_button = tk.Button(window, text="Set Toggle Key", command=lambda: set_toggle_key(KeyCode.from_char(toggle_key_entry.get())))
    set_toggle_key_button.pack(pady=5)

    cps_label = tk.Label(window, text="Set CPS:")
    cps_label.pack(pady=5)

    cps_entry = tk.Entry(window)
    cps_entry.pack(pady=5)

    set_cps_button = tk.Button(window, text="Set CPS", command=lambda: set_cps(float(cps_entry.get())))
    set_cps_button.pack(pady=5)

    click_thread = threading.Thread(target=clicker, daemon=True)
    click_thread.start()

    listener_thread_ = threading.Thread(target=listener_thread, daemon=True)
    listener_thread_.start()

    window.mainloop()

if __name__ == "__main__":
    main()