"""
SuperDooMGuy main module

Developed by Aver (c)
(just for fun)

Small platformer with tiled graphics, powered by pygame
Inspired by SuperMeatBoy and DooM
"""

import pygame
import actors
import blocks
import interaction
from pytmx.util_pygame import load_pygame
from os import getcwd, listdir
from find_file import get_path
from logging import basicConfig, critical, DEBUG

# logging configuration
basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s', level=DEBUG,
            filename='SuperDooMGuy.log')


def load_level(filename):
    """
    Loading .tmx files

    :param filename: str
    :return: groups of sprites
    """

    hero = None
    level = load_pygame(filename)

    # creating groups of sprites
    main_group = pygame.sprite.Group()
    background = pygame.sprite.Group()
    animated_group = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    scores = pygame.sprite.Group()
    angry_enemies = pygame.sprite.Group()
    angry_group = pygame.sprite.Group()
    shooting_enemies = pygame.sprite.Group()
    objects = []

    '''
    TMX files structure:

    1. Layers of tiles:
        Background - tiles of background, interact with nothing
        Platforms - tiles of platforms, ground and walls
        BlockDie - traps

    2. Layers of objects:
        Objects - special tiles with unique mechanics
    '''

    for layer in level.visible_layers:
        if layer.name == 'Background':
            for x, y, image in layer.tiles():
                bg = blocks.Background(x * blocks.PLATFORM_WIDTH, y * blocks.PLATFORM_HEIGHT, image)
                background.add(bg)

        if layer.name == 'Platforms':
            for x, y, image in layer.tiles():
                pf = blocks.Platform(x * blocks.PLATFORM_WIDTH, y * blocks.PLATFORM_HEIGHT, image.convert_alpha())
                main_group.add(pf)
                objects.append(pf)

        if layer.name == 'BlockDie':
            for x, y, image in layer.tiles():
                bd = blocks.BlockDie(x * blocks.PLATFORM_WIDTH, y * blocks.PLATFORM_HEIGHT)
                main_group.add(bd)
                objects.append(bd)

        if layer.name == 'Objects':
            for obj in layer:
                if obj.name == 'Monster':
                    mn = actors.Monster(obj.x, obj.y, obj.properties['x_speed'], obj.properties['y_speed'],
                                        obj.properties['max_length_left'], obj.properties['max_length_up'])
                    main_group.add(mn)
                    objects.append(mn)
                    enemies.add(mn)

                if obj.name == 'Hero':
                    hero = actors.Hero(obj.x, obj.y)
                    objects.append(hero)

                if obj.name == 'Exit':
                    e = blocks.Exit(obj.x, obj.y)
                    main_group.add(e)
                    objects.append(e)

                if obj.name == 'Key':
                    key = blocks.Key(obj.x, obj.y)
                    main_group.add(key)
                    objects.append(key)

                if obj.name == 'Bonfire':
                    bonfire = blocks.Bonfire(obj.x, obj.y)
                    main_group.add(bonfire)
                    objects.append(bonfire)

                if obj.name == 'Coin':
                    coin = blocks.Coin(obj.x, obj.y)
                    main_group.add(coin)
                    scores.add(coin)
                    objects.append(coin)

                if obj.name == 'BlockStop':
                    stop = blocks.BlockStop(obj.x, obj.y)
                    objects.append(stop)

                if obj.name == 'AngryMonster':
                    a_mn = actors.AngryMonster(obj.x, obj.y, obj.properties['x_speed'],
                                               obj.properties['max_length_left'])
                    angry_group.add(a_mn)
                    objects.append(a_mn)
                    angry_enemies.add(a_mn)

                if obj.name == 'ShootingMonster':
                    s_mn = actors.ShootingMonster(obj.x, obj.y, obj.properties['x_speed'],
                                                  obj.properties['max_length_left'])
                    angry_group.add(s_mn)
                    objects.append(s_mn)
                    shooting_enemies.add(s_mn)

                if obj.name == 'BlockBlink':
                    tp = blocks.BlockBlink(obj.x, obj.y, obj.properties['go_x'], obj.properties['go_y'])
                    main_group.add(tp)
                    objects.append(tp)

    return main_group, animated_group, enemies, scores, angry_enemies, objects, hero, angry_group, \
        shooting_enemies, level, background


def set_used(sprite_group):
    for sprite in sprite_group:
        sprite.used = True


def objects_append(platforms, sprite_group):
    for sprite in sprite_group:
        platforms.append(sprite)


def clean_groups(group_1, group_2):
    for sprite in group_2:
        if sprite.used:
            group_1.remove(sprite)
            group_2.remove(sprite)


def draw_group(screen, group, camera):
    for sprite in group:
        screen.blit(sprite.image, camera.apply(sprite))


def shot(entities, bullets, bl, sound):
    sound.play(1, loops=0)
    bullets.add(bl)
    entities.add(bl)


def main(caption):
    """
    Main function with game cycle

    :param caption: game name (str)
    :return: None
    """

    pygame.init()

    # creating and setting window parameters
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h),
                                     pygame.FULLSCREEN | pygame.RESIZABLE)
    pygame.display.set_caption(caption)

    bullets = pygame.sprite.Group()
    sound = interaction.Sound()
    timer = pygame.time.Clock()

    # creating game menu
    menu = interaction.Menu(caption, screen)
    inscription = pygame.font.Font(get_path(['resources', 'font', 'main.ttf']), 12)
    key = pygame.image.load(get_path(['resources', 'blocks', 'key.png'])).convert_alpha()
    sound.play(0)
    n_map = 0

    # getting number of levels
    for file in listdir(getcwd() + '/resources/levels'):
        if '.tmx' in file:
            n_map += 1

    while True:
        menu.render_menu(screen)
        save = menu.load_game()

        for lvl in range(save, n_map + 1):
            left, right, up = False, False, False
            pygame.mouse.set_visible(False)

            bg = pygame.image.load(get_path(['resources', 'levels', 'back_' + str(lvl) + '.png'])).convert()
            bg = pygame.transform.scale(bg, (screen_info.current_w, screen_info.current_h))

            entities, animated_entities, monsters, coins, \
                angry_monsters, platforms, player, angry_entities, shooting_monsters, \
                level, back = load_level(get_path(['resources', 'levels', 'map_' + str(lvl) + '.tmx']))

            total_level_width = level.width * level.tilewidth
            total_level_height = level.height * level.tileheight

            # creating camera
            camera = interaction.Camera(total_level_width, total_level_height, screen_info.current_w,
                                        screen_info.current_h)

            total_monsters = len(angry_monsters)
            total_coins = len(coins)
            player.start_timer()

            while not player.winner:
                # fps lock
                timer.tick(60)

                screen.blit(bg, (0, 0))
                camera.set_resolution(menu.render_size)

                for event in pygame.event.get():
                    # pause
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.mouse.set_visible(True)
                        player.pause_timer()
                        menu.render_menu(screen, ingame=True)
                        player.unpause_timer()
                        pygame.mouse.set_visible(False)

                    # shooting
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and player.health > 0:
                        if not player.speed_x and not left and not right:
                            if player.direction < 0:
                                bl = blocks.Bullet(player.rect.x, player.rect.y + 10, right=False)
                                shot(entities, bullets, bl, sound)

                            else:
                                bl = blocks.Bullet(player.rect.x + 18, player.rect.y + 10)
                                shot(entities, bullets, bl, sound)
                        else:
                            if player.speed_x < 0:
                                bl = blocks.Bullet(player.rect.x, player.rect.y + 10, right=False)
                                shot(entities, bullets, bl, sound)

                            elif player.speed_x > 0:
                                bl = blocks.Bullet(player.rect.x + 18, player.rect.y + 10)
                                shot(entities, bullets, bl, sound)

                    # moving
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            left = True

                        if event.key == pygame.K_d:
                            right = True

                        if event.key == pygame.K_w:
                            up = True
                            sound.play(2, loops=0)

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            left = False

                        if event.key == pygame.K_d:
                            right = False

                        if event.key == pygame.K_w:
                            up = False

                if player.respawn:
                    set_used(angry_monsters)
                    set_used(shooting_monsters)

                clean_groups(entities, coins)
                clean_groups(entities, bullets)
                clean_groups(platforms, angry_monsters)
                clean_groups(platforms, shooting_monsters)

                if player.respawn:
                    # reload level
                    _, _, _, _, angry_monsters, _, _, angry_entities, \
                        shooting_monsters, \
                        _, _ = load_level(get_path(['resources', 'levels', 'map_' + str(lvl) + '.tmx']))
                    player.respawn = False

                    objects_append(platforms, angry_monsters)
                    objects_append(platforms, shooting_monsters)

                # updating sprite groups
                animated_entities.update()
                monsters.update(platforms)
                angry_monsters.update(platforms, player.rect.x, player.rect.y)
                shooting_monsters.update(platforms, player.rect.x, player.rect.y, entities, bullets)
                coins.update()
                bullets.update(platforms)
                player.update(left, right, up, platforms, entities, sound)
                camera.update(player.rect)

                # drawing sprites
                draw_group(screen, back, camera)
                draw_group(screen, entities, camera)
                draw_group(screen, angry_entities, camera)
                screen.blit(player.image, camera.apply(player))
                screen.blit(inscription.render('Health  ' + str(player.health) + '%', 1, (0, 0, 0)), (20, 30))
                screen.blit(inscription.render('Score  ' + str(player.score), 1, (0, 0, 0)), (140, 30))

                if int(player.jump_power) < actors.JUMP_POWER - 2:
                    screen.blit(inscription.render(str(int(player.jump_power)), 1, (0, 0, 0)),
                                (player.rect.x + camera.state.x, player.rect.y + camera.state.y - 30))

                if player.key:
                    screen.blit(key, (230, 20))
                else:
                    screen.blit(inscription.render('No key', 1, (0, 0, 0)), (230, 30))

                if menu.show_fps:
                    screen.blit(inscription.render(str(int(timer.get_fps())), 1, (0, 0, 0)),
                                (menu.render_size[0] - 30, 30))

                pygame.display.update()

                # make screen shot
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    menu.make_shot()

            results = [['Level passed!', ((menu.render_size[0] / 2) - 150, 50)],
                       ['Game Saved', ((menu.render_size[0] / 2) - 150, 150)],
                       ['Time: ' + player.get_timer(), (100, 250)],
                       ['Score: ' + str(player.score) + '/' + str(total_coins), (100, 300)],
                       ['Monsters killed: ' + str(total_monsters - len(angry_monsters)) + '/' + str(total_monsters),
                        (100, 350)],
                       ['Deaths: ' + str(player.deaths), (100, 400)]]

            if lvl == n_map:
                results[0][0] = 'Game passed!'
                results[1][0] = 'Well done!'
        
            pygame.mouse.set_visible(True)
            sound.play(3, loops=0)

            if lvl + 1 <= n_map:
                menu.save_game(lvl + 1)
            else:
                menu.save_game(lvl)

            menu.render_results(screen, results)

try:
    main('SuperDooMGuy')
except Exception as ex:
    critical(ex)
