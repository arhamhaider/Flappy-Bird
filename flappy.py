import random
import sys
import pygame
from pygame.locals import *

window_width = 600
window_height = 499
window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
framepersecond = 32

pipe_image = pygame.image.load('images/pipe.png')
background_image = pygame.image.load('images/background.jpg')
bird_player_image = pygame.image.load('images/bird.png')
sealevel_image = pygame.image.load('images/base.jfif')

def flappy_game():
    your_score = 0
    horizontal = int(window_width / 5)
    vertical = int(window_width / 2)
    ground = 0
    my_temp_height = 100

    first_pipe = create_pipe()
    second_pipe = create_pipe()

    down_pipes = [{'x': window_width + 300 - my_temp_height, 'y': first_pipe[1]['y']},
                  {'x': window_width + 300 - my_temp_height + (window_width / 2), 'y': second_pipe[1]['y']}]

    up_pipes = [{'x': window_width + 300 - my_temp_height, 'y': first_pipe[0]['y']},
                {'x': window_width + 200 - my_temp_height + (window_width / 2), 'y': second_pipe[0]['y']}]

    pipe_vel_x = -4
    bird_velocity_y = -9
    bird_max_vel_y = 10
    bird_min_vel_y = -8
    bird_acc_y = 1

    bird_flap_velocity = -8
    bird_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True

        game_over = is_game_over(horizontal, vertical, up_pipes, down_pipes)
        if game_over:
            return()

        player_mid_pos = horizontal + game_images['flappybird'].get_width() / 2
        for pipe in up_pipes:
            pipe_mid_pos = pipe['x'] + game_images['pipeimage'][0].get_width() / 2
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
                your_score += 1
                print(f"Your score is {your_score}")

        if bird_velocity_y < bird_max_vel_y and not bird_flapped:
            bird_velocity_y += bird_acc_y

        if bird_flapped:
            bird_flapped = False

        player_height = game_images['flappybird'].get_height()
        vertical = vertical + min(bird_velocity_y, elevation - vertical - player_height)

        for upper_pipe, lower_pipe in zip(up_pipes, down_pipes):
            upper_pipe['x'] += pipe_vel_x
            lower_pipe['x'] += pipe_vel_x

        if 0 < up_pipes[0]['x'] < 5:
            new_pipe = create_pipe()
            up_pipes.append(new_pipe[0])
            down_pipes.append(new_pipe[1])

        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        window.blit(game_images['background'], (0, 0))
        for upper_pipe, lower_pipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0], (upper_pipe['x'], upper_pipe['y']))
            window.blit(game_images['pipeimage'][1], (lower_pipe['x'], lower_pipe['y']))

        window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['flappybird'], (horizontal, vertical))

        display_score(your_score)

        pygame.display.update()
        framepersecond_clock.tick(framepersecond)

def is_game_over(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation - 25 or vertical < 0:
        return True

    for pipe in up_pipes:
        pipe_height = game_images['pipeimage'][0].get_height()
        if vertical < pipe_height + pipe['y'] and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True

    for pipe in down_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y']) and \
                abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True

    return False

def create_pipe():
    offset = window_height / 3
    pipe_height = game_images['pipeimage'][0].get_height()
    y2 = offset + random.randrange(0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))
    pipe_x = window_width + 10
    y1 = pipe_height - y2 + offset
    pipe = [{'x': pipe_x, 'y': -y1}, {'x': pipe_x, 'y': y2}]
    return pipe

def display_score(score):
    numbers = [int(x) for x in list(str(score))]
    width = sum(game_images['scoreimages'][num].get_width() for num in numbers)
    x_offset = (window_width - width) / 1.1

    for num in numbers:
        window.blit(game_images['scoreimages'][num], (x_offset, window_width * 0.02))
        x_offset += game_images['scoreimages'][num].get_width()

if __name__ == "__main__":
    pygame.init()
    framepersecond_clock = pygame.time.Clock()

    pygame.display.set_caption('Flappy Bird Game')

    game_images['scoreimages'] = tuple(pygame.image.load(f'images/{i}.png').convert_alpha() for i in range(10))
    game_images['flappybird'] = bird_player_image.convert_alpha()
    game_images['sea_level'] = sealevel_image.convert_alpha()
    game_images['background'] = background_image.convert_alpha()
    game_images['pipeimage'] = (pygame.transform.rotate(pipe_image.convert_alpha(), 180),
                                pipe_image.convert_alpha())

    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

    while True:
        horizontal = int(window_width / 5)
        vertical = int((window_height - game_images['flappybird'].get_height()) / 2)
        ground = 0

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                flappy_game()
            else:
                window.blit(game_images['background'], (0, 0))
                window.blit(game_images['flappybird'], (horizontal, vertical))
                window.blit(game_images['sea_level'], (ground, elevation))
                pygame.display.update()
                framepersecond_clock.tick(framepersecond)
