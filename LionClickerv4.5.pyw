import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import time
import threading
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import random
import os
import pygame

clicking = False
jitter_enabled = False
sound_enabled = False
cps_randomization_enabled = False
custom_cps = 14
min_cps = 1
max_cps = 20
mouse = Controller()

pygame.init()

click_sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Click.wav")
click_sound = pygame.mixer.Sound(click_sound_path) if os.path.exists(click_sound_path) else None

TOGGLE_KEY = KeyCode(char="p")

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
                cps = random.uniform(min_cps, max_cps)

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

def set_min_cps(new_min_cps):
    global min_cps
    min_cps = new_min_cps
    update_label()

def set_max_cps(new_max_cps):
    global max_cps
    max_cps = new_max_cps
    update_label()

def listener_thread():
    with Listener(on_press=_toggle_event) as listener:
        listener.join()

def update_label():
    label_text.set(f"Jitter: {'OFF' if not jitter_enabled else 'ON'} | Click Sounds: {'OFF' if not sound_enabled else 'ON'} | CPS Randomization: {'OFF' if not cps_randomization_enabled else 'ON'} | Toggle Key: {TOGGLE_KEY.char} | Min CPS: {min_cps} | Max CPS: {max_cps}")

def create_rounded_rectangle_image(width, height, radius, color):
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    draw.rectangle((radius, 0, width - radius, height), fill=color)
    draw.rectangle((0, radius, width, height - radius), fill=color)
    
    draw.pieslice((0, 0, 2 * radius, 2 * radius), 180, 270, fill=color)
    draw.pieslice((width - 2 * radius, 0, width, 2 * radius), 270, 360, fill=color)
    draw.pieslice((0, height - 2 * radius, 2 * radius, height), 90, 180, fill=color)
    draw.pieslice((width - 2 * radius, height - 2 * radius, width, height), 0, 90, fill=color)
    
    return image

class RoundButton(tk.Button):
    def __init__(self, parent, text, command, width=100, height=40, corner_radius=20, bg="red", fg="black", *args, **kwargs):
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.bg = bg
        self.fg = fg

        self.image = ImageTk.PhotoImage(create_rounded_rectangle_image(width, height, corner_radius, bg))
        
        super().__init__(parent, image=self.image, text=text, command=command, compound="center", fg=fg, *args, **kwargs)
        
        self["borderwidth"] = 0
        self["highlightthickness"] = 0
        self["bg"] = parent["bg"]

def main():
    global label_text, custom_cps, min_cps, max_cps
    window = tk.Tk()
    window.title("LionClickerv4.5")
    window.geometry("700x700")
    window.configure(bg="black")

    background_image = Image.open("GUI.png")
    background_photo = ImageTk.PhotoImage(background_image)

    background_label = tk.Label(window, image=background_photo, fg="black", bg="red")
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    label_text = tk.StringVar()
    label_text.set("Jitter: OFF | Click Sounds: OFF | CPS Randomization: OFF | Toggle Key: z | Min CPS: 1 | Max CPS: 20")

    jitter_label = tk.Label(window, textvariable=label_text, fg="red", bg="black")
    jitter_label.pack(pady=100)

    toggle_jitter_button = RoundButton(window, text="Jitter", command=toggle_jitter, bg="red", fg="black")
    toggle_jitter_button.pack(pady=5)

    toggle_sound_button = RoundButton(window, text="Click Sounds", command=toggle_sound, bg="red", fg="black")
    toggle_sound_button.pack(pady=5)

    toggle_cps_randomization_button = RoundButton(window, text="CPS Randomization", command=toggle_cps_randomization, bg="red", fg="black")
    toggle_cps_randomization_button.pack(pady=5)

    toggle_key_label = tk.Label(window, text="Select Toggle Key:", fg="red", bg="black")
    toggle_key_label.pack(pady=5)

    toggle_key_entry = tk.Entry(window, bg="white", fg="black")
    toggle_key_entry.pack(pady=5)

    set_toggle_key_button = RoundButton(window, text="Set Toggle Key", command=lambda: set_toggle_key(KeyCode.from_char(toggle_key_entry.get())), bg="red", fg="black")
    set_toggle_key_button.pack(pady=5)

    min_cps_label = tk.Label(window, text="Set Min CPS:", fg="red", bg="black")
    min_cps_label.pack(pady=5)

    min_cps_slider = tk.Scale(window, from_=1, to=20, orient="horizontal", bg="black", fg="red", troughcolor="white", command=lambda val: set_min_cps(int(val)))
    min_cps_slider.set(min_cps)
    min_cps_slider.pack(pady=5)

    max_cps_label = tk.Label(window, text="Set Max CPS:", fg="red", bg="black")
    max_cps_label.pack(pady=5)

    max_cps_slider = tk.Scale(window, from_=1, to=20, orient="horizontal", bg="black", fg="red", troughcolor="white", command=lambda val: set_max_cps(int(val)))
    max_cps_slider.set(max_cps)
    max_cps_slider.pack(pady=5)

    click_thread = threading.Thread(target=clicker, daemon=True)
    click_thread.start()

    listener_thread_ = threading.Thread(target=listener_thread, daemon=True)
    listener_thread_.start()

    window.mainloop()

if __name__ == "__main__":
    main()
