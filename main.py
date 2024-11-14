import tkinter as tk
import random

# Game settings
BALL_SPEED = 5
PADDLE_SPEED = 20
LIVES = 3
WIDTH = 400
HEIGHT = 600

# Initialize the main window
root = tk.Tk()
root.title("Catch the Ball")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

# Canvas for the game
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="lightblue")
canvas.pack()

# Initialize game variables
score = 0
lives = LIVES

# Display score and lives
score_text = canvas.create_text(10, 10, anchor="nw", font=("Arial", 16), text=f"Score: {score}")
lives_text = canvas.create_text(10, 30, anchor="nw", font=("Arial", 16), text=f"Lives: {lives}")

# Paddle setup
paddle = canvas.create_rectangle(0, 0, 80, 10, fill="blue")
canvas.move(paddle, WIDTH // 2 - 40, HEIGHT - 50)

# Ball setup
ball = canvas.create_oval(0, 0, 20, 20, fill="red")
canvas.move(ball, random.randint(20, WIDTH - 20), 0)

# Update score and lives display
def update_score_lives():
    canvas.itemconfig(score_text, text=f"Score: {score}")
    canvas.itemconfig(lives_text, text=f"Lives: {lives}")

# Paddle movement
def move_paddle(event):
    x = 0
    if event.keysym == "Left":
        x = -PADDLE_SPEED
    elif event.keysym == "Right":
        x = PADDLE_SPEED

    # Move paddle within bounds
    paddle_pos = canvas.coords(paddle)
    if paddle_pos[0] + x >= 0 and paddle_pos[2] + x <= WIDTH:
        canvas.move(paddle, x, 0)

# Ball movement
def move_ball():
    global score, lives

    # Move ball downwards
    canvas.move(ball, 0, BALL_SPEED)
    ball_pos = canvas.coords(ball)
    paddle_pos = canvas.coords(paddle)

    # Ball reaches bottom
    if ball_pos[3] >= HEIGHT:
        lives -= 1
        if lives == 0:
            canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Game Over", font=("Arial", 24), fill="red")
            return
        else:
            reset_ball()

    # Ball hits paddle
    if paddle_pos[0] < ball_pos[2] and paddle_pos[2] > ball_pos[0] and paddle_pos[1] < ball_pos[3] and paddle_pos[3] > ball_pos[1]:
        score += 1
        reset_ball()

    # Update score and lives, and schedule next move
    update_score_lives()
    root.after(50, move_ball)

# Reset ball to top with random position
def reset_ball():
    x_position = random.randint(20, WIDTH - 20)
    canvas.coords(ball, x_position, 0, x_position + 20, 20)

# Bind paddle movement to arrow keys
root.bind("<Left>", move_paddle)
root.bind("<Right>", move_paddle)

# Start the game loop
move_ball()
root.mainloop()
