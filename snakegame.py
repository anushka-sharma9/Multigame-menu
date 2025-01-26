import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        """Initialize the Snake game."""
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)
        
        # Game Variables
        self.board_size = 20
        self.cell_size = 20
        self.snake = [(5, 5), (4, 5), (3, 5)]  # Initial snake position
        self.food = None
        self.direction = 'Right'
        self.game_over = False
        self.score = 0
        
        # Create canvas
        self.canvas = tk.Canvas(self.root, width=self.board_size * self.cell_size,
                                height=self.board_size * self.cell_size,
                                  bg="black")
        self.canvas.pack()

        # Draw initial snake and food
        self.create_food()
        self.draw_snake()

        # Bind keys for controlling the snake
        self.root.bind("<KeyPress>", self.change_direction)

        # Start the game loop
        self.update_game()

    def create_food(self):
        """Create a new food item at a random location."""
        self.food = (random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1))
        while self.food in self.snake:  # Ensure the food is not on the snake
            self.food = (random.randint(0, self.board_size - 1),
                          random.randint(0, self.board_size - 1))
        self.canvas.create_rectangle(self.food[0] * self.cell_size,
                                      self.food[1] * self.cell_size,
                                     (self.food[0] + 1) * self.cell_size,
                                       (self.food[1] + 1) * self.cell_size,
                                     fill="red",
                                      
                                       outline="black")

    def draw_snake(self):
        """Draw the snake on the canvas."""
        self.canvas.delete("snake")  # Clear the previous snake
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0] * self.cell_size, segment[1] * self.cell_size,
                                         (segment[0] + 1) * self.cell_size,
                                           (segment[1] + 1) * self.cell_size,
                                         fill="green", outline="black",
                                           tags="snake")

    def change_direction(self, event):
        """Change the direction of the snake based on the key press."""
        if event.keysym == 'Left' and self.direction != 'Right':
            self.direction = 'Left'
        elif event.keysym == 'Right' and self.direction != 'Left':
            self.direction = 'Right'
        elif event.keysym == 'Up' and self.direction != 'Down':
            self.direction = 'Up'
        elif event.keysym == 'Down' and self.direction != 'Up':
            self.direction = 'Down'

    def move_snake(self):
        """Move the snake in the current direction."""
        head_x, head_y = self.snake[0]
        if self.direction == 'Left':
            head_x -= 1
        elif self.direction == 'Right':
            head_x += 1
        elif self.direction == 'Up':
            head_y -= 1
        elif self.direction == 'Down':
            head_y += 1

        new_head = (head_x, head_y)

        # Check for collision with the wall or itself
        if (new_head[0] < 0 or new_head[0] >= self.board_size or
            new_head[1] < 0 or new_head[1] >= self.board_size or
            new_head in self.snake):
            self.game_over = True
            return

        # Add the new head to the snake
        self.snake = [new_head] + self.snake[:-1]

        # Check if the snake eats food
        if new_head == self.food:
            self.snake.append(self.snake[-1])  # Add a new segment to the snake
            self.score += 1
            self.create_food()  # Create a new food item
            self.canvas.create_text(self.board_size * self.cell_size / 2, 10,
                                    text=f"Score: {self.score}",
                                      fill="white", font=("Arial", 14))

    def update_game(self):
        """Update the game state and redraw the screen."""
        if self.game_over:
            self.canvas.create_text(self.board_size * self.cell_size / 2, 
                                    self.board_size * self.cell_size / 2,
                                    text="Game Over! Press R to Restart",
                                      fill="white", font=("Arial", 16))
            self.root.bind("<KeyPress-r>", self.restart_game)
            return
        
        # Move the snake and redraw the board
        self.move_snake()
        self.draw_snake()

        # Set the update interval for the game loop (e.g., 100 milliseconds)
        self.root.after(100, self.update_game)

    def restart_game(self, event):
        """Restart the game when the player presses the 'R' key."""
        self.snake = [(5, 5), (4, 5), (3, 5)]  
        # Reset snake position
        self.direction = 'Right'
        self.game_over = False
        self.score = 0
        self.canvas.delete("all")  
        # Clear the canvas
        self.create_food() 
         # Create initial food
        self.draw_snake()  
        # Draw initial snake
        self.update_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
