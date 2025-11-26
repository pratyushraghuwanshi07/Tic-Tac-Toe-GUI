# streamlit_app.py
import streamlit as st
import pygame
import sys
import io

# === CONFIG ===
st.set_page_config(page_title="Tic Tac Toe", layout="centered")
st.title("Tic Tac Toe – Python + Pygame")
st.caption("Click the board to play!")

# Initialize pygame (headless mode)
pygame.init()
SIZE = WIDTH, HEIGHT = 600, 650
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Tic Tac Toe")

# Colors & fonts
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
font = pygame.font.SysFont("Arial", 60)
small_font = pygame.font.SysFont("Arial", 40)

# Game state
board = [[" " for _ in range(3)] for _ in range(3)]
current_player = "X"
winner = None
game_over = False

def draw_board():
    screen.fill(WHITE)
    # Draw grid
    pygame.draw.line(screen, BLACK, (200, 0), (200, 600), 10)
    pygame.draw.line(screen, BLACK, (400, 0), (400, 600),10)
    pygame.draw.line(screen, BLACK, (0, 200), (600, 200),10)
    pygame.draw.line(screen, BLACK, (0, 400), (600, 400),10)
    # Draw X and O
    for r in range(3):
        for c in range(3):
            if board[r][c] == "X":
                pygame.draw.line(screen, RED, (c*200+50, r*200+50), (c*200+150, r*200+150), 15)
                pygame.draw.line(screen, RED, (c*200+150, r*200+50), (c*200+50, r*200+150), 15)
            elif board[r][c] == "O":
                pygame.draw.circle(screen, BLUE, (c*200+100, r*200+100), 80, 15)

def check_winner():
    global winner, game_over
    # rows, cols, diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            winner = board[i][0]; game_over = True
        if board[0][i] == board[1][i] == board[2][i] != " ":
            winner = board[0][i]; game_over = True
    if board[0][0] == board[1][1] == board[2][2] != " ":
        winner = board[0][0]; game_over = True
    if board[0][2] == board[1][1] == board[2][0] != " ":
        winner = board[0][2]; game_over = True
    elif all(board[i][j] != " " for i in range(3) for j in range(3)):
        winner = "Tie"
        game_over = True

def reset_game():
    global board, current_player, winner, game_over
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    winner = None
    game_over = False

# Streamlit pygame loop (magic part)
class PygameStreamlit:
    def __init__(self):
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
    def paint(self):
        draw_board()
        if game_over:
            s = small_font.render(f"{'Tie!' if winner=='Tie' else winner+' wins!'}", True, BLACK)
            screen.blit(s, (100, 610))
            reset_btn = pygame.Rect(200, 550, 200, 60)
            pygame.draw.rect(screen, (0,200,0), reset_btn)
            text = small_font.render("Play Again", True, WHITE)
            screen.blit(text, (210, 560))
            return reset_btn
        return None

# Main loop inside Streamlit
if "pygame_surface" not in st.session_state:
    st.session_state.pygame_surface = PygameStreamlit()

# Show the game
frame = st.session_state.pygame_surface.paint()

# Convert pygame surface → image for Streamlit
buffer = io.BytesIO()
pygame.image.save(screen, buffer, "png")
buffer.seek(0)
st.image(buffer, use_column_width=True)

# Handle clicks
if st.session_state.get("click"):
    x, y = st.session_state.click
    col = x // 200
    row = y // 200
    if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == " " and not game_over:
        board[row][col] = current_player
        check_winner()
        current_player = "O" if current_player == "X" else "X"

# Reset button
if frame and frame.collidepoint(st.session_state.get("click", (0,0))):
    reset_game()

# Click handler (Streamlit → Pygame coordinates)
click = st.experimental_get_query_params().get("click", None)
if click:
    st.session_state.click = tuple(map(int, click[0].split(",")))
else:
    st.session_state.click = None

# Add clickable overlay (invisible)
st.markdown(
    """
    <a href="?click=100,100" style="display:block;width:600px;height:650px;position:absolute;top:0;left:0;"></a>
    """,
    unsafe_allow_html=True
)