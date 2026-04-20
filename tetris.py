import pygame
from random import choice
from copy import deepcopy
import random
x_size, y_size = 10, 20
ppb = 45
game_res = x_size * ppb, y_size * ppb
fps = 60

pygame.init()
game_sc = pygame.display.set_mode(game_res)
clock = pygame.time.Clock()
pygame.display.set_caption("TETRIS")

grid = [pygame.Rect(x * ppb, y * ppb, ppb, ppb) for x in range(x_size) for y in range(y_size)]

field = [[0 for i in range(x_size)] for j in range(y_size)]

white = pygame.Color(255, 255, 255)

figures_pos = [
    [(0, 0), (-1, 0), (-2, 0),  (1, 0)],
    [(0, 0), (0, -1), (-1, -1), (-1, 0)],
    [(-1, 0), (-1, 1), (0, 0), (0, -1)], 
    [(0, 0), (-1, 0), (0, 1), (-1, -1)], 
    [(0, 0), (0, -1), (0, 1), (-1, -1)],
    [(0, 0), (0, -1), (0, 1), (1, -1)],
    [(0, 0), (0, -1), (0,1), (-1, 0)]
]
figures = [[pygame.Rect(x + x_size // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, ppb -2, ppb - 2)

figure = deepcopy(choice(figures))

score = 0

def check_borders():
    if figure[i].x < 0 or figure[i].x > (x_size - 1):
        return False
    elif figure[i].y > (y_size - 1) or field[figure[i].y][figure[i].x]:
        return False
    return True

def game_over():
    my_font = pygame.font.SysFont("time new roman", 50)
    game_over_surface = my_font.render("Your score was : " + str(round(score)), True , white)
    game_over_rect = game_over_surface.get_rect()
    game_sc.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    pygame.time.wait(5000)
    pygame.quit()

def show_score():
    score_font = pygame.font.SysFont("time new roman", 30)
    score_surface = score_font.render("Score : " + str(round(score)), True, white)
    game_sc.blit(score_surface, [x, 5])
    pygame.display.flip()

anim_count, anim_speed, anim_limit = 0, 60, 2000
change_color = False
color = 'white'
rot = 0

while True:
    if change_color:    
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        change_color = False

    dx, rotate = 0, False
    game_sc.fill(pygame.Color(0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx -= 1
            if event.key == pygame.K_RIGHT:
                dx += 1
            if event.key == pygame.K_DOWN:
                anim_limit = 100
            if event.key == pygame.K_UP:
                rotate = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                anim_limit = 2000
    #rotation
    center = figure[0]
    old_figure = deepcopy(figure)
    if rotate:
        rotate = False
        for i in range(4):
            difference_x = center.x - figure[i].x
            difference_y = center.y - figure[i].y
            x = figure[i].x
            y = figure[i].y
            if i == 0:
                pass
            elif abs(difference_x) + abs(difference_y) == 1:
                if difference_x > 0:
                        figure[i].y -= 1
                        figure[i].x += 1
                elif difference_x == 0:
                    if difference_y >0:
                        figure[i].y += 1 
                        figure[i].x += 1
                    else:
                        figure[i].y -= 1
                        figure[i].x -= 1
                else:
                    figure[i].y += 1
                    figure[i].x -= 1
                if not check_borders():
                    figure = old_figure
                    break
            elif abs(difference_x) == 2 or abs(difference_y) == 2:
                if abs(difference_x) or abs(difference_y) == 2:
                    if difference_x > 0:
                        figure[i].y -= 2
                        figure[i].x += 2
                    elif difference_x == 0:
                        if difference_y >0:
                            figure[i].y += 2 
                            figure[i].x += 2
                        else:
                            figure[i].y -= 2
                            figure[i].x -= 2
                    else:
                        figure[i].y += 2
                        figure[i].x -= 2
                    if not check_borders():
                        figure = old_figure
                        break
            elif abs(difference_x) == 1 and abs(difference_y) == 1:
                if difference_x > 0:
                    if difference_y > 0:
                        figure[i].x += 2
                    else:
                        figure[i].y -= 2
                else:
                    if difference_y > 0:
                        figure[i].y += 2
                    else:
                        figure[i].x -= 2
                if not check_borders():
                    figure = old_figure
                    break
    
    """
    for i in range(4):
    x = figure[i].y - center.y
    y = figure[i].x - center.x
    figure[i].x = center.x - x
    figure[i].y = center.y - y
    if not check_borders():
        figure = old_figure
        break
    """
    # move x
    old_figure = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = old_figure
            break

    #move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        old_figure = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[old_figure[i].y][old_figure[i].x] = pygame.Color(color)
                figure = deepcopy(choice(figures))
                anim_limit = 2000
                change_color = True
                score += 1
                break
    #check lines
    line = y_size - 1
    for row in range(y_size-1, -1, -1):
        count = 0
        for i in range(x_size):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < x_size:
            line -= 1
        else:
            score += 10
    #draw a grid
    [pygame.draw.rect(game_sc, (40, 40, 40), (i_rect), 1) for i_rect in grid]

    #draw a figure
    for i in range(4):
        figure_rect.x = figure[i].x * ppb
        figure_rect.y = figure[i].y *ppb
        pygame.draw.rect(game_sc, pygame.Color(color), figure_rect)

    #draw blocks
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y, = x *ppb, y*ppb
                pygame.draw.rect(game_sc, col, figure_rect)

    if pygame.Color(color)  in field[0]:
        game_over()
    
    show_score()
    pygame.display.flip()
    clock.tick(fps)
