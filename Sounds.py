import os

from pygame import mixer


class PlaySoundError(Exception):
    ErrorMsg = "Error, can't play sound: {sound}!"


class Sound:
    # Should be moved to yaml, similarly to Map.py
    __DIR = os.getcwd() + "/sounds/"
    SOUND_DEAD = __DIR + "dead.mp3"
    SOUND_GAME_OVER = __DIR + "gameover.wav"
    SOUND_HIT = __DIR + "hit.mp3"
    SOUND_START = __DIR + "start.mp3"
    SOUND_STEP = __DIR + "step.mp3"
    SOUND_WIN = __DIR + "win.mp3"

    @staticmethod
    def play(sound2play):
        try:
            mixer.init()
            mixer.music.load(sound2play)
            mixer.music.set_volume(0.6)
            mixer.music.play(1)
        except Exception as e:
            raise PlaySoundError(PlaySoundError.ErrorMsg.format(sound=sound2play))
