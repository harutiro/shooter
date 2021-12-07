from random import random

import pyxel
import pygame

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

STAR_COUNT = 100
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW = 5

PLAYER_CORONA_WIDTH = 13
PLAYER_CORONA_HEIGHT = 43
PLAYER_WIDTH = 21
PLAYER_HEIGHT = 27
PLAYER_SPEED = 3
PLAYER_SET_IMAGE = 0

BULLET_WIDTH = 2
BULLET_HEIGHT = 8
BULLET_COLOR = 11
BULLET_SPEED = 4

ENEMY_CORONA_WIDTH = 30
ENEMY_CORONA_HEIGHT = 26
ENEMY_WIDTH = 25
ENEMY_HEIGHT = 16
ENEMY_SPEED = 1.9
ENEMY_SET_IMAGE =16

BLAST_START_RADIUS = 1
BLAST_END_RADIUS = 8
BLAST_COLOR_IN = 7
BLAST_COLOR_OUT = 10

PLAY_MODE_CORONA = False

enemy_list = []
bullet_list = []
blast_list = []

class MusicPlayer:
    def __init__(self,filename):
        self.filename = filename
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(1000) #イントロ有りで1曲丸々再生
        pygame.mixer.music.set_volume(0.2)
        print("OK")

    def loop(self,time=0.0):
        pos = pygame.mixer.music.get_pos() #再生している音楽の再生時間を取得する
        if int(pos) == -1: #再生が終了するとposは-1を返すんだって！知らなかった！
            pygame.mixer.music.play(-1,time) #-1を指定することでループ再生、timeの指定秒数からスタートさせる
             
             


def update_list(list):
    for elem in list:
        elem.update()


def draw_list(list):
    for elem in list:
        elem.draw()


def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)
        else:
            i += 1


class Background:
    def __init__(self):
        self.star_list = []
        for i in range(STAR_COUNT):
            self.star_list.append(
                (random() * pyxel.width, random() * pyxel.height, random() * 1.5 + 1)
            )

    def update(self):
        for i, (x, y, speed) in enumerate(self.star_list):
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            self.star_list[i] = (x, y, speed)

    def draw(self):
        for (x, y, speed) in self.star_list:
            pyxel.pset(x, y, STAR_COLOR_HIGH if speed > 1.8 else STAR_COLOR_LOW)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.alive = True

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= PLAYER_SPEED

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += PLAYER_SPEED

        if pyxel.btn(pyxel.KEY_UP):
            self.y -= PLAYER_SPEED

        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += PLAYER_SPEED

        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - self.w)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - self.h)

        if pyxel.btnp(pyxel.KEY_SPACE):
            Bullet(
                self.x + (PLAYER_WIDTH - BULLET_WIDTH) / 2, self.y - BULLET_HEIGHT / 2
            )

            pyxel.play(0, 0)

    def draw(self):
        if PLAY_MODE_CORONA:
            pyxel.blt(self.x, self.y, 0, 128, 0, self.w, self.h, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, 0)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.alive = True

        bullet_list.append(self)

    def update(self):
        self.y -= BULLET_SPEED

        if self.y + self.h - 1 < 0:
            self.alive = False

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, BULLET_COLOR)


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.dir = 1
        self.alive = True
        self.offset = int(random() * 60)

        enemy_list.append(self)

    def update(self):
        if (pyxel.frame_count + self.offset) % 60 < 30:
            self.x += ENEMY_SPEED
            self.dir = 1
        else:
            self.x -= ENEMY_SPEED
            self.dir = -1

        self.y += ENEMY_SPEED

        if self.y > pyxel.height - 1:
            self.alive = False

    def draw(self):
        if PLAY_MODE_CORONA:
            pyxel.blt(self.x, self.y, 0, 152, 0, self.w * self.dir, self.h, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 32, 0, self.w * self.dir, self.h, 0)


class Blast:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BLAST_START_RADIUS
        self.alive = True

        blast_list.append(self)

    def update(self):
        self.radius += 1

        if self.radius > BLAST_END_RADIUS:
            self.alive = False

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, BLAST_COLOR_IN)
        pyxel.circb(self.x, self.y, self.radius, BLAST_COLOR_OUT)


class App:
    def __init__(self):
        pyxel.init(200, 250, caption="Pyxel Shooter")

        pyxel.image(0).load(
            0,
            0,
            "senntouki.png",
        )

        pyxel.image(0).load(
            32,
            0,
            "ufo.png",
        )

        pyxel.image(0).load(
            128,
            0,
            "coronawakutinn.png",
        )

        pyxel.image(0).load(
            152,
            0,
            "corona.png",
        )

        pyxel.sound(0).set("a3a2c1a1", "p", "7", "s", 5)
        pyxel.sound(1).set("a3a2c2c2", "n", "7742", "s", 10)

        self.scene = SCENE_TITLE
        self.score = 0
        self.background = Background()
        self.player = Player(pyxel.width / 2, pyxel.height - 20)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.background.update()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()


    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY
        if pyxel.btnp(pyxel.KEY_C):
            global PLAY_MODE_CORONA
            global ENEMY_HEIGHT
            global ENEMY_WIDTH
            global PLAYER_WIDTH
            global PLAYER_HEIGHT

            PLAY_MODE_CORONA = True

            ENEMY_HEIGHT = ENEMY_CORONA_HEIGHT
            ENEMY_WIDTH = ENEMY_CORONA_WIDTH
            PLAYER_WIDTH = PLAYER_CORONA_WIDTH
            PLAYER_HEIGHT = PLAYER_CORONA_HEIGHT

            self.player = Player(pyxel.width / 2, pyxel.height - 20)

            self.scene = SCENE_PLAY    


    def update_play_scene(self):
        if pyxel.frame_count % 6 == 0:
            Enemy(random() * (pyxel.width - PLAYER_WIDTH) + 20, 20)

        for a in enemy_list:
            for b in bullet_list:
                if (
                    a.x + a.w > b.x
                    and b.x + b.w > a.x
                    and a.y + a.h > b.y
                    and b.y + b.h > a.y
                ):
                    a.alive = False
                    b.alive = False

                    blast_list.append(
                        Blast(a.x + ENEMY_WIDTH / 2, a.y + ENEMY_HEIGHT / 2)
                    )

                    pyxel.play(1, 1)

                    self.score += 10

        for enemy in enemy_list:
            if (
                self.player.x + self.player.w > enemy.x
                and enemy.x + enemy.w > self.player.x
                and self.player.y + self.player.h > enemy.y
                and enemy.y + enemy.h > self.player.y
            ):
                enemy.alive = False

                # 自機の爆発を生成する
                blast_list.append(
                    Blast(
                        self.player.x + PLAYER_WIDTH / 2,
                        self.player.y + PLAYER_HEIGHT / 2,
                    )
                )

                pyxel.play(1, 1)

                self.scene = SCENE_GAMEOVER

        self.player.update()
        update_list(bullet_list)
        update_list(enemy_list)
        update_list(blast_list)

        cleanup_list(enemy_list)
        cleanup_list(bullet_list)
        cleanup_list(blast_list)

    def update_gameover_scene(self):
        update_list(bullet_list)
        update_list(enemy_list)
        update_list(blast_list)

        cleanup_list(enemy_list)
        cleanup_list(bullet_list)
        cleanup_list(blast_list)

        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY
            self.player.x = pyxel.width / 2
            self.player.y = pyxel.height - 20
            self.score = 0

            enemy_list.clear()
            bullet_list.clear()
            blast_list.clear()

    def draw(self):
        pyxel.cls(0)

        self.background.draw()

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

        pyxel.text(79, 4, "SCORE {:5}".format(self.score), 7)

    def draw_title_scene(self):
        pyxel.text(75, 101, "Pyxel Shooter", pyxel.frame_count % 16)
        pyxel.text(71, 181, "- PRESS ENTER -", 13)
        pyxel.text(56, 201, "- PRESS C CORONAMODE -", 13)


    def draw_play_scene(self):
        self.player.draw()
        draw_list(bullet_list)
        draw_list(enemy_list)
        draw_list(blast_list)

    def draw_gameover_scene(self):
        draw_list(bullet_list)
        draw_list(enemy_list)
        draw_list(blast_list)

        pyxel.text(83, 101, "GAME OVER", 8)
        pyxel.text(71, 181, "- PRESS ENTER -", 13)        


# filename = 'sound.mp3' #再生したいmp3ファイル
# pygame.mixer.init()
# pygame.mixer.music.load(filename) #音源を読み込み
# mp3_length = mp3(filename).info.length #音源の長さ取得
# pygame.mixer.music.play(1) #再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)

musicPlayer = MusicPlayer("sound.ogg")

App()
