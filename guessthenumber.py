import tkinter as tk
from tkinter import messagebox
import random
import time

class GuessTheNumberGame:
    def __init__(self, root):
        """Initialize the Guess the Number game."""
        self.root = root
        self.root.title("Guess the Number Game")
        
        # Game Variables
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = 10
        self.time_left = 30  # Time limit in seconds
        self.difficulty = "Medium"
        
        # Initialize Highscore Variables
        self.best_time = float('inf')
        self.best_attempts = float('inf')
        
        # Create the main game widgets
        self.create_widgets()
    
    def create_widgets(self):
        """Create all widgets for the game."""
        # Title label
        self.title_label = tk.Label(self.root, text="Guess the Number!", font=("Arial", 24))
        self.title_label.pack(pady=20)
        
        # Instructions
        self.instruction_label = tk.Label(self.root, text="I am thinking of a number between 1 and 100.", font=("Arial", 14))
        self.instruction_label.pack(pady=10)
        
        # Difficulty Level Selection
        self.difficulty_label = tk.Label(self.root, text="Select Difficulty:", font=("Arial", 12))
        self.difficulty_label.pack(pady=5)
        
        self.difficulty_menu = tk.OptionMenu(self.root, *["Easy", "Medium", "Hard"], command=self.change_difficulty)
        self.difficulty_menu.pack(pady=5)
        
        # Input field for the player to guess the number
        self.guess_label = tk.Label(self.root, text="Enter your guess (1-100):", font=("Arial", 12))
        self.guess_label.pack(pady=10)
        
        self.guess_entry = tk.Entry(self.root, font=("Arial", 12), width=10)
        self.guess_entry.pack(pady=5)
        
        # Check guess button
        self.check_button = tk.Button(self.root, text="Check Guess", font=("Arial", 14), command=self.check_guess)
        self.check_button.pack(pady=10)
        
        # Label for the result
        self.result_label = tk.Label(self.root, text="Make a guess to start.", font=("Arial", 14))
        self.result_label.pack(pady=20)
        
        # Label for the number of attempts
        self.attempts_label = tk.Label(self.root, text=f"Attempts: 0/{self.max_attempts}", font=("Arial", 12))
        self.attempts_label.pack(pady=5)
        
        # Timer Label
        self.timer_label = tk.Label(self.root, text=f"Time Left: {self.time_left}s", font=("Arial", 12))
        self.timer_label.pack(pady=5)
        
        # Hint button
        self.hint_button = tk.Button(self.root, text="Get a Hint", font=("Arial", 14), command=self.give_hint)
        self.hint_button.pack(pady=10)
        
        # Reset game button
        self.reset_button = tk.Button(self.root, text="Reset Game", font=("Arial", 14), command=self.reset_game)
        self.reset_button.pack(pady=10)
        
        # Highscore Display
        self.score_label = tk.Label(self.root, text=f"Best Attempts: {self.best_attempts}, Best Time: {self.best_time}s", font=("Arial", 12))
        self.score_label.pack(pady=5)

        # Start the timer
        self.update_timer()

    def change_difficulty(self, difficulty):
        """Change the difficulty of the game."""
        self.difficulty = difficulty
        if difficulty == "Easy":
            self.max_attempts = 15
            self.time_left = 40
        elif difficulty == "Medium":
            self.max_attempts = 10
            self.time_left = 30
        elif difficulty == "Hard":
            self.max_attempts = 7
            self.time_left = 20
        
        # Reset for new difficulty
        self.reset_game()

    def update_timer(self):
        """Update the countdown timer."""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time Left: {self.time_left}s")
            self.root.after(1000, self.update_timer)
        else:
            if self.attempts < self.max_attempts:
                self.result_label.config(text=f"Game Over! Time's up! The number was {self.target_number}.")
                self.check_button.config(state="disabled")
                self.ask_play_again()

    def check_guess(self):
        """Check the player's guess and update the result."""
        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number between 1 and 100.")
            return
        
        if not 1 <= guess <= 100:
            messagebox.showerror("Out of Range", "Your guess must be between 1 and 100.")
            return
        
        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}/{self.max_attempts}")
        
        if guess < self.target_number:
            self.result_label.config(text="Too low! Try again.")
        elif guess > self.target_number:
            self.result_label.config(text="Too high! Try again.")
        else:
            self.result_label.config(text=f"Congratulations! You guessed the number in {self.attempts} attempts.")
            self.check_button.config(state="disabled")
            self.update_highscore()
            self.ask_play_again()

        # Check if the player has exceeded the max attempts
        if self.attempts >= self.max_attempts and guess != self.target_number:
            self.result_label.config(text=f"Game Over! The number was {self.target_number}.")
            self.check_button.config(state="disabled")
            self.ask_play_again()

    def give_hint(self):
        """Provide a hint to the player."""
        if self.attempts == 0:
            messagebox.showinfo("Hint", "You haven't made a guess yet! Try guessing first.")
        else:
            if self.target_number % 2 == 0:
                hint = "The number is even."
            else:
                hint = "The number is odd."
            messagebox.showinfo("Hint", hint)

    def update_highscore(self):
        """Update the highscore (best attempts and time)."""
        if self.attempts < self.best_attempts:
            self.best_attempts = self.attempts
        if self.time_left > 0 and (30 - self.time_left) < self.best_time:
            self.best_time = 30 - self.time_left

        self.score_label.config(text=f"Best Attempts: {self.best_attempts}, Best Time: {self.best_time}s")
    
    def ask_play_again(self):
        """Ask the player if they want to play again."""
        play_again = messagebox.askyesno("Game Over",
                                          f"Would you like to play again?")
        if play_again:
            self.reset_game()

    def reset_game(self):
        """Reset the game for a new round."""
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.time_left = 30
        self.result_label.config(text="Make a guess to start.")
        self.guess_entry.delete(0, tk.END)
        self.check_button.config(state="normal")
        self.attempts_label.config(text=f"Attempts: 0/{self.max_attempts}")
        self.timer_label.config(text=f"Time Left: {self.time_left}s")
        self.update_timer()

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessTheNumberGame(root)
    root.mainloop()
