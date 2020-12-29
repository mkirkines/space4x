import math
from typing import List, Tuple, Union

even_moves: List[List[int]] = [
    [1, 1],
    [1, 0],
    [1, -1],
    [0, -1],
    [-1, 0],
    [0, -1],
]
odd_moves: List[List[int]] = [
    [0, 1],
    [1, 0],
    [0, -1],
    [-1, -1],
    [-1, 0],
    [-1, 1],
]


def distance(x_0: int, y_0: int, x_1: int, y_1: int) -> float:
    return math.sqrt((y_1 - y_0) ** 2 + (x_1 - x_0) ** 2)


def find_path(
    x_start: int, y_start: int, x_end: int, y_end: int
) -> List[List[int]]:
    path = []
    current_x = x_start
    current_y = y_start
    while (dist := distance(current_x, current_y, x_end, y_end)) != 0:
        best_dist = 10e4
        best_pos: Union[None, Tuple[int, int]] = None
        moves = even_moves if current_y & 1 == 0 else odd_moves
        path.append([current_x, current_y])
        for move in moves:
            new_pos: Tuple[int, int] = (
                current_x + move[0],
                current_y + move[1],
            )
            new_dist = distance(*new_pos, x_end, y_end)
            if new_dist < dist and new_dist < best_dist:
                best_dist = new_dist
                best_pos = new_pos
        current_x = best_pos[0]  # type: ignore
        current_y = best_pos[1]  # type: ignore
    return path


if __name__ == "__main__":
    path = find_path(6, 3, 9, 6)
    print(path)
