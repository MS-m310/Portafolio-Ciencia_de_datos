
import random
import datetime
import pyttsx3
import pygame
import sys
import os
import time
import json

# Definir constantes
max_lines = 3
max_bet = 100
min_bet = 1
rows = 3
cols = 3
symbol_count = {"🫀": 3, "🧠": 3, "🫁": 3, "👁️": 3}
symbol_value = {"🫀": 5, "🧠": 4, "🫁": 3, "👁️": 2}

# Inicializar música y voz
pygame.mixer.init()
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# Configuración de datos del usuario
user_data = {}

# Funciones de asistencia de audio y visual
def play_bgm(music_file='background_music.ogg', volume=0.3):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops=-1)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def typewriter(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if char != "\n":
            time.sleep(0.05)
        else:
            time.sleep(0.5)

def get_date():
    return datetime.datetime.now().strftime("%d/%m/%y")

def get_time():
    return datetime.datetime.now().strftime("%H:%M")

# Funciones de inicio de sesión y registro
def load_user_data():
    global user_data
    try:
        with open("user_data.json", "r") as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {}

def save_user_data():
    with open("user_data.json", "w") as file:
        json.dump(user_data, file)

def register_user():
    username = input("Ingrese un nombre de usuario para registrarse: ")
    if username in user_data:
        print("El nombre de usuario ya está registrado.")
        return register_user()
    balance = select_initial_balance()
    user_data[username] = {"balance": balance, "level": "Principiante", "xp": 0, "login_streak": 0}
    save_user_data()
    print(f"Usuario registrado exitosamente: {username}")
    return username

def login_user():
    username = input("Ingrese su nombre de usuario para iniciar sesión: ")
    if username not in user_data:
        print("Usuario no encontrado. Intente registrarse primero.")
        return register_user()
    user_data[username]["login_streak"] += 1
    save_user_data()
    return username

# Selección de balance inicial y métodos de pago
def select_initial_balance():
    balances = [1, 3, 5, 10, 20, 50, 100, 500]
    print("Seleccione su balance inicial:")
    for i, balance in enumerate(balances, start=1):
        print(f"{i}. ${balance}")
    choice = int(input("Seleccione una opción: "))
    return balances[choice - 1] if 1 <= choice <= len(balances) else 1

def add_coins_via_payment():
    methods = ["Tarjeta de Crédito", "ATH Móvil", "PayPal"]
    print("Seleccione un método de pago:")
    for i, method in enumerate(methods, start=1):
        print(f"{i}. {method}")
    choice = int(input("Seleccione una opción de pago: "))
    amount = select_initial_balance()
    return amount if 1 <= choice <= len(methods) else 0

# Funciones del juego
def verify_winnings(columns, lines, bet, values):
    winnings = 0
    winning_line = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_line.append(line + 1)
    return winnings, winning_line

def slot_machine_spin(rows, cols, symbols):
    all_symbols = [symbol for symbol, count in symbols.items() for _ in range(count)]
    columns = []
    for _ in range(cols):
        current_symbols = all_symbols[:]
        column = [random.choice(current_symbols) for _ in range(rows)]
        columns.append(column)
    return columns

def draw_slot_machine(columns):
    for row in range(len(columns[0])):
        print(" | ".join(column[row] for column in columns))
    print()

def deposit():
    while True:
        amount = input("¿Cuánto dinero deseas depositar? $")
        if amount.isdigit() and int(amount) > 0:
            return int(amount)
        print("Por favor, ingrese una cantidad válida.")

def number_of_line():
    while True:
        line = input("Ingrese el número de líneas (1 a 3): ")
        if line.isdigit() and 1 <= int(line) <= max_lines:
            return int(line)
        print("Número de líneas no válido.")

def get_bet():
    while True:
        amount = input("¿Cuánto deseas apostar por línea? $")
        if amount.isdigit() and min_bet <= int(amount) <= max_bet:
            return int(amount)
        print(f"La apuesta debe estar entre ${min_bet} y ${max_bet}.")

def game(balance):
    lines = number_of_line()
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(f"Saldo insuficiente. Saldo actual: ${balance}")
            return 0
        else:
            break
    columns = slot_machine_spin(rows, cols, symbol_count)
    draw_slot_machine(columns)
    winnings, winning_lines = verify_winnings(columns, lines, bet, symbol_value)
    print(f"Ganaste ${winnings}")
    return winnings - total_bet

# Sistema de niveles y recompensas
def update_level(username, balance_change):
    xp_increase = balance_change // 10
    user_data[username]["xp"] += xp_increase
    current_xp = user_data[username]["xp"]
    if current_xp > 100:
        user_data[username]["level"] = "Intermedio"
    elif current_xp > 200:
        user_data[username]["level"] = "Avanzado"
    save_user_data()

def daily_reward(username):
    if user_data[username]["login_streak"] % 7 == 0:
        reward = 50
        user_data[username]["balance"] += reward
        print(f"Has recibido una recompensa de ${reward} por iniciar sesión 7 días consecutivos.")
        save_user_data()

# Funciones principales
def program_opening():
    play_bgm()
    print("\nBienvenido a la tragamonedas virtual.")
    speak("Bienvenido a la tragamonedas virtual.")
    print("¡Buena suerte!")
    speak("Buena suerte.")

def main():
    program_opening()
    load_user_data()
    user = login_user()
    balance = user_data[user]["balance"]
    daily_reward(user)
    while True:
        print(f"\nSaldo actual: ${balance}")
        balance_change = game(balance)
        balance += balance_change
        user_data[user]["balance"] = balance
        save_user_data()
        if balance <= 0:
            print("Saldo insuficiente. Fin del juego.")
            break
        print("¿Deseas jugar de nuevo? (s/n)")
        if input().lower() != 's':
            break
    print(f"Saldo final: ${balance}. ¡Gracias por jugar!")

main()
