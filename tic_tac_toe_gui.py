import tkinter as tk
from tkinter import messagebox
import math

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe: Can You Beat the AI?")
        self.root.configure(bg="#1E1E1E")
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()
        self.ai_move()  # AI plays first

    def create_board(self):
        for r in range(3):
            for c in range(3):
                button = tk.Button(self.root, text=" ", font=("Arial", 24, "bold"), width=5, height=2,
                                   bg="#282828", fg="#00FFFF", activebackground="#005f5f",
                                   command=lambda r=r, c=c: self.player_move(r, c))
                button.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[r][c] = button
        self.status_label = tk.Label(self.root, text="AI's turn (O)", font=("Arial", 16), bg="#1E1E1E", fg="#00FF00")
        self.status_label.grid(row=3, column=0, columnspan=3)

    def update_status(self, message):
        self.status_label.config(text=message)

    def player_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = 'X'
            self.buttons[row][col].config(text='X', state="disabled", disabledforeground="#FFFFFF")
            if self.check_winner('X'):
                self.update_status("Congratulations! You win!")
                self.show_winner("X")
            elif not self.empty_squares():
                self.update_status("It's a draw!")
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.update_status("AI's turn (O)")
                self.root.after(500, self.ai_move)

    def ai_move(self):
        if not self.empty_squares():
            return
        move = self.get_best_move()
        if move:
            row, col = move
            self.board[row][col] = 'O'
            self.buttons[row][col].config(text='O', state="disabled", disabledforeground="#FFA500")
            if self.check_winner('O'):
                self.update_status("AI wins!")
                self.show_winner("O")
            elif not self.empty_squares():
                self.update_status("It's a draw!")
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.update_status("Your turn! (X)")

    def show_winner(self, winner):
        messagebox.showinfo("Game Over", f"{winner} wins!")
        self.reset_game()

    def reset_game(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=" ", state="normal")
        self.update_status("AI's turn (O)")
        self.root.after(500, self.ai_move)  # AI plays first again

    def empty_squares(self):
        return any(self.board[r][c] == ' ' for r in range(3) for c in range(3))

    def check_winner(self, player):
        board = self.board
        for row in board:
            if all([spot == player for spot in row]):
                return True
        for col in range(3):
            if all([board[row][col] == player for row in range(3)]):
                return True
        if board[0][0] == board[1][1] == board[2][2] == player:
            return True
        if board[0][2] == board[1][1] == board[2][0] == player:
            return True
        return False

    def minimax(self, is_maximizing):
        if self.check_winner('O'):
            return 10  # AI wins
        elif self.check_winner('X'):
            return -10  # Player wins
        elif not self.empty_squares():
            return 0  # Draw

        if is_maximizing:
            best_score = -math.inf
            for (r, c) in self.available_moves():
                self.board[r][c] = 'O'
                score = self.minimax(False)
                self.board[r][c] = ' '
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = math.inf
            for (r, c) in self.available_moves():
                self.board[r][c] = 'X'
                score = self.minimax(True)
                self.board[r][c] = ' '
                best_score = min(best_score, score)
            return best_score

    def get_best_move(self):
        best_score = -math.inf
        best_move = None
        for (r, c) in self.available_moves():
            self.board[r][c] = 'O'
            score = self.minimax(False)
            self.board[r][c] = ' '
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move

    def available_moves(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ' ']

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()


