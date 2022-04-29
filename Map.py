from collections import defaultdict

from Images import ImgFloor, ImgWall


class MapConfig:
    MAP_X = 10
    MAP_Y = 10
    STATS_X = 50
    # Right now, it is static. Random generated map would require a logic to avoid of closing characters into an area.
    _WALL_COORDINATES = [
        [3],
        [3, 5, 7, 8],
        [1, 2, 3, 5, 7, 8],
        [5],
        [0, 1, 2, 3, 5, 6, 7, 8],
        [1, 3],
        [1, 3, 5, 6, 8],
        [5, 6, 8],
        [1, 2, 3, 8],
        [3, 5, 6]
    ]

    @staticmethod
    def is_floor(x=0, y=0):
        return MapConfig.is_in_map(x, y) and x not in MapConfig._WALL_COORDINATES[y]

    @staticmethod
    def is_in_map(x=0, y=0):
        return (-1 < x < MapConfig.MAP_X) and (-1 < y < MapConfig.MAP_Y)

    @staticmethod
    def is_wall(x=0, y=0):
        return MapConfig.is_in_map(x, y) and x in MapConfig._WALL_COORDINATES[y]


class MapBlock:
    def __init__(self, x=0, y=0, is_wall=False, img=None):
        self.x = x
        self.y = y
        self.wall = is_wall
        self.img = img


class Map:

    def __init__(self):
        self.__map = None
        self.__graph = None
        self._img_floor = ImgFloor()
        self._img_wall = ImgWall()
        self.generate_map()
        self.generate_graph()

    def generate_map(self):
        self.__map = dict()
        for y in range(MapConfig.MAP_Y):
            for x in range(MapConfig.MAP_X):
                current_block = MapBlock(
                    x, y, MapConfig.is_wall(x, y), self._img_wall if MapConfig.is_wall(x, y) else self._img_floor)
                self.__map[(x, y)] = current_block

    def generate_graph(self):
        edges = []
        for key, block in self.__map.items():
            if not block.wall:
                if block.x < MapConfig.MAP_X - 1:
                    neighbour_x = self.__map[(block.x + 1, block.y)]
                    if neighbour_x:
                        if not neighbour_x.wall:
                            edges.append([(block.x, block.y), (neighbour_x.x, block.y)])

                if block.y < MapConfig.MAP_Y - 1:
                    neighbour_y = self.__map[(block.x, block.y + 1)]
                    if neighbour_y:
                        if not neighbour_y.wall:
                            edges.append([(block.x, block.y), (block.x, neighbour_y.y)])

        graph = defaultdict(list)
        for edge in edges:
            a, b = edge[0], edge[1]

            graph[a].append(b)
            graph[b].append(a)
        self.__graph = graph

    def get_graph(self):
        return self.__graph

    def get_map(self):
        return self.__map

    def get_shortest_path(self, start, goal):
        # Lotar: This code is from geeksforgeeks with some modifications
        # Breadth First Search or BFS for a Graph
        explored = []

        # Queue for traversing the
        # graph in the BFS
        queue = [[start]]

        if start == goal:
            return None

        # Loop to traverse the graph
        # with the help of the queue
        while queue:
            path = queue.pop(0)
            node = path[-1]

            # Condition to check if the
            # current node is not visited
            if node not in explored:
                neighbours = self.get_graph()[node]

                # Loop to iterate over the
                # neighbours of the node
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)

                    # Condition to check if the
                    # neighbour node is the goal
                    if neighbour == goal:
                        return new_path
                explored.append(node)

        # When the nodes are not connected
        return None
