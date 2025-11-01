import tkinter as tk
import random

#!/usr/bin/env python3
"""
Simple Snake game using tkinter (no pygame).
Save as snake.py and run: python snake.py
"""

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
INITIAL_SNAKE_LENGTH = 5
INITIAL_SPEED = 120  # milliseconds per move (lower is faster)
SPEED_STEP = -3      # decrease ms per food (makes game faster)
MIN_SPEED = 40


class SnakeGame:
    def __init__(self, root):
        self.root = root
        root.title("Snake")
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
        self.canvas.pack()
        self.score_var = tk.StringVar()
        self.score_var.set("Score: 0")
        self.score_label = tk.Label(root, textvariable=self.score_var)
        self.score_label.pack()

        self.reset_game()
        self.root.bind("<Key>", self.on_key)
        self.running = True
        self.after_id = None
        self.start()

    def reset_game(self):
        self.direction = (1, 0)  # moving right
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.snake = [(center_x - i, center_y) for i in range(INITIAL_SNAKE_LENGTH)]
        self.speed = INITIAL_SPEED
        self.score = 0
        self.place_food()
        self.redraw()

    def start(self):
        self.running = True
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.loop()

    def stop(self):
        self.running = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def loop(self):
        if not self.running:
            return
        self.move_snake()
        self.redraw()
        self.after_id = self.root.after(self.speed, self.loop)

    def place_food(self):
        free_cells = {(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)} - set(self.snake)
        if not free_cells:
            self.food = None
            return
        self.food = random.choice(list(free_cells))

    def move_snake(self):
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check wall collision
        x, y = new_head
        if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
            self.game_over()
            return

        # Check self-collision
        if new_head in self.snake:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # Eat food?
        if self.food and new_head == self.food:
            self.score += 1
            self.score_var.set(f"Score: {self.score}")
            # speed up
            self.speed = max(MIN_SPEED, self.speed + SPEED_STEP)
            self.place_food()
        else:
            self.snake.pop()  # move forward

    def on_key(self, event):
        key = event.keysym.lower()
        dir_map = {
            "up": (0, -1),
            "w": (0, -1),
            "down": (0, 1),
            "s": (0, 1),
            "left": (-1, 0),
            "a": (-1, 0),
            "right": (1, 0),
            "d": (1, 0),
        }
        if key == "r":
            self.reset_game()
            self.start()
            return
        if key == "space":
            if self.running:
                self.stop()
            else:
                self.start()
            return

        if key in dir_map:
            new_dir = dir_map[key]
            # Prevent reversing
            if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
                self.direction = new_dir

    def redraw(self):
        self.canvas.delete("all")
        # draw food
        if self.food:
            self.draw_cell(self.food, fill="red")
        # draw snake
        for i, cell in enumerate(self.snake):
            color = "#00FF00" if i == 0 else "#66FF66"
            self.draw_cell(cell, fill=color, outline="#003300")
        # optional grid lines (comment out if undesired)
        # self.draw_grid()

    def draw_cell(self, pos, fill="white", outline=""):
        x, y = pos
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline)

    def draw_grid(self):
        for i in range(GRID_WIDTH + 1):
            x = i * CELL_SIZE
            self.canvas.create_line(x, 0, x, WINDOW_HEIGHT, fill="#111111")
        for j in range(GRID_HEIGHT + 1):
            y = j * CELL_SIZE
            self.canvas.create_line(0, y, WINDOW_WIDTH, y, fill="#111111")

    def game_over(self):
        self.stop()
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            text=f"GAME OVER\nScore: {self.score}\nPress R to restart",
            fill="white",
            font=("Arial", 24),
            justify=tk.CENTER,
        )

        
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()