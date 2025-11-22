#!/usr/bin/env python3
"""Tic Tac Toe GUI using tkinter.

Usage:
  python3 tic_tac_toe_gui.py

Controls:
  - Use the Mode menu to choose Human vs Human or Human vs Computer.
  - If playing vs computer, choose whether you want to be X or O.
  - Click Restart to start a new game.
"""

import tkinter as tk
from tkinter import messagebox
import math
from typing import List, Optional, Tuple

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


def available_moves(board: List[str]) -> List[int]:
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def check_winner(board: List[str]) -> Optional[str]:
    for a, b, c in WIN_COMBINATIONS:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board: List[str]) -> bool:
    return all(cell != EMPTY for cell in board)


def minimax(board: List[str], maximizing: bool) -> Tuple[int, Optional[int]]:
    """Return (score, move). X is maximizer (score +1), O minimizer (score -1)."""
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
            score, _ = minimax(board, False)
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
            score, _ = minimax(board, True)
            board[move] = EMPTY
            if score < best_score:
                best_score = score
                best_move = move
        return (best_score, best_move)


class TicTacToeGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.mode = "hvh"  # hvh or hvc
        self.human_is_x = True
        self.board: List[str] = [EMPTY] * 9
        self.current = PLAYER_X

        self.status_var = tk.StringVar()
        self.status_var.set("Mode: Human vs Human | X to move")

        # Menu
        menubar = tk.Menu(root)
        mode_menu = tk.Menu(menubar, tearoff=0)
        mode_menu.add_command(label="Human vs Human", command=self.set_hvh)
        mode_menu.add_command(label="Human vs Computer (You = X)", command=lambda: self.set_hvc(True))
        mode_menu.add_command(label="Human vs Computer (You = O)", command=lambda: self.set_hvc(False))
        menubar.add_cascade(label="Mode", menu=mode_menu)
        menubar.add_command(label="Restart", command=self.new_game)
        root.config(menu=menubar)

        # Board buttons
        self.buttons: List[tk.Button] = []
        board_frame = tk.Frame(root)
        board_frame.pack(padx=10, pady=10)

        for i in range(9):
            b = tk.Button(board_frame, text=" ", width=6, height=3, font=(None, 20),
                          command=lambda i=i: self.on_click(i))
            b.grid(row=i // 3, column=i % 3)
            self.buttons.append(b)

        status = tk.Label(root, textvariable=self.status_var)
        status.pack(pady=(0, 10))

        self.new_game()

    def set_hvh(self):
        self.mode = "hvh"
        self.status_var.set("Mode: Human vs Human")
        self.new_game()

    def set_hvc(self, human_is_x: bool):
        self.mode = "hvc"
        self.human_is_x = human_is_x
        side = "X" if human_is_x else "O"
        self.status_var.set(f"Mode: Human vs Computer (You = {side})")
        self.new_game()

    def new_game(self):
        self.board = [EMPTY] * 9
        self.current = PLAYER_X
        for b in self.buttons:
            b.config(text=" ", state=tk.NORMAL)
        self.update_status()
        # If computer is X and should move first
        if self.mode == "hvc" and not self.human_is_x and self.current == PLAYER_X:
            self.root.after(300, self.computer_move)

    def on_click(self, idx: int) -> None:
        if self.board[idx] != EMPTY:
            return
        if self.mode == "hvh":
            self.board[idx] = self.current
            self.buttons[idx].config(text=self.current)
            if self.check_end():
                return
            self.current = PLAYER_O if self.current == PLAYER_X else PLAYER_X
            self.update_status()
        else:
            # Human vs Computer
            human = PLAYER_X if self.human_is_x else PLAYER_O
            computer = PLAYER_O if self.human_is_x else PLAYER_X
            if self.current != human:
                return
            self.board[idx] = human
            self.buttons[idx].config(text=human)
            if self.check_end():
                return
            self.current = computer
            self.update_status()
            self.root.after(200, self.computer_move)

    def computer_move(self) -> None:
        human = PLAYER_X if self.human_is_x else PLAYER_O
        computer = PLAYER_O if self.human_is_x else PLAYER_X
        # If game already finished or not computer's turn, do nothing
        if check_winner(self.board) or is_full(self.board):
            return
        if self.current != computer:
            return

        # For minimax we always treat X as maximizer. If computer is X, maximizing True.
        if computer == PLAYER_X:
            _, move = minimax(self.board, True)
        else:
            # If computer is O, find move that minimizes X's score
            best_move = None
            best_score = math.inf
            for m in available_moves(self.board):
                self.board[m] = PLAYER_O
                score, _ = minimax(self.board, True)
                self.board[m] = EMPTY
                if score < best_score:
                    best_score = score
                    best_move = m
            move = best_move

        if move is None:
            moves = available_moves(self.board)
            move = moves[0]

        self.board[move] = computer
        self.buttons[move].config(text=computer)
        if self.check_end():
            return
        self.current = human
        self.update_status()

    def update_status(self) -> None:
        winner = check_winner(self.board)
        if winner:
            self.status_var.set(f"Player {winner} wins!")
            for b in self.buttons:
                b.config(state=tk.DISABLED)
        elif is_full(self.board):
            self.status_var.set("It's a tie.")
        else:
            self.status_var.set(f"{self.mode_display()} | {self.current}'s turn")

    def mode_display(self) -> str:
        if self.mode == "hvh":
            return "Mode: Human vs Human"
        side = "X" if self.human_is_x else "O"
        return f"Mode: Human vs Computer (You = {side})"

    def check_end(self) -> bool:
        winner = check_winner(self.board)
        if winner:
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            for b in self.buttons:
                b.config(state=tk.DISABLED)
            self.update_status()
            return True
        if is_full(self.board):
            messagebox.showinfo("Game Over", "It's a tie.")
            self.update_status()
            return True
        return False


def main():
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
