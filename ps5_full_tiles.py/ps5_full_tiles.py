import tkinter as tk
from tkinter import simpledialog, messagebox
import pygame
import threading
import time
import json
import os

# ===============================
# ITGames представляє
# Повний симулятор PS5 на ПК з плитками та акаунтами
# ===============================

ACCOUNTS_FILE = "accounts.json"

# -------------------------------
# Функції для акаунтів
def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as f:
            return json.load(f)
    return {"users": []}

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

def login_user(username):
    accounts = load_accounts()
    for user in accounts["users"]:
        if user["username"] == username:
            return user
    new_user = {"username": username, "last_game": ""}
    accounts["users"].append(new_user)
    save_accounts(accounts)
    return new_user

# -------------------------------
# Логін користувача
root_login = tk.Tk()
root_login.withdraw()
username = simpledialog.askstring("Логін", "Введіть своє ім'я користувача:")
if not username:
    messagebox.showinfo("Вихід", "Акаунт не введено. Вихід.")
    exit()
current_user = login_user(username)
root_login.destroy()

# -------------------------------
# Ініціалізація геймпада
pygame.init()
pygame.joystick.init()
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Геймпад підключено:", joystick.get_name())

# -------------------------------
# Головне вікно
root = tk.Tk()
root.title(f"ITGames PS5 - {current_user['username']}")
root.geometry("900x600")
root.configure(bg="#111")
root.protocol("WM_DELETE_WINDOW", lambda: messagebox.showinfo("Сигнал загублено","Сигнал втрачено. Перевірте підключення.") or root.destroy())

# -------------------------------
title = tk.Label(root, text="ITGames представляє", font=("Arial", 24), fg="#00ff88", bg="#111")
title.pack(pady=10)
subtitle = tk.Label(root, text=f"Меню PS5 - {current_user['username']}", font=("Arial", 18), fg="white", bg="#111")
subtitle.pack(pady=5)

# -------------------------------
# Ігрові плитки
games = ["Spider-Man", "Ratchet & Clank", "Horizon", "Demon's Souls", "Gran Turismo"]
buttons = []
selected_index = 0

def start_game(name):
    current_user["last_game"] = name
    save_accounts(load_accounts())
    messagebox.showinfo("Запуск гри", f"Гра {name} запущена!")

frame_tiles = tk.Frame(root, bg="#111")
frame_tiles.pack(pady=20)

for g in games:
    btn = tk.Label(frame_tiles, text=g, font=("Arial", 16), bg="#00ff88", fg="#111", width=20, height=3, relief="raised", bd=5)
    btn.pack(side="left", padx=10)
    btn.bind("<Button-1>", lambda e, name=g: start_game(name))
    buttons.append(btn)

def highlight_button(index):
    for i, btn in enumerate(buttons):
        if i == index:
            btn.configure(bg="#00ccff", width=22, height=4)
        else:
            btn.configure(bg="#00ff88", width=20, height=3)

highlight_button(selected_index)

# -------------------------------
# Навігація клавіатурою
def key_pressed(event):
    global selected_index
    if event.keysym == "Left":
        selected_index = (selected_index - 1) % len(buttons)
        highlight_button(selected_index)
    elif event.keysym == "Right":
        selected_index = (selected_index + 1) % len(buttons)
        highlight_button(selected_index)
    elif event.keysym == "Return":
        start_game(games[selected_index])

root.bind("<Left>", key_pressed)
root.bind("<Right>", key_pressed)
root.bind("<Return>", key_pressed)

# -------------------------------
# Кнопка налаштувань
def settings():
    messagebox.showinfo("Налаштування", "Відкрито меню налаштувань.")

btn_settings = tk.Button(root, text="Налаштування", font=("Arial", 16), bg="#00ff88", fg="#111", width=20, command=settings)
btn_settings.pack(pady=20)

# -------------------------------
# Геймпад-цикл
def gamepad_loop():
    global selected_index
    while True:
        if joystick:
            pygame.event.pump()
            hat = joystick.get_hat(0)
            if hat[0] == -1:
                selected_index = (selected_index - 1) % len(buttons)
                highlight_button(selected_index)
                time.sleep(0.2)
            elif hat[0] == 1:
                selected_index = (selected_index + 1) % len(buttons)
                highlight_button(selected_index)
                time.sleep(0.2)
            for i in range(joystick.get_numbuttons()):
                if joystick.get_button(i):
                    start_game(games[selected_index])
                    time.sleep(0.2)
        time.sleep(0.05)

threading.Thread(target=gamepad_loop, daemon=True).start()

# -------------------------------
root.mainloop()
print(" http://127.0.0.1:5000")
