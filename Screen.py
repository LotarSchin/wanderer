from tkinter import *

from Character import Skeleton
from Config import Config
from Images import *

CFG_FILE = r'./config/ScreenConfig.yaml'
# Dict keys
STATS_POSITION_X = "stats_position_x"
STATS_POSITION_Y = "stats_position_y"
STATS_POSITION_OFFSET = "stats_position_offset"
STATS_HEIGHT = "stats_height"
STATS_FORMAT = "stats_format"
STATS_FORMAT_ENEMY = "stats_format_enemy"
STATS_FORMAT_WON = "stats_format_won"
STATS_FORMAT_FAILED = "stats_format_failed"
HERO_STAT_TEXT_COLOR = "hero_stat_text_color"
HERO_STAT_TEXT_FONT = "hero_stat_text_font"
ENEMY_STAT_TEXT_COLOR = "enemy_stat_text_color"
ENEMY_STAT_TEXT_FONT = "enemy_stat_text_font"


class GameScreen(Canvas):

    def __init__(self, window, game_map, game_control):
        self.__enemy_stat_text_font = None
        self.__enemy_stat_text_color = None
        self.__hero_stat_text_font = None
        self.__hero_stat_text_color = None
        self.__stats_format_failed = None
        self.__stats_format_won = None
        self.__stats_format_enemy = None
        self.__stats_format = None
        self.__stats_height = None
        self.__stats_position_offset = None
        self.__stats_position_y = None
        self.__stats_position_x = None
        self.__floor = None
        self.load_config()
        super().__init__(window, width=game_map.map_config.map_x * ImgConfig.IMG_SIZE,
                         height=game_map.map_config.map_y * ImgConfig.IMG_SIZE + self.__stats_height)
        self.load_images()
        self.pack()
        self._window = window
        self._map = game_map
        self._game_control = game_control

    def cls(self):
        super().delete("all")

    def draw_map(self):
        for block in self._map.get_map().values():
            self.create_image(ImgConfig.IMG_SIZE * block.x, ImgConfig.IMG_SIZE * block.y,
                              image=block.img, anchor=NW)

    def draw_characters(self):
        for character in self._game_control.get_characters().values():
            self.create_image(character.x * ImgConfig.IMG_SIZE, character.y *
                              ImgConfig.IMG_SIZE, image=character.get_image(), anchor=NW)

    def draw_stats(self):
        self.create_text(self.get_hero_txt_pos_x(),
                         self.get_txt_pos_y(),
                         text=self.get_hero_stat_txt(),
                         fill=self.__hero_stat_text_color,
                         font=self.__hero_stat_text_font)

        if self._game_control.get_level_status() == self._game_control.LEVEL_STATUS_WON:
            txt = self.__stats_format_won.format(level=self._game_control.hero.level)
        elif self._game_control.get_level_status() == self._game_control.LEVEL_STATUS_FAILED:
            txt = self.__stats_format_failed.format(level=self._game_control.hero.level)
        else:
            txt = self.get_enemy_stat_txt()

        self.create_text(self.get_enemy_txt_pos_x(),
                         self.get_txt_pos_y(),
                         text=txt,
                         fill=self.__enemy_stat_text_color,
                         font=self.__enemy_stat_text_font)

    def draw_screen(self) -> None:
        self.cls()
        self.draw_map()
        self.draw_characters()
        self.draw_stats()

    def get_enemy_stat_txt(self):
        enemy = self._game_control.get_enemy(self._game_control.hero)
        if enemy:
            enemy_level, enemy_hp, enemy_orig_hp, enemy_dp, enemy_sp = self._game_control.get_stats(
                enemy)
            if enemy.get_character_type() == Skeleton.TYPE:
                keyholder = enemy.is_key_holder()
            else:
                keyholder = False
            return self.__stats_format_enemy.format(name=enemy.get_name(),
                                                    hp=enemy_hp, orig_hp=enemy_orig_hp, dp=enemy_dp, sp=enemy_sp,
                                                    keyholder=keyholder)

    def get_hero_stat_txt(self):
        hero = self._game_control.hero
        if hero:
            level, hp, orig_hp, dp, sp = self._game_control.get_stats(
                hero)
            return self.__stats_format.format(name=hero.get_name(),
                                              level=level, hp=hp, orig_hp=orig_hp, dp=dp, sp=sp)

    def get_hero_txt_pos_x(self):
        return self.__stats_position_x

    def get_enemy_txt_pos_x(self):
        return self.__stats_position_x + self.__stats_position_offset

    def get_txt_pos_y(self):
        return ImgConfig.IMG_SIZE * self._map.map_config.map_y + self.__stats_position_y

    def load_config(self):
        try:
            screen_config = dict(Config.load_config(CFG_FILE))
            self.__stats_position_x = screen_config[STATS_POSITION_X]
            self.__stats_position_y = screen_config[STATS_POSITION_Y]
            self.__stats_position_offset = screen_config[STATS_POSITION_OFFSET]
            self.__stats_height = screen_config[STATS_HEIGHT]
            self.__stats_format = screen_config[STATS_FORMAT]
            self.__stats_format_enemy = screen_config[STATS_FORMAT_ENEMY]
            self.__stats_format_won = screen_config[STATS_FORMAT_WON]
            self.__stats_format_failed = screen_config[STATS_FORMAT_FAILED]
            self.__hero_stat_text_color = screen_config[HERO_STAT_TEXT_COLOR]
            self.__hero_stat_text_font = screen_config[HERO_STAT_TEXT_FONT]
            self.__enemy_stat_text_color = screen_config[ENEMY_STAT_TEXT_COLOR]
            self.__enemy_stat_text_font = screen_config[ENEMY_STAT_TEXT_FONT]
        except AttributeError as e:
            print(Config.ERR_ATTR_ERROR.format(file=CFG_FILE, error=e))
        except KeyError as e:
            print(Config.ERR_ATTR_ERROR.format(file=CFG_FILE, error=e))

    def load_images(self) -> None:
        self.__floor = ImgFloor()
