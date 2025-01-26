import tkinter as tk
import random

class SnakeLadderGame:
    def __init__(self, root):
        """Initialize the Snake and Ladder game."""
        self.root = root
        self.root.title("Snake and Ladder")
        
        self.board_size = 10
        self.num_cells = self.board_size * self.board_size
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
        
        self.player_positions = [0, 0]  # Starting positions for player 1 and player 2
        self.turn = 0  # Player 1 starts first
        self.dice_roll = 0  # Current dice roll
        self.game_over = False
        
        self.create_widgets()
        self.create_board()

    def create_widgets(self):
        """Create the main game widgets."""
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=10)

        self.turn_label = tk.Label(self.info_frame, 
                                   text="Player 1's turn",
                                     font=("Arial", 14))
        self.turn_label.pack(side=tk.LEFT, 
                             padx=20)

        self.dice_label = tk.Label(self.info_frame,
                                    text="Dice Roll: 0",
                                      font=("Arial", 14))
        self.dice_label.pack(side=tk.LEFT,
                              padx=20)

        self.roll_button = tk.Button(self.root,
                                      text="Roll Dice",
                                        command=self.roll_dice, 
                                        font=("Arial", 12))
        self.roll_button.pack(pady=5)

        self.reset_button = tk.Button(self.root, text="Reset Game",
                                       command=self.reset_game, font=("Arial", 12))
        self.reset_button.pack(pady=5)

        self.message_label = tk.Label(self.root, text="",
                                       font=("Arial", 12),
                                         fg="green")
        self.message_label.pack(pady=10)

    def create_board(self):
        """Create the 10x10 game board."""
        self.canvas = tk.Canvas(self.root, width=600, height=600)
        self.canvas.pack()

        # Draw the grid
        cell_size = 60
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2)
                
                # Number the cells
                cell_number = (self.board_size - row - 1) * self.board_size + col + 1
                self.canvas.create_text(x1 + 30, y1 + 30, text=str(cell_number), font=("Arial", 12))

        # Draw snakes and ladders
        for start, end in self.snakes.items():
            start_x, start_y = self.get_cell_coordinates(start)
            end_x, end_y = self.get_cell_coordinates(end)
            self.canvas.create_line(start_x + 30, start_y + 30, end_x + 30, end_y + 30, arrow=tk.LAST, fill="red", width=2)
            self.canvas.create_text((start_x + end_x) // 2 + 30, (start_y + end_y) // 2 + 30, text="S", font=("Arial", 14, "bold"))

        for start, end in self.ladders.items():
            start_x, start_y = self.get_cell_coordinates(start)
            end_x, end_y = self.get_cell_coordinates(end)
            self.canvas.create_line(start_x + 30, start_y + 30, end_x + 30, end_y + 30, arrow=tk.FIRST, fill="green", width=2)
            self.canvas.create_text((start_x + end_x) // 2 + 30, (start_y + end_y) // 2 + 30, text="L", font=("Arial", 14, "bold"))

        # Draw player pieces
        self.players = [
            self.canvas.create_oval(15, 15, 45, 45, fill="blue"),
            self.canvas.create_oval(15, 15, 45, 45, fill="yellow")
        ]

    def get_cell_coordinates(self, cell):
        """Get the (x, y) coordinates of a given cell."""
        cell_size = 60
        row = (cell - 1) // self.board_size
        col = (cell - 1) % self.board_size
        x = col * cell_size
        y = (self.board_size - row - 1) * cell_size
        return x, y

    def roll_dice(self):
        """Roll the dice and move the current player."""
        if self.game_over:
            return
        self.dice_roll = random.randint(1, 6)
        self.dice_label.config(text=f"Dice Roll: {self.dice_roll}")
        
        # Move the current player
        new_position = self.player_positions[self.turn] + self.dice_roll
        if new_position <= self.num_cells:
            self.player_positions[self.turn] = new_position

        # Check for snakes or ladders
        if self.player_positions[self.turn] in self.snakes:
            self.player_positions[self.turn] = self.snakes[self.player_positions[self.turn]]
            self.message_label.config(text="Oops! You hit a snake.")
        elif self.player_positions[self.turn] in self.ladders:
            self.player_positions[self.turn] = self.ladders[self.player_positions[self.turn]]
            self.message_label.config(text="Yay! You climbed a ladder.")
        else:
            self.message_label.config(text="")

        # Update the position of the player on the board
        self.update_player_position()

        # Check for winner
        if self.player_positions[self.turn] == self.num_cells:
            self.message_label.config(text=f"Player {self.turn + 1} wins!")
            self.game_over = True
            return

        # Switch turns
        self.turn = (self.turn + 1) % 2
        self.turn_label.config(text=f"Player {self.turn + 1}'s turn")

    def update_player_position(self):
        """Update the position of the players on the board."""
        player_oval = self.players[self.turn]
        x, y = self.get_cell_coordinates(self.player_positions[self.turn])
        self.canvas.coords(player_oval, x + 15, y + 15, x + 45, y + 45)

    def reset_game(self):
        """Reset the game to its initial state."""
        self.game_over = False
        self.player_positions = [0, 0]
        self.turn = 0
        self.dice_roll = 0
        self.dice_label.config(text="Dice Roll: 0")
        self.turn_label.config(text="Player 1's turn")
        self.message_label.config(text="")
        
        # Reset player positions
        for player_oval in self.players:
            self.canvas.coords(player_oval, 15, 15, 45, 45)

    def exit_game(self):
        """Exit the game."""
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeLadderGame(root)
    root.mainloop()
