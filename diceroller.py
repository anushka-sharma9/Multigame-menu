import random
import tkinter as tk
from tkinter import messagebox

class DiceRollerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Dice Roller Game")
        
        self.player_scores = {}
        self.current_round = 1
        self.total_rounds = 3
        self.current_player_index = 0
        self.players = []

        self.create_setup_screen()

    def create_setup_screen(self):
        """Create the setup screen for the game."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root,
                  text="Welcome to Dice Roller Game!",
                    font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root,
                  text="Enter number of players (2-4):").pack()
        self.num_players_entry = tk.Entry(self.root)
        self.num_players_entry.pack()

        tk.Label(self.root,
                  text="Enter number of rounds (1-5):").pack()
        self.num_rounds_entry = tk.Entry(self.root)
        self.num_rounds_entry.pack()

        tk.Button(self.root,
         text="Start Game",
         command=self.start_game).pack(pady=10)

    def start_game(self):
        """Start the game after validating input."""
        try:
            num_players = int(self.num_players_entry.get())
            self.total_rounds = int(self.num_rounds_entry.get())
            if num_players < 2 or num_players > 4 or self.total_rounds < 1 or self.total_rounds > 5:
               
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for players (2-4) and rounds (1-5).")
            return

        self.players = [f"Player {i+1}" for i in range(num_players)]
        self.player_scores = {player: 0 for player in self.players}
        self.current_round = 1
        self.current_player_index = 0
        self.create_game_screen()

    def create_game_screen(self):
        """Create the main game screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, 
                 text=f"Round {self.current_round} of {self.total_rounds}", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root,
                  text=f"{self.players[self.current_player_index]}'s turn").pack()

        tk.Label(self.root,
                  text="Choose number of dice to roll (1-3):").pack()
        self.num_dice_entry = tk.Entry(self.root)
        self.num_dice_entry.pack()

        tk.Button(self.root,
                   text="Roll Dice", command=self.roll_dice).pack(pady=10)
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.scoreboard_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.scoreboard_label.pack(pady=10)
        self.update_scoreboard()

    def roll_dice(self):
        """Roll dice and update the score for the current player."""
        try:
            num_dice = int(self.num_dice_entry.get())
            if num_dice < 1 or num_dice > 3:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of dice (1-3).")
            return

        rolls = [random.randint(1, 6) for _ in range(num_dice)]
        total = sum(rolls)
        roll_faces = " ".join(self.get_dice_face(value) for value in rolls)
        self.player_scores[self.players[self.current_player_index]] += total

        self.result_label.config(text=f"Rolled: {roll_faces} (Total: {total})")
        self.next_turn()

    def get_dice_face(self, value):
        """Return the dice face for a given value."""
        dice_faces = {
            1: "⚀", 2: "⚁", 3: "⚂",
            4: "⚃", 5: "⚄", 6: "⚅"
        }
        return dice_faces.get(value, str(value))

    def next_turn(self):
        """Advance to the next player's turn or the next round."""
        self.current_player_index += 1
        if self.current_player_index >= len(self.players):
            self.current_player_index = 0
            self.current_round += 1

        if self.current_round > self.total_rounds:
            self.show_final_results()
            
        else:
            self.create_game_screen()

    def update_scoreboard(self):
        """Update the scoreboard display."""
        scoreboard_text = "Scoreboard:\n" + "\n".join(f"{player}: {score}" for player, score in self.player_scores.items())
        self.scoreboard_label.config(text=scoreboard_text)

    def show_final_results(self):
        """Display the final results of the game."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root,
                  text="Game Over!",
                    font=("Arial", 16)).pack(pady=10)

        winner_score = max(self.player_scores.values())
        winners = [player for player, score in self.player_scores.items() if score == winner_score]

        result_text = "\n".join(f"{player}: {score}" for player, score in self.player_scores.items())
        tk.Label(self.root, text=f"Final Scores:\n{result_text}", font=("Arial", 12)).pack(pady=10)

        if len(winners) > 1:
            winner_text = f"It's a tie between {' and '.join(winners)} with {winner_score} points!"
        else:
            winner_text = f"The winner is {winners[0]} with {winner_score} points!"

        tk.Label(self.root,
         text=winner_text, 
        font=("Arial", 14), fg="green").pack(pady=10)
        tk.Button(self.root,
         text="Play Again",
         command=self.create_setup_screen).pack(pady=5)
        tk.Button(self.root,
         text="Quit",
        command=self.root.quit).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    game = DiceRollerGame(root)
    root.mainloop()
