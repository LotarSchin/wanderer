from tkinter import Tk

from win32api import GetMonitorInfo, MonitorFromPoint

from GameControl import GameControl
from Images import ImgConfig
from Map import Map, MapConfig
from Screen import GameScreen
from Sounds import Sound


class WindowConfig:
    _TITLE = "Wanderer Game"
    _LEFT_KEY = "<Left>"
    _RIGHT_KEY = "<Right>"
    _UP_KEY = "<Up>"
    _DOWN_KEY = "<Down>"
    _SPACE = "<space>"


class Window(Tk, WindowConfig):

    def __init__(self):
        super().__init__()

        self.center()
        self.title(self._TITLE)

        self.map = Map()

        self.game_control = GameControl(self.map)

        self.__bind_keys()

        self.screen = GameScreen(
            self, self.map, self.game_control)

        Sound.play(Sound.SOUND_START)

    def __bind_keys(self):
        self.bind(self._LEFT_KEY, self.left_key)
        self.bind(self._RIGHT_KEY, self.right_key)
        self.bind(self._UP_KEY, self.up_key)
        self.bind(self._DOWN_KEY, self.down_key)
        self.bind(self._SPACE, self.space_key)

    def center(self):
        w = ImgConfig.IMG_SIZE * MapConfig.MAP_X
        h = ImgConfig.IMG_SIZE * MapConfig.MAP_Y + MapConfig.STATS_X

        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        monitor_work_map = monitor_info.get("Work")
        ws = monitor_work_map[2]
        hs = monitor_work_map[3]

        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def down_key(self, event):
        self.game_control.move(self.game_control.hero, y=1)

    def draw_screen(self):
        self.screen.draw_screen()

    def left_key(self, event):
        self.game_control.move(self.game_control.hero, x=-1)

    def right_key(self, event):
        self.game_control.move(self.game_control.hero, x=1)

    def up_key(self, event):
        self.game_control.move(self.game_control.hero, y=-1)

    def space_key(self, event):
        self.game_control.prepare_battle(self.game_control.hero)
