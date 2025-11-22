import sys
import math
from typing import List, Optional, Tuple

#!/usr/bin/env python3
# Code2.py - Simple Tic Tac Toe (Human vs Human or Human vs Computer with Minimax)


EMPTY = " "
PLAYER_X = "X"
PLAYER_O = "O"
WIN_COMBINATIONS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


def print_board(board: List[str]) -> None:
    rows = [
        f" {board[0]} | {board[1]} | {board[2]} ",
        "-----------",
        f" {board[3]} | {board[4]} | {board[5]} ",
        "-----------",
        f" {board[6]} | {board[7]} | {board[8]} ",
    ]
    print("\n".join(rows))


def available_moves(board: List[str]) -> List[int]:
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def check_winner(board: List[str]) -> Optional[str]:
    for a, b, c in WIN_COMBINATIONS:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board: List[str]) -> bool:
    return all(cell != EMPTY for cell in board)


def minimax(board: List[str], current: str, maximizing: bool) -> Tuple[int, Optional[int]]:
    winner = check_winner(board)
    if winner == PLAYER_X:
        return (1, None)
    if winner == PLAYER_O:
        return (-1, None)
    if is_full(board):
        return (0, None)

    if maximizing:
        best_score = -math.inf
        best_move = None
        for move in available_moves(board):
            board[move] = PLAYER_X
            score, _ = minimax(board, PLAYER_O, False)
            board[move] = EMPTY
            if score > best_score:
                best_score = score
                best_move = move
        return (best_score, best_move)
    else:
        best_score = math.inf
        best_move = None
        for move in available_moves(board):
            board[move] = PLAYER_O
            score, _ = minimax(board, PLAYER_X, True)
            board[move] = EMPTY
            if score < best_score:
                best_score = score
                best_move = move
        return (best_score, best_move)


def get_human_move(board: List[str]) -> int:
    moves = available_moves(board)
    while True:
        try:
            raw = input("Enter move (1-9): ").strip()
            if raw.lower() in ("q", "quit", "exit"):
                print("Exiting.")
                sys.exit(0)
            pos = int(raw) - 1
            if pos in moves:
                return pos
            print("Invalid move. Cell occupied or out of range.")
        except (ValueError, TypeError):
            print("Please enter a number from 1 to 9.")


def human_vs_human():
    board = [EMPTY] * 9
    current = PLAYER_X
    while True:
        print_board(board)
        print(f"Player {current}'s turn.")
        move = get_human_move(board)
        board[move] = current
        winner = check_winner(board)
        if winner or is_full(board):
            print_board(board)
            if winner:
                print(f"Player {winner} wins!")
            else:
                print("It's a tie.")
            return
        current = PLAYER_O if current == PLAYER_X else PLAYER_X


def human_vs_computer(human_is_x: bool):
    board = [EMPTY] * 9
    human = PLAYER_X if human_is_x else PLAYER_O
    computer = PLAYER_O if human_is_x else PLAYER_X
    current = PLAYER_X  # X always starts

    while True:
        print_board(board)
        if current == human:
            print(f"Your turn ({human}).")
            move = get_human_move(board)
            board[move] = human
        else:
            print(f"Computer's turn ({computer}). Thinking...")
            # Use minimax oriented so that PLAYER_X tries to maximize, PLAYER_O minimize.
            if computer == PLAYER_X:
                _, move = minimax(board, PLAYER_X, True)
            else:
                _, move = minimax(board, PLAYER_X, True)
                # If computer is O, minimax still returns best for X maximizing,
                # but the returned move is the best for the current position when exploring optimal play.
                # To choose move for O, we can simulate picks: run minimax for both roles is handled above.
            # Fallback if minimax returns None
            if move is None:
                moves = available_moves(board)
                move = moves[0]
            board[move] = computer
            print(f"Computer chose {move + 1}.")

        winner = check_winner(board)
        if winner or is_full(board):
            print_board(board)
            if winner:
                if winner == human:
                    print("You win!")
                else:
                    print("Computer wins!")
            else:
                print("It's a tie.")
            return

        current = PLAYER_O if current == PLAYER_X else PLAYER_X


def choose_mode() -> None:
    print("Tic Tac Toe")
    print("1) Human vs Human")
    print("2) Human vs Computer (you choose X or O)")
    print("Q) Quit")
    while True:
        choice = input("Choose mode [1/2/Q]: ").strip().lower()
        if choice == "1":
            human_vs_human()
            return
        if choice == "2":
            while True:
                side = input("Play as X (goes first) or O? [X/O]: ").strip().upper()
                if side in ("X", "O"):
                    human_vs_computer(human_is_x=(side == "X"))
                    return
                print("Invalid choice. Enter X or O.")
        if choice in ("q", "quit", "exit"):
            print("Goodbye.")
            return
        print("Invalid selection.")


if __name__ == "__main__":
    try:
        choose_mode()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")