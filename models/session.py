from models.exces import *
from models.boat import Boat
from models.board import Board
from models.player import Player


class GameSession:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.player1.other_board = player2.my_board
        self.player2.other_board = player1.my_board
        self.winner: Player | None = None
        self.to_move: Player = self.player1

    def check_game_over(self) -> bool:
        if self.player1.alive_boat_count == 0:
            self.winner = self.player2
            return True

        if self.player2.alive_boat_count == 0:
            self.winner = self.player1
            return True

        return False

    def move(self, i, j):
        if (i, j) in self.to_move.hit_history:
            return

        self.to_move.hit_at(i, j)
        if self.to_move is self.player1:
            self.player2.alive_boat_count = self.player2.count_alive_boats()
            if not self.player2.my_board.has_boat_at(i, j):
                self.to_move = self.player2
        else:
            self.player1.alive_boat_count = self.player1.count_alive_boats()
            if not self.player1.my_board.has_boat_at(i, j):
                self.to_move = self.player1
        self.check_game_over()
