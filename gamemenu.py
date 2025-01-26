import tkinter as tk
from tkinter import messagebox
import os
import subprocess

# Function to run the selected game
def run_game(game_name):
    try:
        # Use subprocess to run the game scripts
        subprocess.run(["python", f"{game_name}.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run {game_name}: {e}")

# Main Menu GUI using Tkinter
class GameMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Menu")

        # Create a frame for the buttons
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        # Create buttons for each game
        games = [
            ("Dice Roller", "diceroller"),
            ("Guess the Number", "guessthenumber"),
            ("Rock Paper Scissors", "rockpaperscissor"),
            ("Snake and Ladder", "snakeandladder"),
            ("Snake Game", "snakegame"),
            ("Tic Tac Toe", "tictactoe")
        ]
        
        for game_name, game_file in games:
            btn = tk.Button(frame, text=game_name, width=20, height=2, 
                            command=lambda g=game_file: run_game(g))
            btn.pack(pady=10)

# Main program entry point
if __name__ == "__main__":
    root = tk.Tk()
    menu = GameMenu(root)
    root.mainloop()
