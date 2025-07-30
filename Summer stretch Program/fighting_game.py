import tkinter as tk
import random

# Initial setup
window = tk.Tk()
window.title("Fighting Game")
window.geometry("400x300")

# Health setup
player1_health = 100
player2_health = 100

# Labels
status_label = tk.Label(window, text="Player 1's Turn", font=("Arial", 14))
status_label.pack()

p1_health_label = tk.Label(window, text=f"Player 1 Health: {player1_health}")
p1_health_label.pack()

p2_health_label = tk.Label(window, text=f"Player 2 Health: {player2_health}")
p2_health_label.pack()

# Game mechanics
turn = 1  # 1 for Player 1, 2 for Player 2

def attack():
    global player1_health, player2_health, turn
    damage = random.randint(10, 20)

    if turn == 1:
        player2_health -= damage
        status_label.config(text=f"Player 1 attacks! -{damage} HP")
        p2_health_label.config(text=f"Player 2 Health: {max(player2_health, 0)}")
        turn = 2
    else:
        player1_health -= damage
        status_label.config(text=f"Player 2 attacks! -{damage} HP")
        p1_health_label.config(text=f"Player 1 Health: {max(player1_health, 0)}")
        turn = 1

    check_winner()

def check_winner():
    if player1_health <= 0:
        status_label.config(text="Player 2 Wins!")
        attack_button.config(state="disabled")
    elif player2_health <= 0:
        status_label.config(text="Player 1 Wins!")
        attack_button.config(state="disabled")

# Button
attack_button = tk.Button(window, text="Attack!", command=attack)
attack_button.pack(pady=20)

# Start the game loop
window.mainloop()
