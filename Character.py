import math
import random
from random import randint

from Images import ImgHeroDown, ImgSkeleton, ImgHeroUp, ImgHeroLeft, ImgHeroRight, ImgBoss
from Sounds import Sound


class Character:
    level = 1
    TYPE = "CHARACTER"

    @staticmethod
    def d6():
        return randint(1, 6)

    def __init__(self, name, img=None):
        self._dp = 0
        self._hp = 0
        self._orig_hp = 0
        self._sp = 0
        self.x = 0
        self.y = 0
        self._img_down = None
        self._img_left = None
        self._img_right = None
        self._img_up = None
        self._curr_img = None
        self.__name = name
        self.init_position()
        self.init_images(img)
        self.init_skills()

    def generate_dp(self):
        return 0

    def generate_hp(self):
        return 0

    def generate_sp(self):
        return 0

    @staticmethod
    def get_character_type():
        return Character.TYPE

    def get_dp(self):
        return self._dp

    def get_image(self):
        return self._curr_img

    def get_name(self):
        return self.__name

    def get_position(self):
        return self.x, self.y

    def get_stats(self):
        return self.level, self._hp, self._orig_hp, self._dp, self._sp

    def get_sv(self):
        return 2 * self.d6() + self._sp

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if self._hp < 1:
            Sound.play(Sound.SOUND_DEAD)

    def init_images(self, img=None):
        self._curr_img = img
        self._img_up = self._curr_img
        self._img_down = self._curr_img
        self._img_left = self._curr_img
        self._img_right = self._curr_img

    def init_position(self, x=0, y=0):
        self.x = x
        self.y = y

    def init_skills(self):
        pass


class Hero(Character):
    TYPE = "HERO"
    PERCENT_CHANCE_OF_HP_FULL_RECHARGE = 10
    PERCENT_CHANCE_OF_HP_3RD_RECHARGE = 40
    PERCENT_CHANCE_OF_HP_10PERCENT_RECHARGE = 50

    def __init__(self):
        self._x = 0
        self._y = 0
        super().__init__(__class__.__name__, ImgHeroDown())
        self.num_of_moves = 0
        self._hp = self.generate_hp()
        self._orig_hp = self._hp

    @staticmethod
    def get_character_type():
        return Hero.TYPE

    def generate_dp(self):
        return 2 * self.d6()

    def generate_hp(self):
        return 20 + 3 * self.d6()

    def generate_sp(self):
        return 5 + self.d6()

    def init_images(self, img=None):
        self._img_down = ImgHeroDown()
        self._img_up = ImgHeroUp()
        self._img_left = ImgHeroLeft()
        self._img_right = ImgHeroRight()
        self._curr_img = self._img_down

    def init_skills(self):
        full_recharge = random.randrange(100) < self.PERCENT_CHANCE_OF_HP_FULL_RECHARGE
        if full_recharge:
            self._hp = self._orig_hp
        else:
            recharge_the_third = random.randrange(100) < self.PERCENT_CHANCE_OF_HP_3RD_RECHARGE
            if recharge_the_third:
                self._hp = min(self._orig_hp, self._hp + self._orig_hp // 3)
            else:
                recharge_10_percent = random.randrange(100) < self.PERCENT_CHANCE_OF_HP_10PERCENT_RECHARGE
                if recharge_10_percent:
                    self._hp = min(self._orig_hp, self._hp + self._orig_hp // 10)

        self._dp = self.generate_dp()
        self._sp = self.generate_sp()
        self.num_of_moves = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if self._x != value:
            self._curr_img = self._img_left if self._x > value else self._img_right
            self._x = value
            self.num_of_moves += 1
            Sound.play(Sound.SOUND_STEP)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if self._y != value:
            self._curr_img = self._img_up if self._y > value else self._img_down
            self._y = value
            self.num_of_moves += 1
            Sound.play(Sound.SOUND_STEP)


class Boss(Character):
    TYPE = "BOSS"

    def __init__(self):
        super().__init__(self.__class__.__name__, ImgBoss())
        self.init_skills()

    @staticmethod
    def get_character_type():
        return Boss.TYPE

    def init_skills(self):
        self._hp = 2 * Character.level * self.d6() + self.d6()
        self._orig_hp = self._hp
        self._dp = math.floor((Character.level / 2) * self.d6() + (self.d6() / 2))
        self._sp = Character.level * self.d6() + Character.level


class Skeleton(Character):
    TYPE = "SKELETON"

    def __init__(self, skeleton_id: int):
        super().__init__(self.__class__.__name__ + str(skeleton_id), ImgSkeleton())
        self._key_holder = False
        self.init_skills()

    def generate_dp(self):
        return math.floor((Character.level / 2) * self.d6())

    def generate_hp(self):
        return 2 * Character.level * self.d6()

    def generate_sp(self):
        return Character.level * self.d6()

    @staticmethod
    def get_character_type():
        return Skeleton.TYPE

    def init_skills(self):
        self._hp = self.generate_hp()
        self._orig_hp = self._hp
        self._dp = self.generate_dp()
        self._sp = self.generate_sp()

    def is_key_holder(self):
        return self._key_holder

    def set_key_holder(self, value):
        self._key_holder = value
