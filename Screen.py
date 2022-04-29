from tkinter import *

from Character import Skeleton
from Images import *


class GameScreen(Canvas):
    # Should be moved to a yaml, similarly to Map.py
    __STATS_POSITION_X = 160
    __STATS_POSITION_Y = 20
    __STATS_POSITION_OFFSET = 350
    __STATS_HEIGHT = 50
    __STATS_FORMAT = '{name} (Level {level} ) HP: {hp}/{orig_hp} | DP: {dp} | SP: {sp} '
    __STATS_FORMAT_ENEMY = '{name} HP: {hp}/{orig_hp} | DP: {dp} | SP: {sp} | Key: ({keyholder})'
    __STATS_FORMAT_WON = 'CONGRATS!!! YOU WON!!! NEXT LEVEL IS {level}'
    __STATS_FORMAT_FAILED = 'OHH, YOU JUST DIED!!! CURRENT LEVEL IS {level}'
    __HERO_STAT_TEXT_COLOR = 'Black'
    __HERO_STAT_TEXT_FONT = 'Arial 11 bold'
    __ENEMY_STAT_TEXT_COLOR = 'Red'
    __ENEMY_STAT_TEXT_FONT = 'Arial 11 bold'

    def __init__(self, window, game_map, game_control):
        super().__init__(window, width=game_map.map_config.map_x * ImgConfig.IMG_SIZE,
                         height=game_map.map_config.map_y * ImgConfig.IMG_SIZE + self.__STATS_HEIGHT)
        self.__floor = None
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
                         fill=self.__HERO_STAT_TEXT_COLOR,
                         font=self.__HERO_STAT_TEXT_FONT)

        if self._game_control.get_level_status() == self._game_control.LEVEL_STATUS_WON:
            txt = self.__STATS_FORMAT_WON.format(level=self._game_control.hero.level)
        elif self._game_control.get_level_status() == self._game_control.LEVEL_STATUS_FAILED:
            txt = self.__STATS_FORMAT_FAILED.format(level=self._game_control.hero.level)
        else:
            txt = self.get_enemy_stat_txt()

        self.create_text(self.get_enemy_txt_pos_x(),
                         self.get_txt_pos_y(),
                         text=txt,
                         fill=self.__ENEMY_STAT_TEXT_COLOR,
                         font=self.__ENEMY_STAT_TEXT_FONT)

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
            return self.__STATS_FORMAT_ENEMY.format(name=enemy.get_name(),
                                                    hp=enemy_hp, orig_hp=enemy_orig_hp, dp=enemy_dp, sp=enemy_sp,
                                                    keyholder=keyholder)

    def get_hero_stat_txt(self):
        hero = self._game_control.hero
        if hero:
            level, hp, orig_hp, dp, sp = self._game_control.get_stats(
                hero)
            return self.__STATS_FORMAT.format(name=hero.get_name(),
                                              level=level, hp=hp, orig_hp=orig_hp, dp=dp, sp=sp)

    def get_hero_txt_pos_x(self):
        return self.__STATS_POSITION_X

    def get_enemy_txt_pos_x(self):
        return self.__STATS_POSITION_X + self.__STATS_POSITION_OFFSET

    def get_txt_pos_y(self):
        return ImgConfig.IMG_SIZE * self._map.map_config.map_y + self.__STATS_POSITION_Y

    def load_images(self) -> None:
        self.__floor = ImgFloor()
