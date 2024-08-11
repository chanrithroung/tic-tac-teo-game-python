# import tkinter
# # Check the Version of tk 
# a = tkinter.TkVersion

# Tic_tac_toe.py
import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

# Create a class player
class Player(NamedTuple):
    label: str
    color: str


BOARD_SIZE = 3

DEFAULT_PLAYERS = (
    Player(label='X', color='green'),
    Player(label='O', color='blue')
)

# Create a Tic-tac-toe Class
class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_moves()
    
    def _setup_moves(self):
        self.current_moves = [
            [Move(row, col) for col in range(self.board_size) ]
            for row in range(self.board_size)
        ]

        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self.current_moves
        ]

        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    
    def is_valid_move(self, move):
        """Return True is move is valid, and False otherwise."""
        return self.current_moves[move.row][move.col].label == ""

    def process_move(self, move):
        """Process the current move and check if it's a win."""
        self.current_moves[move.row][move.col] = move
        for combo in self._winning_combos:
            results = set(
                self.current_moves[n][m].label
                for n, m in combo
            )
            print(results)

            if (len(results)==1) and ("" not in results):
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner
    

    # Checking for Tied Games

    def is_tied(self):
        """Return True if the game is tied, and false for otherwise."""
        no_winner = not self._has_winner
        player_moves = (
            move.label for row in self.current_moves for move in row
        )

        return no_winner and all(player_moves)
    
    # Toggle player between turns 
    def toggle_player(self):
        """Return a toggle player"""
        self.current_player = next(self._players)


# Create a move class
class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


# Borad Size


class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_board_display()
        self._create_board_grid()
    
    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),           
        )
        self.display.pack()
    
    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(3):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(3):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",       
                )
               
               
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )
    
    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)
    
    def update_display(self, msg, color="#b943a7"):
        self.display['text'] = msg
        self.display['fg'] = color
    
    def play(self, event):
        """Handle a player's move."""
        click_btn = event.widget
        row, col = self._cells[click_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(click_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self.update_display(msg="Tied game!", color="#FF0000")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self.update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self.update_display(msg)


    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="#00FF00")

def main():
    """ Create the game's board and run its main loop."""
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()
if __name__ == '__main__':
    main()
