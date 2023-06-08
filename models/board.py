import random

from models.exces import *
from models.boat import Boat

from pprint import pprint


class Board:
    def __init__(self, size=8, ships=None):
        if not ships:
            ships = {4: 1, 3: 2, 2: 3}  # count : lenght
            # ships = [(1, 4), (2, 3), (3, 2), (4, 1)]
        self._data = [[0 for _ in range(size)] for _ in range(size)]
        self.boats: list[Boat] = []
        self.ships = ships
        self.free_cells: list[tuple] | None = None
        self.update_free_cells()
        self.random_init()

    @property
    def data(self):
        return self._data

    def _is_valid_pos(self, i, j):
        return (0 <= i < len(self.data)) and (0 <= j < len(self.data[0]))

    def update_free_cells(self):
        self.free_cells = [(i, j) for i in range(len(self._data))
                           for j in range(len(self._data[0])) if self._is_available_cell(i, j)]

    def _is_available_cell(self, i, j):
        if self._is_valid_pos(i - 1, j - 1):
            if self.data[i - 1][j - 1] != 0:
                return False
        if self._is_valid_pos(i - 1, j):
            if self.data[i - 1][j] != 0:
                return False
        if self._is_valid_pos(i - 1, j + 1):
            if self.data[i - 1][j + 1] != 0:
                return False
        if self._is_valid_pos(i, j - 1):
            if self.data[i][j - 1] != 0:
                return False
        if self._is_valid_pos(i, j):
            if self.data[i][j] != 0:
                return False
        if self._is_valid_pos(i, j + 1):
            if self.data[i][j + 1] != 0:
                return False
        if self._is_valid_pos(i + 1, j - 1):
            if self.data[i + 1][j - 1] != 0:
                return False
        if self._is_valid_pos(i + 1, j):
            if self.data[i + 1][j] != 0:
                return False
        if self._is_valid_pos(i + 1, j + 1):
            if self.data[i + 1][j + 1] != 0:
                return False

        return True

    def set_value_at(self, i, j, value):
        if not self._is_valid_pos(i, j):
            raise BoardIndexError()
        if not self._is_available_cell(i, j):
            raise BoatCollisionError()

        self._data[i][j] = value
        self.update_free_cells()

    def set_boat(self, boat: Boat):
        boat_pos = boat.get_all_coords()
        for pos in boat_pos:
            if not (self._is_valid_pos(*pos) and self._is_available_cell(*pos)):
                raise BoardIndexError()

        for pos in boat_pos:
            self.data[pos[0]][pos[1]] = 1

        self.boats.append(boat)
        self.update_free_cells()

    def get_value_at(self, i, j):
        return self.data[i][j]

    def has_boat_at(self, i, j):
        for boat in self.boats:
            if (i, j) in boat.get_all_coords():
                return True

        return False

    def change_value_at(self, i, j, value):
        self._data[i][j] = value

    def being_hitted_at(self, i, j) -> bool:
        """Returns True if a boat is hitted, otherwise False."""
        pos = (i, j)
        # self.set_value_at(*pos, self.data[i][j] + 2)
        # self._data[i][j] += 2
        self.change_value_at(i, j, self.data[i][j] + 2)
        if self.has_boat_at(*pos):
            for boat in self.boats:
                if pos in boat.get_all_coords():
                    boat.being_hitted()
                    if not boat.is_alive:
                        for x, y in boat.get_all_coords():
                            self.change_value_at(x, y, self.data[x][y] + 1)
                    return True

        return False

    def get_horizontal_segments(self):
        all_rows = [list() for _ in range(len(self.data))]

        for point in self.free_cells:
            all_rows[point[0]].append(point)

        all_segments = []

        for row in all_rows:
            row_segments = []
            current_segment = []
            for i in range(len(row)):  # ith point in the current row
                current_segment.append(row[i])

                if i == len(row) - 1:
                    continue

                if row[i][1] + 1 != row[i + 1][1]:
                    row_segments.append(current_segment)
                    current_segment = []

            if current_segment:
                row_segments.append(current_segment)

            all_segments.extend(row_segments)
            current_segment = []
            row_segments = []

        return all_segments

    def get_vertical_segments(self):
        all_rows = [list() for _ in range(len(self.data))]

        transposed_cells = [point[::-1] for point in self.free_cells]

        for point in transposed_cells:
            all_rows[point[0]].append(point)

        all_segments = []

        for row in all_rows:
            row_segments = []
            current_segment = []
            for i in range(len(row)):  # ith point in the current row
                current_segment.append(row[i])

                if i == len(row) - 1:
                    continue

                if row[i][1] + 1 != row[i + 1][1]:
                    row_segments.append(current_segment)
                    current_segment = []

            if current_segment:
                row_segments.append(current_segment)

            all_segments.extend(row_segments)
            current_segment = []
            row_segments = []

        for segment in all_segments:
            for i in range(len(segment)):
                segment[i] = segment[i][::-1]

        return all_segments

    def random_init(self):
        try:
            for count, length in self.ships.items():
                for i in range(count):
                    horizontal = random.choice([False, True])
                    if horizontal:
                        available_segments = [segment for segment in self.get_horizontal_segments()
                                              if len(segment) >= length]
                        if available_segments:
                            space = random.choice(available_segments)
                        else:
                            space = random.choice([segment for segment in self.get_vertical_segments()
                                                   if len(segment) >= length])
                    else:
                        available_segments = [segment for segment in self.get_vertical_segments()
                                              if len(segment) >= length]
                        if available_segments:
                            space = random.choice(available_segments)
                        else:
                            space = random.choice([segment for segment in self.get_horizontal_segments()
                                                   if len(segment) >= length])

                    boat_space = random.choice(
                        [space[i:i + length] for i in range(len(space))
                         if len(space[i:i + length]) >= length])
                    boat = Boat(head=boat_space[0], tail=boat_space[-1])
                    self.set_boat(boat)
        except IndexError:
            self.__init__(size=len(self._data), ships=self.ships)
