import tkinter as tk
from tkinter import messagebox
import random
import time

class RockPaperScissorsGame:
    def __init__(self, root):
        """Initialize the Rock Paper Scissors game."""
        self.root = root
        self.root.title("Rock Paper Scissors")

        self.choices = ["Rock", "Paper", "Scissors"]
        self.player_score = 0
        self.computer_score = 0
        self.rounds = 0
        self.history = []  # To store the history of the rounds
        
        # Create the game interface
        self.create_widgets()
        
    def create_widgets(self):
        """Create the main game widgets."""
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=10)

        # Display for scores
        self.score_label = tk.Label(self.info_frame,
                                     text=self.get_score_text(),
                                       font=("Arial", 14))
        self.score_label.pack(side=tk.LEFT, padx=20)

        # Display for rounds
        self.round_label = tk.Label(self.info_frame,
                                     text="Rounds: 0",
                                       font=("Arial", 14))
        self.round_label.pack(side=tk.LEFT, 
                              padx=20)

        # Display for the result of each round
        self.result_label = tk.Label(self.root, text="Choose an option to start", font=("Arial", 16))
        self.result_label.pack(pady=20)

        # Buttons for choices
        self.rock_button = tk.Button(self.root, text="Rock", command=lambda: self.player_choice("Rock"), width=15, font=("Arial", 14))
        self.rock_button.pack(pady=10)

        self.paper_button = tk.Button(self.root,
                                       text="Paper", 
                                       command=lambda: self.player_choice("Paper"), width=15, font=("Arial", 14))
        self.paper_button.pack(pady=10)

        self.scissors_button = tk.Button(self.root,
                                          text="Scissors", command=lambda: self.player_choice("Scissors"), width=15, font=("Arial", 14))
        self.scissors_button.pack(pady=10)

        # Reset Button
        self.reset_button = tk.Button(self.root, text="Reset Game", command=self.reset_game, width=15, font=("Arial", 14))
        self.reset_button.pack(pady=10)

        # Display for history of the game
        self.history_label = tk.Label(self.root,
                                       text="History: No rounds played yet.", font=("Arial", 12))
        self.history_label.pack(pady=10)

        # Stats Button
        self.stats_button = tk.Button(self.root,
                                       text="View Stats", command=self.show_stats, width=15, font=("Arial", 14))
        self.stats_button.pack(pady=10)

        # Display the animations on button click
        self.button_animation()

    def button_animation(self):
        """Create an animation for the buttons when clicked."""
        self.rock_button.config(relief=tk.RAISED, bg="#f0f0f0")
        self.paper_button.config(relief=tk.RAISED, bg="#f0f0f0")
        self.scissors_button.config(relief=tk.RAISED, bg="#f0f0f0")
        
        def animate_button(button):
            button.config(relief=tk.SUNKEN, bg="#d3d3d3")
            time.sleep(0.2)
            button.config(relief=tk.RAISED, bg="#f0f0f0")
        
        self.rock_button.bind("<ButtonPress-1>", lambda e: animate_button(self.rock_button))
        self.paper_button.bind("<ButtonPress-1>", lambda e: animate_button(self.paper_button))
        self.scissors_button.bind("<ButtonPress-1>", lambda e: animate_button(self.scissors_button))

    def player_choice(self, player_choice):
        """Handle the player's choice."""
        computer_choice = random.choice(self.choices)
        result = self.determine_winner(player_choice, computer_choice)

        self.update_scores(result)
        self.update_display(player_choice, computer_choice, result)
        self.rounds += 1
        self.round_label.config(text=f"Rounds: {self.rounds}")
        
        # Add to the history
        self.history.append(f"Round {self.rounds}: Player chose {player_choice}, Computer chose {computer_choice} - {result}")
        self.update_history()

    def determine_winner(self, player_choice, computer_choice):
        """Determine the winner of the round."""
        if player_choice == computer_choice:
            return "Tie"
        elif (player_choice == "Rock" and computer_choice == "Scissors") or \
             (player_choice == "Paper" and computer_choice == "Rock") or \
             (player_choice == "Scissors" and computer_choice == "Paper"):
            return "Player"
        else:
            return "Computer"

    def update_scores(self, result):
        """Update the score based on the round result."""
        if result == "Player":
            self.player_score += 1
        elif result == "Computer":
            self.computer_score += 1

    def update_display(self,
                        player_choice, computer_choice, result):
        """Update the display with the choices and result of the round."""
        self.result_label.config(text=f"Player chose: {player_choice}\nComputer chose: {computer_choice}\nResult: {result}")
        self.score_label.config(text=self.get_score_text())

        if self.player_score == 10 or self.computer_score == 10:
            self.end_game()

    def get_score_text(self):
        """Return the current score text."""
        return f"Player: {self.player_score}  |  Computer: {self.computer_score}"

    def end_game(self):
        """End the game when either the player or computer reaches 10 points."""
        if self.player_score == 10:
            winner = "Player"
        elif self.computer_score == 10:
            winner = "Computer"
        
        messagebox.showinfo("Game Over",
                             f"{winner} wins the game!\nFinal Score:\nPlayer: {self.player_score}  |  Computer: {self.computer_score}")
        self.reset_game()

    def update_history(self):
        """Update the history display."""
        if len(self.history) > 5:
            self.history = self.history[-5:]
        
        self.history_label.config(text="History:\n" + "\n".join(self.history))

    def show_stats(self):
        """Show the detailed stats in a message box."""
        stats = f"Player Score: {self.player_score}\nComputer Score: {self.computer_score}\nRounds Played: {self.rounds}"
        messagebox.showinfo("Game Stats",
                             stats)

    def reset_game(self):
        """Reset the game for a new round."""
        self.player_score = 0
        self.computer_score = 0
        self.rounds = 0
        self.history.clear()
        self.result_label.config(text="Choose an option to start")
        self.score_label.config(text=self.get_score_text())
        self.round_label.config(text="Rounds: 0")
        self.history_label.config(text="History: No rounds played yet.")

if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()
