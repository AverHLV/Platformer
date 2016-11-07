"""
This module describes the behavior of moving objects
"""

import blocks
from pygame import sprite, image, time, Surface, Color, Rect
from pyganim import PygAnimation
from timeit import default_timer
from find_file import get_path

COLOR = "#000000"
MOVE_SPEED = 5
JUMP_POWER = 10
GRAVITY = 0.5
WIDTH = 22
HEIGHT = 32

RES_PATH = ['resources', 'hero']
ANIMATION_DELAY = 100
ANIMATION_STAY_RIGHT = [(get_path([RES_PATH[0], RES_PATH[1], 'sr.png']), ANIMATION_DELAY)]
ANIMATION_STAY_LEFT = [(get_path([RES_PATH[0], RES_PATH[1], 'sl.png']), ANIMATION_DELAY)]

ANIMATION_JUMP_STAY_RIGHT = [(get_path([RES_PATH[0], RES_PATH[1], 'jsr.png']), ANIMATION_DELAY)]
ANIMATION_JUMP_STAY_LEFT = [(get_path([RES_PATH[0], RES_PATH[1], 'jsl.png']), ANIMATION_DELAY)]
ANIMATION_JUMP_LEFT = [(get_path([RES_PATH[0], RES_PATH[1], 'jl.png']), ANIMATION_DELAY)]
ANIMATION_JUMP_RIGHT = [(get_path([RES_PATH[0], RES_PATH[1], 'jr.png']), ANIMATION_DELAY)]

ANIMATION_RIGHT = [(get_path([RES_PATH[0], RES_PATH[1], 'r1.png']), ANIMATION_DELAY),
                   (get_path([RES_PATH[0], RES_PATH[1], 'r2.png']), ANIMATION_DELAY),
                   (get_path([RES_PATH[0], RES_PATH[1], 'r3.png']), ANIMATION_DELAY),
                   (get_path([RES_PATH[0], RES_PATH[1], 'r4.png']), ANIMATION_DELAY)]

ANIMATION_LEFT = [(get_path([RES_PATH[0], RES_PATH[1], 'l1.png']), ANIMATION_DELAY),
                  (get_path([RES_PATH[0], RES_PATH[1], 'l2.png']), ANIMATION_DELAY),
                  (get_path([RES_PATH[0], RES_PATH[1], 'l3.png']), ANIMATION_DELAY),
                  (get_path([RES_PATH[0], RES_PATH[1], 'l4.png']), ANIMATION_DELAY)]

ANIMATION_DELAY = 300
ANIMATION_DIE = [(get_path([RES_PATH[0], RES_PATH[1], 'd1.png']), ANIMATION_DELAY),
                 (get_path([RES_PATH[0], RES_PATH[1], 'd2.png']), ANIMATION_DELAY),
                 (get_path([RES_PATH[0], RES_PATH[1], 'd3.png']), ANIMATION_DELAY),
                 (get_path([RES_PATH[0], RES_PATH[1], 'd4.png']), ANIMATION_DELAY),
                 (get_path([RES_PATH[0], RES_PATH[1], 'd5.png']), ANIMATION_DELAY)]

MONSTER_WIDTH = 32
RES_PATH = ['resources', 'enemies']

MONSTER_RIGHT = [(get_path([RES_PATH[0], RES_PATH[1], 'm_r1.png']), ANIMATION_DELAY),
                 (get_path([RES_PATH[0], RES_PATH[1], 'm_r2.png']), ANIMATION_DELAY)]

MONSTER_LEFT = [(get_path([RES_PATH[0], RES_PATH[1], 'm_l1.png']), ANIMATION_DELAY),
                (get_path([RES_PATH[0], RES_PATH[1], 'm_l2.png']), ANIMATION_DELAY)]

ANIMATION_DELAY = 200
ANGRY_MONSTER_STAY = [(get_path([RES_PATH[0], RES_PATH[1], 'a_m_s.png']), ANIMATION_DELAY)]

ANGRY_MONSTER_RIGHT = [(get_path([RES_PATH[0], RES_PATH[1], 'a_m_r1.png']), ANIMATION_DELAY),
                       (get_path([RES_PATH[0], RES_PATH[1], 'a_m_r2.png']), ANIMATION_DELAY),
                       (get_path([RES_PATH[0], RES_PATH[1], 'a_m_r3.png']), ANIMATION_DELAY)]

ANGRY_MONSTER_LEFT = [(get_path([RES_PATH[0], RES_PATH[1], 'a_m_l1.png']), ANIMATION_DELAY),
                      (get_path([RES_PATH[0], RES_PATH[1], 'a_m_l2.png']), ANIMATION_DELAY),
                      (get_path([RES_PATH[0], RES_PATH[1], 'a_m_l3.png']), ANIMATION_DELAY)]

ANIMATION_DELAY = 300
ANGRY_MONSTER_DIE = [(get_path([RES_PATH[0], RES_PATH[1], 'a_m_d1.png']), ANIMATION_DELAY),
                     (get_path([RES_PATH[0], RES_PATH[1], 'a_m_d2.png']), ANIMATION_DELAY),
                     (get_path([RES_PATH[0], RES_PATH[1], 'a_m_d3.png']), ANIMATION_DELAY),
                     (get_path([RES_PATH[0], RES_PATH[1], 'a_m_d3.png']), ANIMATION_DELAY)]

ANIMATION_DELAY = 100
SHOOTING_MONSTER_STAY_RIGHT = [(get_path([RES_PATH[0], RES_PATH[1], 's_m_sr.png']), ANIMATION_DELAY)]
SHOOTING_MONSTER_STAY_LEFT = [(get_path([RES_PATH[0], RES_PATH[1], 's_m_sl.png']), ANIMATION_DELAY)]

SHOOTING_MONSTER_RIGHT = [(get_path([RES_PATH[0], RES_PATH[1], 's_m_r1.png']), ANIMATION_DELAY),
                          (get_path([RES_PATH[0], RES_PATH[1], 's_m_r2.png']), ANIMATION_DELAY),
                          (get_path([RES_PATH[0], RES_PATH[1], 's_m_r3.png']), ANIMATION_DELAY)]

SHOOTING_MONSTER_LEFT = [(get_path([RES_PATH[0], RES_PATH[1], 's_m_l1.png']), ANIMATION_DELAY),
                         (get_path([RES_PATH[0], RES_PATH[1], 's_m_l2.png']), ANIMATION_DELAY),
                         (get_path([RES_PATH[0], RES_PATH[1], 's_m_l3.png']), ANIMATION_DELAY)]

ANIMATION_DELAY = 300
SHOOTING_MONSTER_DIE = [(get_path([RES_PATH[0], RES_PATH[1], 's_m_d1.png']), ANIMATION_DELAY),
                        (get_path([RES_PATH[0], RES_PATH[1], 's_m_d2.png']), ANIMATION_DELAY),
                        (get_path([RES_PATH[0], RES_PATH[1], 's_m_d3.png']), ANIMATION_DELAY),
                        (get_path([RES_PATH[0], RES_PATH[1], 's_m_d4.png']), ANIMATION_DELAY)]


class Hero(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # physical variables
        self.speed_x = 0
        self.speed_y = 0
        self.startX = x
        self.startY = y
        self.score = 0
        self.difference = 0
        self.direction = 1
        self.deaths = 0
        self.health = 100
        self.jump_power = JUMP_POWER

        # flags
        self.start = None
        self.played = False
        self.on_ground = False
        self.respawn = False
        self.winner = False
        self.key = False

        # images and animation
        self.image = Surface((WIDTH, HEIGHT))
        self.image.set_colorkey(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.a_timer = AnimationTimer()

        self.an_right = PygAnimation(ANIMATION_RIGHT)
        self.an_right.play()

        self.an_left = PygAnimation(ANIMATION_LEFT)
        self.an_left.play()

        self.an_stay_right = PygAnimation(ANIMATION_STAY_RIGHT)
        self.an_stay_right.play()

        self.an_stay_left = PygAnimation(ANIMATION_STAY_LEFT)
        self.an_stay_left.play()

        self.an_jump_stay_right = PygAnimation(ANIMATION_JUMP_STAY_RIGHT)
        self.an_jump_stay_right.play()

        self.an_jump_stay_left = PygAnimation(ANIMATION_JUMP_STAY_LEFT)
        self.an_jump_stay_left.play()

        self.an_jump_left = PygAnimation(ANIMATION_JUMP_LEFT)
        self.an_jump_left.play()

        self.an_jump_right = PygAnimation(ANIMATION_JUMP_RIGHT)
        self.an_jump_right.play()

        self.an_die = PygAnimation(ANIMATION_DIE)
        self.an_die.play()

    def update(self, left, right, up, platforms, entities, sound):
        """
        This method updates player state on the screen

        :param left: bool
        :param right: bool
        :param up: bool
        :param platforms: list
        :param entities: sprites group
        :param sound: Sound object
        :return: None
        """

        if self.health <= 0:
            if not self.played:
                sound.play(4, loops=0)
                self.played = True
                self.a_timer.start_timer()

            if self.a_timer.get_timer() >= 0.4:
                self.die(platforms, entities)
            else:
                self.image.fill(Color(COLOR))
                self.an_die.blit(self.image, (0, 0))

        else:
            self.update_jump_power(up)

            if left:
                self.speed_x = - MOVE_SPEED
                self.image.fill(Color(COLOR))

                if up:
                    self.an_jump_left.blit(self.image, (0, 0))
                else:
                    self.an_left.blit(self.image, (0, 0))

            if right:
                self.speed_x = MOVE_SPEED
                self.image.fill(Color(COLOR))

                if up:
                    self.an_jump_right.blit(self.image, (0, 0))
                else:
                    self.an_right.blit(self.image, (0, 0))

            if not (left or right):
                if self.speed_x:
                    self.direction = self.speed_x

                self.speed_x = 0

                if not up:
                    self.image.fill(Color(COLOR))

                    if self.direction > 0:
                        self.an_stay_right.blit(self.image, (0, 0))
                    else:
                        self.an_stay_left.blit(self.image, (0, 0))

            if up and self.on_ground:
                self.speed_y = - self.jump_power
                self.image.fill(Color(COLOR))

                if self.direction > 0:
                    self.an_jump_stay_right.blit(self.image, (0, 0))
                else:
                    self.an_jump_stay_left.blit(self.image, (0, 0))

            if not self.on_ground:
                self.speed_y += GRAVITY

            self.on_ground = False
            self.rect.y += self.speed_y
            self.collide(0, self.speed_y, platforms)
            self.rect.x += self.speed_x
            self.collide(self.speed_x, 0, platforms)

    def collide(self, speed_x, speed_y, platforms):
        """
        Checking collision

        :param speed_x: horizontal speed
        :param speed_y: vertical speed
        :param platforms: list
        :return: None
        """

        for platform in platforms:
            if sprite.collide_rect(self, platform) and \
                    self is not platform and not isinstance(platform, blocks.BlockStop):
                if self.special_block(platform):
                    if (isinstance(platform, AngryMonster) or isinstance(platform, ShootingMonster)) and \
                            platform.health > 0:
                        self.health = 0

                    elif isinstance(platform, blocks.BlockDie) or \
                            (isinstance(platform, Monster) and not platform.descendant):
                        self.health = 0

                    elif isinstance(platform, blocks.Bonfire) and not platform.active:
                        self.startX = platform.rect.x
                        self.startY = platform.rect.y
                        platform.activate()

                    elif isinstance(platform, blocks.BlockBlink):
                        self.blink(platform.go_x, platform.go_y)

                    elif isinstance(platform, blocks.Exit) and self.key:
                        self.winner = True

                    elif isinstance(platform, blocks.Key):
                        self.key = True
                        platform.take()

                    elif isinstance(platform, blocks.Coin):
                        self.score += 1
                        platform.take()
                else:
                    if speed_x > 0:
                        self.rect.right = platform.rect.left
                        self.speed_x = 0

                    if speed_x < 0:
                        self.rect.left = platform.rect.right
                        self.speed_x = 0

                    if speed_y > 0:
                        self.rect.bottom = platform.rect.top
                        self.on_ground = True
                        self.speed_y = 0

                    if speed_y < 0:
                        self.rect.top = platform.rect.bottom
                        self.speed_y = 0

    def update_jump_power(self, up):
        if up and self.on_ground and self.jump_power >= 2.5:
            self.jump_power -= 0.5
        elif self.on_ground and self.jump_power <= JUMP_POWER + 0.1:
            self.jump_power += 0.1

    @staticmethod
    def special_block(platform):
        if isinstance(platform, blocks.BlockDie) or isinstance(platform, Monster) or \
                isinstance(platform, blocks.Bonfire) or isinstance(platform, blocks.BlockBlink) or \
                isinstance(platform, blocks.Coin) or isinstance(platform, blocks.Exit) or \
                isinstance(platform, blocks.Key):
            return True
        return False

    def blink(self, x, y):
        time.wait(400)
        self.rect.x = x
        self.rect.y = y

    def die(self, platforms, entities):
        if self.key:
            self.key = False
            key = blocks.Key(self.rect.x, self.rect.y)

            for entity in entities:
                if isinstance(sprite, blocks.Key):
                    entities.remove(entity)
                    platforms.remove(entity)

            entities.add(key)
            platforms.append(key)

        self.deaths += 1
        self.blink(self.startX, self.startY)
        self.health = 100
        self.an_die.stop()
        self.an_die.play()
        self.respawn = True
        self.played = False

    def start_timer(self):
        self.start = default_timer()

    def pause_timer(self):
        self.difference = default_timer()

    def unpause_timer(self):
        self.difference = default_timer() - self.difference

    def get_timer(self):
        timer = int((default_timer() - self.start) - self.difference)

        if timer > 59:
            if not timer % 60:
                timer = str(int(timer / 60)) + ' m'
            else:
                timer = str(int(timer / 60)) + ' m ' + str(timer % 60) + ' s'
        else:
            timer = str(timer) + ' s'

        return timer


class Monster(sprite.Sprite):
    def __init__(self, x, y, x_speed, y_speed, max_length_left, max_length_up):
        super().__init__()

        # physical constants
        self.startX = x
        self.startY = y
        self.max_length_left = int(max_length_left)
        self.max_length_up = int(max_length_up)
        self.speed_x = int(x_speed)
        self.speed_y = int(y_speed)
        self.descendant = False

        # image and animation
        self.image = Surface((MONSTER_WIDTH, HEIGHT))
        self.image.set_colorkey(Color(COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, HEIGHT)

        self.an_right = PygAnimation(MONSTER_RIGHT)
        self.an_right.play()

        self.an_left = PygAnimation(MONSTER_LEFT)
        self.an_left.play()

    def update(self, platforms):
        self.image.fill(Color(COLOR))

        if self.speed_x < 0:
            self.an_left.blit(self.image, (0, 0))
        else:
            self.an_right.blit(self.image, (0, 0))

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.collide(platforms)

        if abs(self.startX - self.rect.x) > self.max_length_left:
            self.speed_x = - self.speed_x

        if abs(self.startY - self.rect.y) > self.max_length_up:
            self.speed_y = - self.speed_y

    def collide(self, platforms):
        for platform in platforms:
            if sprite.collide_rect(self, platform) and self is not platform and not \
                   (isinstance(platform, blocks.Coin) or isinstance(platform, blocks.Exit) or
                    isinstance(platform, blocks.Key) or isinstance(platform, Monster)):
                self.speed_x = - self.speed_x
                self.speed_y = - self.speed_y


class AngryMonster(Monster):
    def __init__(self, x, y, x_speed, max_length_left):
        super().__init__(x, y, x_speed, 0, max_length_left, 0)

        self.health = 100
        self.direction = self.speed_x
        self.used = False
        self.started = False
        self.tracked = False
        self.descendant = True

        self.image = Surface((MONSTER_WIDTH, HEIGHT))
        self.image.set_colorkey(Color(COLOR))
        self.an_timer = AnimationTimer()

        self.an_stay = PygAnimation(ANGRY_MONSTER_STAY)
        self.an_stay.play()

        self.an_right = PygAnimation(ANGRY_MONSTER_RIGHT)
        self.an_right.play()

        self.an_left = PygAnimation(ANGRY_MONSTER_LEFT)
        self.an_left.play()

        self.an_die = PygAnimation(ANGRY_MONSTER_DIE)
        self.an_die.play()

    def update(self, platforms, hero_x, hero_y):
        if self.health <= 0:

            if not self.started:
                self.an_timer.start_timer()
                self.started = True

            if self.an_timer.get_timer() >= 0.3:
                self.die()
            else:
                self.image.fill(Color(COLOR))
                self.an_die.blit(self.image, (0, 0))

        else:
            if not self.used:
                if self.rect.x + self.max_length_left > hero_x and self.rect.y == hero_y:
                    self.tracked = True

                    if self.speed_x:
                        self.direction = self.speed_x

                    if (hero_x > self.rect.x and self.speed_x < 0) or (self.rect.x > hero_x and self.speed_x > 0):
                        self.speed_x = - self.speed_x
                else:
                    self.tracked = False

                self.image.fill(Color(COLOR))

                if self.speed_x > 0:
                    self.an_right.blit(self.image, (0, 0))

                elif self.speed_x < 0:
                    self.an_left.blit(self.image, (0, 0))

                else:
                    self.an_stay.blit(self.image, (0, 0))

                self.rect.x += self.speed_x
                self.collide(platforms)

    def collide(self, platforms):
        for platform in platforms:
            if sprite.collide_rect(self, platform) and not \
                   (isinstance(platform, Monster) or isinstance(platform, AngryMonster) or
                    isinstance(platform, blocks.Coin) or
                    isinstance(platform, blocks.Exit) or isinstance(platform, blocks.Key) or
                    isinstance(platform, ShootingMonster)):

                if self.tracked:
                    self.speed_x = 0
                else:
                    if self.speed_x < 0:
                        self.rect.left = platform.rect.right

                        if self.direction > 0:
                            self.speed_x = self.direction
                        else:
                            self.speed_x = - self.direction

                    elif self.speed_x > 0:
                        self.rect.right = platform.rect.left

                        if self.direction < 0:
                            self.speed_x = self.direction
                        else:
                            self.speed_x = - self.direction

                    else:
                        if platform.rect.x > self.rect.x:
                            self.rect.right = platform.rect.left

                            if self.direction > 0:
                                self.speed_x = - self.direction
                            else:
                                self.speed_x = self.direction

                        else:
                            self.rect.left = platform.rect.right

                            if self.direction > 0:
                                self.speed_x = self.direction
                            else:
                                self.speed_x = - self.direction

    def die(self):
        self.image = image.load(get_path([RES_PATH[0], RES_PATH[1], 'a_m_d4.png'])).convert_alpha()
        self.used = True


class ShootingMonster(Monster):
    def __init__(self, x, y, x_speed, max_length_left):
        super().__init__(x, y, x_speed, 0, max_length_left, 0)
        self.radius = 400
        self.health = 100
        self.used = False
        self.started = False
        self.tracked = False
        self.descendant = True
        self.frequency = 0
        self.image = Surface((MONSTER_WIDTH, HEIGHT))
        self.image.set_colorkey(Color(COLOR))
        self.an_timer = AnimationTimer()

        self.an_stay_right = PygAnimation(SHOOTING_MONSTER_STAY_RIGHT)
        self.an_stay_right.play()

        self.an_stay_left = PygAnimation(SHOOTING_MONSTER_STAY_LEFT)
        self.an_stay_left.play()

        self.an_right = PygAnimation(SHOOTING_MONSTER_RIGHT)
        self.an_right.play()

        self.an_left = PygAnimation(SHOOTING_MONSTER_LEFT)
        self.an_left.play()

        self.an_die = PygAnimation(SHOOTING_MONSTER_DIE)
        self.an_die.play()

    def update(self, platforms, hero_x, hero_y, entities, bullets):
        if self.health <= 0:
            if not self.started:
                self.an_timer.start_timer()
                self.started = True

            if self.an_timer.get_timer() >= 0.3:
                self.die()
            else:
                self.image.fill(Color(COLOR))
                self.an_die.blit(self.image, (0, 0))

        else:
            self.frequency += 1

            if not self.used:
                self.image.fill(Color(COLOR))

                if self.rect.x + self.radius > hero_x and self.rect.y == hero_y:
                    if self.rect.x < hero_x:
                        self.an_stay_right.blit(self.image, (0, 0))
                    else:
                        self.an_stay_left.blit(self.image, (0, 0))

                    self.tracked = True
                else:
                    self.tracked = False

                if self.tracked and self.frequency % 20 == 0:
                    if hero_x < self.rect.x:
                        bl = blocks.Bullet(self.rect.x, self.rect.y + 10, right=False, by_monster=True)
                    else:
                        bl = blocks.Bullet(self.rect.x + 25, self.rect.y + 10, by_monster=True)

                    entities.add(bl)
                    bullets.add(bl)

                elif not self.tracked:
                    if self.speed_x > 0:
                        self.an_right.blit(self.image, (0, 0))

                    elif self.speed_x < 0:
                        self.an_left.blit(self.image, (0, 0))

                    self.rect.x += self.speed_x
                    self.collide(platforms)

                    if abs(self.startX - self.rect.x) > self.max_length_left:
                        self.speed_x = - self.speed_x

    def die(self):
        self.image = image.load(get_path([RES_PATH[0], RES_PATH[1], 's_m_d4.png'])).convert_alpha()
        self.used = True


class AnimationTimer(object):
    def __init__(self):
        self.start = None

    def start_timer(self):
        self.start = default_timer()

    def get_timer(self):
        return default_timer() - self.start
