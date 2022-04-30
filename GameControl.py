import time
from math import sqrt

from Character import *
from Sounds import Sound


class GameControl:
    # Should be moved to yaml similarly to Map.py
    __MIN_NUM_OF_SKELETONS = 2
    __MAX_NUM_OF_SKELETONS = 5
    _ENEMY_TYPES = [Skeleton.TYPE,
                    Boss.TYPE]
    LEVEL_STATUS_IN_PROGRESS = "IN PROGRESS"
    LEVEL_STATUS_FAILED = "FAILED"
    LEVEL_STATUS_WON = "WON"
    __MAX_NUM_OF_HERO_MOVES = 2

    def __init__(self, game_map):
        self._level_status = GameControl.LEVEL_STATUS_IN_PROGRESS
        self.map = game_map
        self.screen = None
        self.__generate_level()
        self.set_level_in_progress()

    def __generate_level(self, level_up=False):
        self.__characters = dict()
        if level_up:
            self.map.generate_level()
        self.__init_free_floor_map()
        self.__create_hero()
        self.__create_enemies()
        self.__init_character_positions()

    def __add_free_floor_map(self, pos: tuple):
        self.__free_floor_map.append(pos)

    def __create_boss(self):
        self.__register_character(Boss())

    def __create_enemies(self):
        self.__create_boss()
        self.__create_skeletons()

    def __create_hero(self):
        self.hero = Hero()
        self.__register_character(self.hero)

    def __create_skeletons(self):
        num_of_skeletons = randint(
            self.__MIN_NUM_OF_SKELETONS, self.__MAX_NUM_OF_SKELETONS)

        key_holder = randint(0, num_of_skeletons - 1)
        for i in range(num_of_skeletons):
            skeleton = Skeleton(i)
            skeleton.set_key_holder(i == key_holder)
            self.__register_character(skeleton)

    def __init_character_positions(self):
        for character in self.__characters.values():
            if character.get_character_type() == Hero.TYPE:
                character.init_position(0, 0)
                self.__free_floor_map.pop(0)
                character.init_images()
            else:
                (x, y), pos_idx = self.get_random_floor_map()
                character.init_position(x, y)
                self.__free_floor_map.pop(pos_idx)

    def __init_free_floor_map(self):
        self.__free_floor_map = []
        for x in range(self.map.map_config.map_x):
            for y in range(self.map.map_config.map_y):
                if self.map.map_config.is_floor(x, y):
                    self.__add_free_floor_map((x, y))

    def __register_character(self, character):
        self.__characters[character.get_name()] = character

    def __remove_free_floor_map(self, pos: tuple):
        if pos in self.__free_floor_map:
            self.__free_floor_map.remove(pos)

    def battle(self, attacker, defender):
        if attacker and defender:
            while attacker.hp > 0 and defender.hp > 0:
                self.strike(attacker, defender)
                tmp = attacker
                attacker = defender
                defender = tmp
            self.remove_killed(defender if defender.hp < 1 else attacker)

    def control_enemy(self, character):
        if character.get_character_type() == Hero.TYPE:
            if character.num_of_moves == self.__MAX_NUM_OF_HERO_MOVES:
                character.num_of_moves = 0
                self.move_enemies()
                self.screen.draw_screen()
        elif character.x == self.hero.x and character.y == self.hero.y:
            self.prepare_battle(character)
            self.screen.draw_screen()

    def eval_level_status(self, character):
        if character.get_character_type() == Skeleton.TYPE:
            if character.is_key_holder() and character.hp < 1:
                self.set_level_won()
        elif character.get_character_type() == Hero.TYPE and character.hp < 1:
            self.set_level_failed()
        else:
            self.set_level_in_progress()

    def get_enemy_at_position(self, x, y):
        for character in self.__characters.values():
            if character.get_position() == (x, y) and character.get_character_type() in self.get_enemy_types():
                return character

    def get_characters(self):
        return dict(self.__characters)

    def get_distance_of_hero(self, enemy):
        return sqrt((enemy.x - self.hero.x) ** 2 + (enemy.y - - self.hero.y) ** 2)

    def get_enemy(self, character):
        x, y = character.get_position()
        return self.get_enemy_at_position(x, y)

    @staticmethod
    def get_enemy_types():
        return GameControl._ENEMY_TYPES

    def get_level_status(self):
        return self._level_status

    def get_random_floor_map(self):
        pos_idx = randint(0, len(self.__free_floor_map) - 1)
        return self.__free_floor_map[pos_idx], pos_idx

    @staticmethod
    def get_stats(character):
        return character.get_stats()

    def move(self, character, x=0, y=0):
        if self._level_status in (self.LEVEL_STATUS_WON, self.LEVEL_STATUS_FAILED):
            self.set_level_in_progress()
        if x != 0:
            if self.map.map_config.is_floor(character.x + x, character.y):
                character.x += x
        elif y != 0:
            if self.map.map_config.is_floor(character.x, character.y + y):
                character.y += y
        else:
            pass
        self.control_enemy(character)

    def move_enemies(self):
        enemies = []
        for character in self.__characters.values():
            if character.get_character_type() in self._ENEMY_TYPES:
                enemies.append(character)
        for enemy in enemies:
            self.move_enemy(enemy)

    def move_enemy(self, enemy):
        shortest_path_to_hero = self.map.get_shortest_path((enemy.x, enemy.y), (self.hero.x, self.hero.y))
        if shortest_path_to_hero:
            x, y = shortest_path_to_hero[1]
            self.move(enemy, x - enemy.x, y - enemy.y)

    def prepare_battle(self, character):
        x = character.x
        y = character.y
        if character.TYPE == Hero.TYPE:
            current_enemy = self.get_enemy_at_position(
                x, y)
            self.battle(self.hero, current_enemy)
        else:
            self.battle(character, self.hero)

    def remove_killed(self, character):
        del self.__characters[character.get_name()]
        self.eval_level_status(character)

    def set_level_won(self):
        Sound.play(Sound.SOUND_WIN)
        self._level_status = self.LEVEL_STATUS_WON
        Character.level += 1
        self.__generate_level(True)

    def set_level_failed(self):
        Sound.play(Sound.SOUND_GAME_OVER)
        self._level_status = self.LEVEL_STATUS_FAILED
        Character.level = 1
        self.__generate_level()

    def set_level_in_progress(self):
        self._level_status = self.LEVEL_STATUS_IN_PROGRESS

    @staticmethod
    def strike(attacker, defender):
        Sound.play(Sound.SOUND_HIT)
        time.sleep(0.2)
        attacker_sv = attacker.get_sv()
        if attacker_sv > defender.get_dp():
            defender.hp -= attacker_sv - defender.get_dp()
