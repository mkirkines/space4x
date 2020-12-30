from dataclasses import dataclass, field
from queue import PriorityQueue, Queue
from typing import Any, Dict, List, Union

from space4x.hex_grid import HexGrid, HexTile


# This class is necessary, as PriorityQueue tries to
# compare not only the priorities, but also the items,
# but arcade.Sprite has no suitable comparator.
# This makes PriorityQueue compare only the priority.
# See: https://docs.python.org/3/library/queue.html
@dataclass(order=True)
class PrioritizedItem:
    priority: float
    item: Any = field(compare=False)


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

    def heuristic(self, start_hex: HexTile, end_hex: HexTile) -> float:
        """Manhatten distance on a hexagonal grid.

        Args:
            start_hex (HexTile): Start position
            end_hex (HexTile): End position

        Returns:
            float: Distance
        """
        return (
            abs(start_hex.cube_coordinate.x - end_hex.cube_coordinate.x)
            + abs(start_hex.cube_coordinate.y - end_hex.cube_coordinate.y)
            + abs(start_hex.cube_coordinate.z - end_hex.cube_coordinate.z)
        ) / 2

    def breadth_first_search(
        self, start_hex: HexTile, end_hex: HexTile
    ) -> List[HexTile]:
        """Calculates the shortest path between two HexTiles.

        Uses the Breadth first search.

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

    def dijkstras_algorithm(
        self, start_hex: HexTile, end_hex: HexTile
    ) -> List[HexTile]:
        """Calculates the shortest path between two HexTiles.

        Uses the Dijkstra's algorithm.

        Args:
            start_hex (HexTile): Start position
            end_hex (HexTile): Target position

        Returns:
            List[HexTile]: HexTiles that make up the path
        """
        frontier: PriorityQueue[PrioritizedItem] = PriorityQueue(maxsize=0)
        frontier.put(PrioritizedItem(priority=0, item=start_hex))
        came_from: Dict[HexTile, Union[None, HexTile]] = dict()
        cost_so_far: Dict[HexTile, int] = dict()
        came_from[start_hex] = None
        cost_so_far[start_hex] = 0
        while not frontier.empty():
            current_tile = frontier.get().item
            # Early exit
            if current_tile == end_hex:
                break
            for next_tile in self.get_neighbors(hex_tile=current_tile):
                new_cost = (
                    cost_so_far[current_tile] + 1
                )  # TODO: Think about implementing path cost
                if (
                    next_tile not in cost_so_far
                    or new_cost < cost_so_far[next_tile]
                ):
                    cost_so_far[next_tile] = new_cost
                    priority = new_cost
                    frontier.put(
                        PrioritizedItem(priority=priority, item=next_tile)
                    )
                    came_from[next_tile] = current_tile

        current_tile = end_hex
        path = []
        while current_tile != start_hex:
            path.append((current_tile))
            current_tile = came_from[current_tile]  # type: ignore
        path.append(start_hex)
        path.reverse()
        return path

    def a_star(
        self, start_hex: HexTile, end_hex: HexTile
    ) -> List[HexTile]:
        """Calculates the shortest path between two HexTiles.

        Uses the A-Star algorithm.

        Args:
            start_hex (HexTile): Start position
            end_hex (HexTile): Target position

        Returns:
            List[HexTile]: HexTiles that make up the path
        """
        frontier: PriorityQueue[PrioritizedItem] = PriorityQueue(maxsize=0)
        frontier.put(PrioritizedItem(priority=0, item=start_hex))
        came_from: Dict[HexTile, Union[None, HexTile]] = dict()
        cost_so_far: Dict[HexTile, int] = dict()
        came_from[start_hex] = None
        cost_so_far[start_hex] = 0
        while not frontier.empty():
            current_tile = frontier.get().item
            # Early exit
            if current_tile == end_hex:
                break
            for next_tile in self.get_neighbors(hex_tile=current_tile):
                new_cost = (
                    cost_so_far[current_tile] + 1
                )  # TODO: Think about implementing path cost
                if (
                    next_tile not in cost_so_far
                    or new_cost < cost_so_far[next_tile]
                ):
                    cost_so_far[next_tile] = new_cost
                    priority = new_cost + self.heuristic(
                        start_hex=next_tile, end_hex=end_hex
                    )
                    frontier.put(
                        PrioritizedItem(priority=priority, item=next_tile)
                    )
                    came_from[next_tile] = current_tile

        current_tile = end_hex
        path = []
        while current_tile != start_hex:
            path.append((current_tile))
            current_tile = came_from[current_tile]  # type: ignore
        path.append(start_hex)
        path.reverse()
        return path
