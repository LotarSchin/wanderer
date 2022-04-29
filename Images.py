from tkinter import PhotoImage


class ImgConfig:
    __DIR = "images/"
    _FLOOR = __DIR + "floor.png"
    _WALL = __DIR + "wall.png"
    _HERO_DOWN = __DIR + "hero-down.png"
    _HERO_UP = __DIR + "hero-up.png"
    _HERO_RIGHT = __DIR + "hero-right.png"
    _HERO_LEFT = __DIR + "hero-left.png"
    _SKELETON = __DIR + "skeleton.png"
    _BOSS = __DIR + "boss.png"
    IMG_SIZE = 72


class ImgBoss(PhotoImage, ImgConfig):
    def __init__(self) -> None:
        super().__init__(file=self._BOSS)


class ImgFloor(PhotoImage, ImgConfig):
    def __init__(self) -> None:
        super().__init__(file=self._FLOOR)


class ImgHeroDown(PhotoImage, ImgConfig):
    def __init__(self) -> None:
        super().__init__(file=self._HERO_DOWN)


class ImgHeroLeft(PhotoImage, ImgConfig):
    def __init__(self) -> None:
        super().__init__(file=ImgConfig._HERO_LEFT)


class ImgHeroRight(PhotoImage, ImgConfig):
    def __init__(self) -> None:
        super().__init__(file=ImgConfig._HERO_RIGHT)


class ImgHeroUp(PhotoImage, ImgConfig):
    def __init__(self) -> None:
        super().__init__(file=self._HERO_UP)


class ImgSkeleton(PhotoImage, ImgConfig):
    def __init__(self) -> None:
        super().__init__(file=self._SKELETON)


class ImgWall(PhotoImage, ImgConfig):
    def __init__(self) -> None:
        super().__init__(file=self._WALL)
