from models.exces import *
from models.boat import Boat
from models.board import Board


class Player:
    def __init__(self, username, board=None):
        self.username = username
        self.my_board = board or Board()
        self.other_board: Board | None = None  # other board will be inited at game session start
        self.hit_history: list[tuple] = []  # at hit input first check hit history
        self.boats: list[Boat] = self.my_board.boats
        # self.total_health = sum(boat.health for boat in self.boats)
        self.alive_boat_count = self.count_alive_boats()

    def hit_at(self, i, j):
        self.other_board.being_hitted_at(i, j)
        self.hit_history.append((i, j))

    def count_alive_boats(self):
        return sum(1 for boat in self.boats if boat.is_alive)