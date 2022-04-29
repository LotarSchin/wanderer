import random
from collections import defaultdict

import yaml

from Images import ImgFloor, ImgWall

CFG_FILE = r'./config/MapConfig.yaml'
ERR_FILE_NOT_EXIST = "{file} does not exist!"
ERR_ATTR_ERROR = "Attribute error occured during the processing of {file}! Message: {error}"
ERR_KEY_ERROR = "Key error occured during the processing of {file}! Message: {error}"
# Dict keys
MAP_X = "map_x"
MAP_Y = "map_y"
STATS_X = "stats_x"
WALL_COORDINATES_V1 = 'wall_coordinates_v1'
WALL_COORDINATES_V2 = 'wall_coordinates_v2'


class MapConfig:

    def __init__(self):
        self.map_x = 0
        self.map_y = 0
        self.stats_x = 0
        self.act_wall_list = []
        self.wall_list_v1 = []
        self.wall_list_v2 = []
        self.map_config = dict()
        self.load_config()

    def is_floor(self, x=0, y=0):
        return self.is_in_map(x, y) and x not in self.act_wall_list[y]

    def is_in_map(self, x=0, y=0):
        return (-1 < x < self.map_x) and (-1 < y < self.map_y)

    def is_wall(self, x=0, y=0):
        return self.is_in_map(x, y) and x in self.act_wall_list[y]

    def load_config(self):
        with open(CFG_FILE) as cfg:
            try:
                map_config = yaml.load(cfg, Loader=yaml.FullLoader)
                self.map_x = map_config[MAP_X]
                self.map_y = map_config[MAP_Y]
                self.stats_x = map_config[STATS_X]
                self.wall_list_v1 = list(map_config[WALL_COORDINATES_V1].values())
                self.wall_list_v2 = list(map_config[WALL_COORDINATES_V2].values())
                self.act_wall_list = self.wall_list_v1 if random.choice(
                    [True, False]) else self.wall_list_v2
            except FileNotFoundError:
                print(ERR_FILE_NOT_EXIST.format(file=CFG_FILE))
            except AttributeError as e:
                print(ERR_ATTR_ERROR.format(file=CFG_FILE, error=e))
            except KeyError as e:
                print(ERR_KEY_ERROR.format(file=CFG_FILE, error=e))


class MapBlock:
    def __init__(self, x=0, y=0, is_wall=False, img=None):
        self.x = x
        self.y = y
        self.wall = is_wall
        self.img = img


class Map:

    def __init__(self):
        self.__wall_config = None
        self.__map = None
        self.__graph = None
        self._img_floor = ImgFloor()
        self._img_wall = ImgWall()
        self.map_config = MapConfig()
        self.generate_map()
        self.generate_graph()

    def generate_map(self):
        self.__map = dict()
        for y in range(self.map_config.map_y):
            for x in range(self.map_config.map_x):
                is_wall = self.map_config.is_wall(x, y)
                current_block = MapBlock(
                    x, y, is_wall, self._img_wall if is_wall else self._img_floor)
                self.__map[(x, y)] = current_block

    def generate_graph(self):
        edges = []
        for key, block in self.__map.items():
            if not block.wall:
                if block.x < self.map_config.map_x - 1:
                    neighbour_x = self.__map[(block.x + 1, block.y)]
                    if neighbour_x:
                        if not neighbour_x.wall:
                            edges.append([(block.x, block.y), (neighbour_x.x, block.y)])

                if block.y < self.map_config.map_y - 1:
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
