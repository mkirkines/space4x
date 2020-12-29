from queue import Queue
from typing import Dict, List, Union

from space4x.hex_grid import HexGrid, HexTile


class PathFinder:
    """Implements different path finding algorithms."""

    cube_directions = [
        [1, -1, 0],
        [1, 0, -1],
        [0, 1, -1],
        [-1, 1, 0],
        [-1, 0, 1],
        [0, -1, 1],
    ]

    def __init__(self, hex_grid: HexGrid) -> None:
        """Initializes the PathFinder class.

        It needs the games HexGrid.

        Args:
            hex_grid (HexGrid): current HexGrid of the game.
        """
        self.hex_grid = hex_grid

    def get_neighbors(self, hex_tile: HexTile) -> List[HexTile]:
        """Determines the direct neighbors of a given HexTile.

        Args:
            hex_tile (HexTile): HexTile of which the neighbors are determined

        Returns:
            List[HexTile]: List of neighboring tiles
        """
        neighbors = []
        for direction in self.cube_directions:
            if (
                neighbor := self.hex_grid.get_Tile_by_xyz(
                    x=hex_tile.cube_coordinate.x + direction[0],
                    y=hex_tile.cube_coordinate.y + direction[1],
                    z=hex_tile.cube_coordinate.z + direction[2],
                )
            ) is not None:
                neighbors.append(neighbor)
        return neighbors

    def breadth_first_search(
        self, start_hex: HexTile, end_hex: HexTile
    ) -> List[HexTile]:
        """Calculates the shortest path between two HexTiles.

        Args:
            start_hex (HexTile): Start position
            end_hex (HexTile): Target position

        Returns:
            List[HexTile]: HexTiles that make up the path
        """
        frontier: Queue[HexTile] = Queue(maxsize=0)
        frontier.put(start_hex)
        came_from: Dict[HexTile, Union[None, HexTile]] = dict()
        came_from[start_hex] = None
        while not frontier.empty():
            current_tile = frontier.get()
            # Early exit
            if current_tile == end_hex:
                break
            for next_tile in self.get_neighbors(hex_tile=current_tile):
                if next_tile not in came_from:
                    frontier.put(next_tile)
                    came_from[next_tile] = current_tile

        current_tile = end_hex
        path = []
        while current_tile != start_hex:
            path.append((current_tile))
            current_tile = came_from[current_tile]  # type: ignore
        path.append(start_hex)
        path.reverse()
        return path
