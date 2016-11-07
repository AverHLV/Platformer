"""
This module provides blocks logic.
"""

import actors
from pygame import sprite, image, Rect
from pyganim import PygAnimation
from find_file import get_path

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

RES_PATH = ['resources', 'blocks']
ANIMATION_DELAY = 500
ANIMATION_BLINK = [(get_path([RES_PATH[0], RES_PATH[1], 'p1.png']), ANIMATION_DELAY),
                   (get_path([RES_PATH[0], RES_PATH[1], 'p2.png']), ANIMATION_DELAY)]

ANIMATION_COIN = [(get_path([RES_PATH[0], RES_PATH[1], 'coin_1.png']), ANIMATION_DELAY),
                  (get_path([RES_PATH[0], RES_PATH[1], 'coin_2.png']), ANIMATION_DELAY)]


class Background(sprite.Sprite):
    def __init__(self, x, y, surface):
        super().__init__()

        # sprite surface for drawing
        self.image = surface

        # sprite collision rect
        self.rect = Rect(x, y, 0, 0)


class Platform(sprite.Sprite):
    def __init__(self, x, y, surface):
        super().__init__()
        self.image = surface
        self.image.set_colorkey(self.image.get_alpha())
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockStop(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, image.load(get_path([RES_PATH[0], RES_PATH[1], 'stop_block.png'])).convert_alpha())


class BlockDie(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, image.load(get_path([RES_PATH[0], RES_PATH[1], 'die_block.png'])).convert_alpha())


class BlockBlink(Platform):
    def __init__(self, x, y, go_x, go_y):
        super().__init__(x, y, image.load(get_path([RES_PATH[0], RES_PATH[1], 'p1.png'])).convert_alpha())

        # coordinates of teleport
        self.go_x = int(go_x) * PLATFORM_WIDTH
        self.go_y = int(go_y) * PLATFORM_HEIGHT

        self.an = PygAnimation(ANIMATION_BLINK)
        self.an.play()

    def update(self):
        self.image.fill(self.image.get_alpha())
        self.an.blit(self.image, (0, 0))


class Exit(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, image.load(get_path([RES_PATH[0], RES_PATH[1], 'exit.png'])).convert_alpha())


class Key(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, image.load(get_path([RES_PATH[0], RES_PATH[1], 'key.png'])).convert_alpha())

    def take(self):
        self.image.fill(self.image.get_alpha())
        self.rect.x = - 10
        self.rect.y = - 10


class Coin(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, image.load(get_path([RES_PATH[0], RES_PATH[1], 'coin_1.png'])).convert_alpha())
        self.used = False

        self.an = PygAnimation(ANIMATION_COIN)
        self.an.play()

    def update(self):
        self.image.fill(self.image.get_alpha())
        
        if not self.used:
            self.an.blit(self.image, (0, 0))

    def take(self):
        """
        Take coin

        :return: None
        """

        self.rect.x = - 10
        self.rect.y = - 10
        self.used = True


class Bonfire(Platform):
    def __init__(self, x, y):
        super().__init__(x, y, image.load(get_path([RES_PATH[0], RES_PATH[1], 'bonfire.png'])).convert_alpha())
        self.active = False

    def activate(self):
        """
        Activate bonfire, new spawn point

        :return: None
        """

        self.active = True
        self.image = image.load(get_path([RES_PATH[0], RES_PATH[1], 'bonfire_a.png'])).convert_alpha()


class Bullet(sprite.Sprite):
    def __init__(self, x, y, right=True, by_monster=False):
        super().__init__()
        self.right = right

        # shooting not by player
        self.by_monster = by_monster
        
        if self.right:
            self.image = image.load(get_path([RES_PATH[0], RES_PATH[1], 'bullet_r.png'])).convert_alpha()
        else:
            self.image = image.load(get_path([RES_PATH[0], RES_PATH[1], 'bullet_l.png'])).convert_alpha()
        
        self.speed_x = 10
        self.used = False
        self.rect = Rect(x, y, 10, 5)

    def update(self, platforms):
        if self.right:
            self.rect.x += self.speed_x
        else:
            self.rect.x -= self.speed_x
            
        self.collide(platforms)

    def collide(self, platforms):
        """
        Check bullet collision

        :param platforms: list
        :return: None
        """

        for platform in platforms:
            if sprite.collide_rect(self, platform) and not self.used:
                if isinstance(platform, actors.AngryMonster):
                    platform.health -= 20

                if isinstance(platform, actors.ShootingMonster) and not self.by_monster:
                    platform.health -= 30

                if isinstance(platform, actors.Hero):
                    platform.health -= 50

                if not (isinstance(platform, Coin) or isinstance(platform, BlockStop) or
                        isinstance(platform, Exit) or isinstance(platform, Key) or isinstance(platform, Bonfire)):
                    if isinstance(platform, actors.ShootingMonster) and not self.by_monster:
                        self.image.fill(self.image.get_alpha())
                        self.used = True

                    elif not isinstance(platform, actors.ShootingMonster):
                        self.image.fill(self.image.get_alpha())
                        self.used = True
