from models.exces import *


class Boat:
    def __init__(self, head: tuple, tail: tuple):
        self.head = head
        self.tail = tail
        self.check_valid_coords()
        self.length = len(self.get_all_coords())
        self.health = self.length
        self.is_alive = True

    def check_valid_coords(self) -> None:
        if not (self.head[0] == self.tail[0]
                or self.head[1] == self.tail[1]):
            raise BoatOrientationError()

    def get_all_coords(self) -> list:
        x_min = min(self.head[0], self.tail[0])
        x_max = max(self.head[0], self.tail[0])

        y_min = min(self.head[1], self.tail[1])
        y_max = max(self.head[1], self.tail[1])

        points = []
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                points.append((x, y))

        return points

    def being_hitted(self) -> None:
        self.health -= 1
        if self.health == 0:
            self.is_alive = False

    def __repr__(self) -> str:
        return f'Boat: HEAD:{self.head}, TAIL:{self.tail}, HEALTH:{self.health}'
