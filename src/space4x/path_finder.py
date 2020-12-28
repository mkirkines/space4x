import numpy as np

even_moves = [[1, 1], [1, 0], [1, -1], [0, -1], [-1, 0], [0, -1]]
odd_moves = [[0, 1], [1, 0], [0, -1], [-1, -1], [-1, 0], [-1, 1]]


def distance(x_0, y_0, x_1, y_1):
    return np.sqrt((y_1 - y_0) ** 2 + (x_1 - x_0) ** 2)


def find_path(x_start, y_start, x_end, y_end):
    path = []
    current_x = x_start
    current_y = y_start
    while (dist := distance(current_x, current_y, x_end, y_end)) != 0:
        best_dist = 10e4
        best_pos = None
        moves = even_moves if current_y % 2 == 0 else odd_moves
        path.append([current_x, current_y])
        for move in moves:
            new_pos = current_x + move[0], current_y + move[1]
            new_dist = distance(*new_pos, x_end, y_end)
            if new_dist < dist and new_dist < best_dist:
                best_dist = new_dist
                best_pos = new_pos
        current_x = best_pos[0]
        current_y = best_pos[1]
    return path


if __name__ == "__main__":
    path = find_path(6, 3, 9, 6)
    print(path)
