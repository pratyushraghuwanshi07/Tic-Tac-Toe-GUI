import streamlit as st

# Streamlit config
st.set_page_config(page_title="Tic Tac Toe", page_icon="🎮", layout="centered")
st.title("🎮 Tic Tac Toe – Pure Streamlit Edition")
st.caption("Click any cell to place your X or O. First to three in a row wins!")

# Session state for game
if "board" not in st.session_state:
    st.session_state.board = [""] * 9  # 3x3 flat list
if "current_player" not in st.session_state:
    st.session_state.current_player = "X"
if "winner" not in st.session_state:
    st.session_state.winner = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False

def check_winner(board):
    """Check rows, cols, diags for winner or tie."""
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
        [0, 4, 8], [2, 4, 6]               # diags
    ]
    for line in lines:
        if board[line[0]] == board[line[1]] == board[line[2]] != "":
            return board[line[0]]
    if "" not in board:
        return "Tie!"
    return None

def reset_game():
    """Reset board and state."""
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.game_over = False

# Main game logic
if not st.session_state.game_over:
    st.session_state.winner = check_winner(st.session_state.board)

# Display the board (3x3 grid with clickable buttons)
st.markdown("### The Board")
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        if st.button(
            st.session_state.board[i] or f"Click for {st.session_state.current_player}",
            key=f"cell_{i}",
            disabled=st.session_state.game_over or st.session_state.winner is not None
        ):
            if st.session_state.board[i] == "" and not st.session_state.game_over:
                st.session_state.board[i] = st.session_state.current_player
                st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"
                st.session_state.winner = check_winner(st.session_state.board)
                if st.session_state.winner:
                    st.session_state.game_over = True
                st.rerun()  # Refresh to update board

# Show status
if st.session_state.winner:
    if st.session_state.winner == "Tie!":
        st.error("It's a tie! 🎉")
    else:
        st.success(f"{st.session_state.winner} wins! 🏆")
elif not st.session_state.game_over:
    st.info(f"Player {st.session_state.current_player}'s turn")

# Reset button
if st.button("🔄 New Game", use_container_width=True):
    reset_game()
    st.rerun()

# Fun footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit. Share this: [your-app-link]")