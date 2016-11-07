"""
This module provides interaction with player like camera, game menu, sound
"""

import sys
from pygame import image, mouse, font, event, mixer, constants, display, Surface, Rect, Color
from pyganim import PygAnimation
from os import getcwd, listdir, mkdir, remove
from timeit import default_timer
from datetime import datetime
from pickle import load, dump
from find_file import get_path

COLOR = "#004400"
VERSION = '1.1'
WINDOW_RES = (1024, 768)

SOUND_LIST = ['main_theme.ogg', 'shot.ogg', 'jump.ogg', 'final_laugh.ogg', 'death_cry.ogg']
MENU_ITEMS = [['New game', (100, 200)], ['Continue', (100, 250)], ['Music: On', (100, 300)],
              ['Windowed: Off', (100, 350)], ['Show fps: Off', (100, 400)], ['Quit', (100, 450)]]
RES_ITEMS = [['Continue', (100, 500)]]


RES_PATH = ['resources']
ANIMATION_DELAY = 100
ANIMATION_D_GUY = [(get_path([RES_PATH[0], 'menu', 'doom_guy.png']), ANIMATION_DELAY),
                   (get_path([RES_PATH[0], 'menu', 'doom_guy_f1.png']), ANIMATION_DELAY),
                   (get_path([RES_PATH[0], 'menu', 'doom_guy_f2.png']), ANIMATION_DELAY)]

ANIMATION_DELAY = 150
ANIMATION_FIRING = [(get_path([RES_PATH[0], 'menu', 'muff1.png']), ANIMATION_DELAY),
                    (get_path([RES_PATH[0], 'menu', 'muff2.png']), ANIMATION_DELAY),
                    (get_path([RES_PATH[0], 'menu', 'muff3.png']), ANIMATION_DELAY)]


class Menu(object):
    """Menu class, drawing and managing menus items"""

    def __init__(self, caption, screen):
        # menu fonts
        font.init()
        self.inscription = font.Font(get_path([RES_PATH[0], 'font', 'main.ttf']), 32)
        self.small_inscription = font.Font(get_path([RES_PATH[0], 'font', 'main.ttf']), 12)

        self.items = MENU_ITEMS
        self.res_items = RES_ITEMS
        self.prev_size = screen.get_size()
        self.render_size = self.prev_size
        self.show_fps = False
        self.windowed = False
        self.caption = caption
        self.path = getcwd()

        # images
        self.bg = Surface(screen.get_size())
        self.bg.fill(Color(COLOR))
        self.powered = image.load(get_path([RES_PATH[0], 'menu', 'p_powered.png'])).convert_alpha()
        self.egg = EasterEgg()
        self.d_guy = Surface((350, 600))
        self.firing = Surface((300, 600))
        self.d_guy.set_colorkey(Color(COLOR))
        self.firing.set_colorkey(Color(COLOR))

        # animations
        self.an_d_guy = PygAnimation(ANIMATION_D_GUY)
        self.an_d_guy.play()

        self.an_f = PygAnimation(ANIMATION_FIRING)
        self.an_f.play()

        if '.sav' not in listdir(self.path):
            self.sav = False
        else:
            self.sav = True

        if 'screenshots' not in listdir(self.path):
            self.screen_dir = False
        else:
            self.screen_dir = True

    def render_item(self, surface, active, item):
        """
        Rendering menus item

        :param surface: pygame surface
        :param active: active or not (bool)
        :param item: items list
        :return: None
        """

        if active:
            surface.blit(self.inscription.render(item[0], 1, (250, 60, 60)), item[1])
        else:
            surface.blit(self.inscription.render(item[0], 1, (0, 0, 0)), item[1])

    @staticmethod
    def check_mouse(item):
        """
        Check mouse position

        :param item: items list with coordinates
        :return: bool
        """

        mp = mouse.get_pos()

        if item[1][0] < mp[0] < item[1][0] + 300 and item[1][1] < mp[1] < item[1][1] + 50:
            return True
        return False

    def render_menu(self, screen, ingame=False):
        """
        Main menu function with menu cycle
        
        :param screen: device for drawing
        :param ingame: main menu or pause (bool)
        :return: None
        """
        
        proceed, sound = True, True
        number = -1
        self.egg.start_timer()

        while proceed:
            screen.blit(self.bg, (0, 0))
            screen.blit(self.powered, (self.render_size[0] - 180, self.render_size[1] - 75))
            screen.blit(self.small_inscription.render('SuperDooMGuy v' + VERSION + '. Developed by Aver (c)', 1,
                                                      (0, 0, 0)), (20, self.render_size[1] - 30))

            if not self.egg.changed and self.egg.get_timer() > 120:
                self.d_guy = self.egg.get_image()
                self.egg.changed = True

            if not self.egg.changed:
                self.d_guy.fill(Color(COLOR))
                self.firing.fill(Color(COLOR))
                self.an_d_guy.blit(self.d_guy, (0, 0))
                self.an_f.blit(self.firing, (0, 0))

            screen.blit(self.d_guy, (self.render_size[0] / 2, self.render_size[1] - 600))

            if not self.egg.changed:
                screen.blit(self.firing, ((self.render_size[0] / 2) - 200, self.render_size[1] - 600))

            for item in self.items:
                if self.check_mouse(item) or self.items.index(item) == number:
                    self.render_item(screen, active=True, item=item)
                    number = self.items.index(item)
                else:
                    self.render_item(screen, active=False, item=item)

            for ev in event.get():
                if ingame and ev.type == constants.KEYDOWN and ev.key == constants.K_ESCAPE:
                    proceed = False

                if ev.type == constants.MOUSEBUTTONDOWN and ev.button == 1 and self.egg.changed:
                    self.egg.check_pos(self.render_size)

                if (ev.type == constants.MOUSEBUTTONDOWN and ev.button == 1 and self.check_mouse(self.items[number])) \
                        or (ev.type == constants.KEYDOWN and ev.key == constants.K_SPACE) and number != -1:
                    if not number and not ingame:
                        if self.sav:
                            remove('.sav')

                        self.sav = False
                        proceed = False

                    if number == 1 and (ingame or self.sav):
                        proceed = False

                    if number == 2:
                        if sound:
                            self.items[2][0] = 'Music: Off'
                            mixer.pause()
                            sound = False
                        else:
                            self.items[2][0] = 'Music: On'
                            mixer.unpause()
                            sound = True

                    if number == 3:
                        if not self.windowed:
                            screen = display.set_mode(WINDOW_RES, constants.RESIZABLE)
                            self.render_size = WINDOW_RES
                            self.items[3][0] = 'Windowed: On'
                            self.windowed = True
                        else:
                            screen = display.set_mode(self.prev_size, constants.FULLSCREEN | constants.RESIZABLE)
                            self.render_size = self.prev_size
                            self.items[3][0] = 'Windowed: Off'
                            self.windowed = False

                    if number == 4:
                        if not self.show_fps:
                            self.items[4][0] = 'Show fps: On'
                            self.show_fps = True
                        else:
                            self.items[4][0] = 'Show fps: Off'
                            self.show_fps = False

                    if number == 5:
                        sys.exit()

                if ev.type == constants.KEYDOWN:
                    if ev.key == constants.K_w and number > 0:
                        number -= 1

                    if ev.key == constants.K_s and number < len(self.items) - 1:
                        number += 1

                    if ev.key == constants.K_f:
                        self.make_shot()

            display.update()

    def render_results(self, screen, results):
        proceed = True
        number = -1

        while proceed:
            screen.blit(self.bg, (0, 0))
            screen.blit(self.powered, (self.render_size[0] - 180, self.render_size[1] - 90))

            for item in results:
                self.render_item(screen, active=False, item=item)

            for item in self.res_items:
                if self.check_mouse(item) or self.res_items.index(item) == number:
                    self.render_item(screen, active=True, item=item)
                    number = self.res_items.index(item)
                else:
                    self.render_item(screen, active=False, item=item)

            for ev in event.get():
                if (ev.type == constants.MOUSEBUTTONDOWN and ev.button == 1 and
                        self.check_mouse(self.res_items[number])) or \
                                (ev.type == constants.KEYDOWN and ev.key == constants.K_SPACE) and number != -1:
                    if not number:
                        proceed = False

                if ev.type == constants.KEYDOWN:
                    if ev.key == constants.K_w and number > 0:
                        number -= 1

                    if ev.key == constants.K_s and number < len(self.res_items) - 1:
                        number += 1

                    if ev.key == constants.K_f:
                        self.make_shot()

            display.update()
    
    def make_shot(self):
        if not self.screen_dir:
            mkdir(self.path + '/screenshots')
            self.screen_dir = True
            
        screen_shot = display.get_surface()
        screen_name = self.caption + '_' + str(datetime.now()).replace(':', '-').replace(' ', '_') + '.png'
        image.save(screen_shot, 'screenshots/' + screen_name)

    def load_game(self):
        """
        Loading number of current map

        :return: number of map (int)
        """

        if not self.sav:
            return 1

        return load(open('.sav', 'rb'))

    @staticmethod
    def save_game(number):
        dump(number, open('.sav', 'wb'))


class Camera(object):
    """Providing camera in game"""

    def __init__(self, width, height, width_n, height_n):
        self.state = Rect(0, 0, width, height)
        self.WIN_WIDTH = width_n
        self.WIN_HEIGHT = height_n

    def update(self, target_rect):
        """
        Updating camera

        :param target_rect: pygame Rect
        :return: None
        """

        l, t, _, _ = target_rect
        _, _, w, h = self.state
        l, t = -l + self.WIN_WIDTH / 2, -t + self.WIN_HEIGHT / 2

        l = min(0, l)
        l = max(-(self.state.width - self.WIN_WIDTH), l)
        t = max(-(self.state.height - self.WIN_HEIGHT), t)
        t = min(0, t)

        self.state = Rect(l, t, w, h)

    def set_resolution(self, render_size):
        self.WIN_WIDTH = render_size[0]
        self.WIN_HEIGHT = render_size[1]

    def apply(self, target):
        """
        Moving camera to target Rect

        :param target: Rect
        :return: new Rect
        """

        return target.rect.move(self.state.topleft)


class Sound(object):
    def __init__(self):
        mixer.init()
        self.themes = [mixer.Sound(get_path([RES_PATH[0], 'sound', name])) for name in SOUND_LIST]

    def play(self, number, loops=-1):
        self.themes[number].play(loops)


class EasterEgg(object):
    """Easter egg in main menu"""

    def __init__(self):
        self.img = image.load(get_path([RES_PATH[0], 'menu', 'egg.png'])).convert_alpha()
        self.voice = mixer.Sound(get_path([RES_PATH[0], 'menu', 'voice.ogg']))
        self.changed = False
        self.start = 0

    def get_image(self):
        return self.img

    def check_pos(self, render_size):
        mp = mouse.get_pos()

        if render_size[0] / 2 < mp[0] < (render_size[0] / 2) + 350 and render_size[1] - 600 < mp[1] < render_size[1]:
            self.voice.play(0)

    def start_timer(self):
        self.start = default_timer()

    def get_timer(self):
        return default_timer() - self.start
