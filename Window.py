from tkinter import Tk

from win32api import GetMonitorInfo, MonitorFromPoint

from Config import Config
from GameControl import GameControl
from Images import ImgConfig
from Map import Map
from Screen import GameScreen
from Sounds import Sound

CFG_FILE = r'./config/WindowConfig.yaml'
TITLE = "title"
LEFT_KEY = "left_key"
RIGHT_KEY = "right_key"
UP_KEY = "up_key"
DOWN_KEY = "down_key"
SPACE = "space_key"


class Window(Tk):

    def __init__(self):
        super().__init__()
        self.__title = None
        self.__down_key = None
        self.__left_key = None
        self.__up_key = None
        self.__right_key = None
        self.__space_key = None
        self.closing = False

        self.load_config()

        self.map = Map()

        self.game_control = GameControl(self.map)

        self.__bind_keys()

        self.center()
        self.title(self.__title)

        self.screen = GameScreen(
            self, self.map, self.game_control)

        self.game_control.screen = self.screen
        Sound.play(Sound.SOUND_START)

    def __bind_keys(self):
        self.bind(self.__left_key, self.left_key)
        self.bind(self.__right_key, self.right_key)
        self.bind(self.__up_key, self.up_key)
        self.bind(self.__down_key, self.down_key)
        self.bind(self.__space_key, self.space_key)

    def center(self):
        w = ImgConfig.IMG_SIZE * self.map.map_config.map_x
        h = ImgConfig.IMG_SIZE * self.map.map_config.map_y + self.map.map_config.stats_x

        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        monitor_work_map = monitor_info.get("Work")
        ws = monitor_work_map[2]
        hs = monitor_work_map[3]

        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def down_key(self, event):
        if self.game_control:
            self.game_control.move(self.game_control.hero, y=1)

    def draw_screen(self):
        if self.screen and not self.closing:
            self.screen.draw_screen()

    def destroy(self) -> None:
        self.closing = True
        super().destroy()

    def left_key(self, event):
        if self.game_control:
            self.game_control.move(self.game_control.hero, x=-1)

    def load_config(self):
        window_config = Config.load_config(CFG_FILE)
        self.__title = window_config[TITLE]
        self.__left_key = window_config[LEFT_KEY]
        self.__right_key = window_config[RIGHT_KEY]
        self.__up_key = window_config[UP_KEY]
        self.__down_key = window_config[DOWN_KEY]
        self.__space_key = window_config[SPACE]

    def right_key(self, event):
        if self.game_control:
            self.game_control.move(self.game_control.hero, x=1)

    def up_key(self, event):
        if self.game_control:
            self.game_control.move(self.game_control.hero, y=-1)

    def space_key(self, event):
        if self.game_control:
            self.game_control.prepare_battle(self.game_control.hero)
