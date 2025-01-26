import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        """Initialize the Tic Tac Toe game."""
        self.root = root
        self.root.title("Tic Tac Toe")
        
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.scores = {"X": 0,
        "O": 0,
        "Ties": 0}
        self.colors = {"X": "blue", 
        "O": "green", 
        "Ties": "gray"}
        
        self.create_widgets()
        self.create_board()

    def create_widgets(self):
        """Create additional widgets for the game."""
        # Frame for info and scores
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=10)

        # Score display
        self.score_label = tk.Label(self.info_frame, 
        text=self.get_score_text(),
        font=("Arial", 14))
        self.score_label.pack(side=tk.LEFT, padx=20)

        # Turn display
        self.turn_label = tk.Label(self.info_frame,
         text=f"Player {self.current_player}'s turn", font=("Arial", 14))
        self.turn_label.pack(side=tk.RIGHT, padx=20)

        # Reset and Exit buttons
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=5)

        self.reset_button = tk.Button(self.control_frame,
         text="Reset Scores", command=self.reset_scores, font=("Arial", 12))
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = tk.Button(self.control_frame,
        text="Exit Game", command=self.exit_game, font=("Arial", 12))
        self.exit_button.pack(side=tk.RIGHT, padx=10)

    def create_board(self):
        """Create the 3x3 game board."""
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Arial", 24),
                    width=5,
                    height=2,
                    command=lambda r=row, c=col: self.make_move(r, c),
                    bg="white"
                )
                btn.grid(row=row, column=col)
                self.buttons[row][col] = btn

    def make_move(self, row, col):
        """Handle a player's move."""
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, 
            fg=self.colors[self.current_player])
            
            if self.check_winner(row, col):
                self.highlight_winner(row, col)
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.scores[self.current_player] += 1
                self.reset_board()
            elif self.is_tie():
                self.highlight_tie()
                messagebox.showinfo("Game Over", "It's a tie!")
                self.scores["Ties"] += 1
                self.reset_board()
            else:
                self.switch_player()
        else:
            messagebox.showwarning("Invalid Move", "That spot is already taken!")

    def check_winner(self, row, col):
        """Check if the current player has won."""
        # Check row
        if all(self.board[row][c] == self.current_player for c in range(3)):
            self.winning_combo = [(row, c) for c in range(3)]
            return True
        # Check column
        if all(self.board[r][col] == self.current_player for r in range(3)):
            self.winning_combo = [(r, col) for r in range(3)]
            return True
        # Check diagonals
        if row == col and all(self.board[i][i] == self.current_player for i in range(3)):
            self.winning_combo = [(i, i) for i in range(3)]
            return True
        if row + col == 2 and all(self.board[i][2 - i] == self.current_player for i in range(3)):
            self.winning_combo = [(i, 2 - i) for i in range(3)]
            return True
        return False

    def highlight_winner(self, row, col):
        """Highlight the winning combination."""
        for r, c in self.winning_combo:
            self.buttons[r][c].config(bg="lightgreen")

    def is_tie(self):
        """Check if the game is a tie."""
        return all(self.board[row][col] != "" for row in range(3) for col in range(3))

    def highlight_tie(self):
        """Highlight the board in case of a tie."""
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(bg="lightgray")

    def switch_player(self):
        """Switch the current player."""
        self.current_player = "O" if self.current_player == "X" else "X"
        self.turn_label.config(text=f"Player {self.current_player}'s turn")

    def reset_board(self):
        """Reset the board for a new game."""
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", bg="white")
        self.current_player = "X"
        self.turn_label.config(text=f"Player {self.current_player}'s turn")
        self.update_score_label()

    def reset_scores(self):
        """Reset the scores and the board."""
        self.scores = {"X": 0, "O": 0, "Ties": 0}
        self.reset_board()
        self.update_score_label()
        messagebox.showinfo("Scores Reset", "All scores have been reset!")

    def update_score_label(self):
        """Update the score display."""
        self.score_label.config(text=self.get_score_text())

    def get_score_text(self):
        """Return the current score text."""
        return f"X: {self.scores['X']}  |  O: {self.scores['O']}  |  Ties: {self.scores['Ties']}"

    def exit_game(self):
        """Exit the game."""
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
