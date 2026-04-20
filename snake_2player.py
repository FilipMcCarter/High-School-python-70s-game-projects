import pygame
import random

snake_speed = 10
snake2_speed = 10

xsize = 720
ysize = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()

pygame.display.set_caption("Duel of Snakes")
game_window = pygame.display.set_mode((xsize, ysize))
                                      
fps = pygame.time.Clock()

s_position = [100, 50]

s_body = [
    [100, 50],
    [90, 50],
    [80, 50],
    [70, 50]
]

s2_position = [200, 150]

s2_body = [
    [200,150],
    [190, 150],
    [180, 150],
    [170, 150]
]

fruit_position = [
    random.randrange(1, (xsize//10)) * 10,
    random.randrange(1, (ysize//10)) * 10
]
fruit_spawn = True

direction = "RIGHT"
change_to = direction

direction_2 = "RIGHT"
change_to_2 = direction_2

score = 0
score_2 = 0

def show_score(x, color, font, size, points, is_death):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score : " + str(points) + " " + str(is_death), True, color)
    game_window.blit(score_surface, [x, 5])
    pygame.display.flip()

def game_over():
    if score > score_2:
        my_font = pygame.font.SysFont("time new roman", 50)
        game_over_surface = my_font.render("The winner is green with score : " + str(score), True , green)
        game_over_rect = game_over_surface.get_rect()
        game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(5000)
        pygame.quit()
    elif score_2 > score:
        my_font = pygame.font.SysFont("time new roman", 50)
        game_over_surface = my_font.render("The winner is blue with score : " + str(score_2), True , blue)
        game_over_rect = game_over_surface.get_rect()
        game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(5000)
        pygame.quit()
    else:
        my_font = pygame.font.SysFont("time new roman", 50)
        game_over_surface = my_font.render("It's a tie your scores are Green : " + str(score) + ", Blue : " + str(score_2), True , white)
        game_over_rect = game_over_surface.get_rect()
        game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(5000)
        pygame.quit()

is_g_death = "Alive"
is_b_death = "Alive"

def green_died():
    global is_g_death
    is_g_death = "Dead"

def blue_died():
    global is_b_death
    is_b_death = "Dead"

while True:
    for event in pygame.event.get():
        if is_g_death != "Dead":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = "UP"
                elif event.key == pygame.K_DOWN:
                    change_to = "DOWN"
                elif event.key == pygame.K_LEFT:
                    change_to = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    change_to = "RIGHT"

                if change_to == "UP" and direction != "DOWN":
                    direction = "UP"
                elif change_to == "DOWN" and direction != "UP":
                    direction = "DOWN"
                elif change_to == "LEFT" and direction != "RIGHT":
                    direction = "LEFT"
                elif change_to == "RIGHT" and direction != "LEFT":
                    direction = "RIGHT"

        if is_b_death != "Dead":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    change_to_2 = "UP"
                elif event.key == pygame.K_s:
                    change_to_2 = "DOWN"
                elif event.key == pygame.K_a:
                    change_to_2 = "LEFT"
                elif event.key == pygame.K_d:
                    change_to_2 = "RIGHT"

                if change_to_2 == "UP" and direction_2 != "DOWN":
                    direction_2 = "UP"
                elif change_to_2 == "DOWN" and direction_2 != "UP":
                    direction_2 = "DOWN"
                elif change_to_2 == "LEFT" and direction_2 != "RIGHT":
                    direction_2 = "LEFT"
                elif change_to_2 == "RIGHT" and direction_2 != "LEFT":
                    direction_2 = "RIGHT"

    if is_g_death != "Dead":
        if direction == "UP":
            s_position[1] -= 10
        elif direction == "DOWN":
            s_position[1] += 10
        elif direction == "RIGHT":
            s_position[0] += 10
        elif direction == "LEFT":
            s_position[0] -= 10

        s_body.insert(0, list(s_position))
        if s_position == fruit_position:
            score += 10
            fruit_spawn = False
            snake_speed += 2
        else:
            s_body.pop()
        

    if is_b_death != "Dead":
        if direction_2 == "UP":
            s2_position[1] -= 10
        elif direction_2 == "DOWN":
            s2_position[1] += 10
        elif direction_2 == "RIGHT":
            s2_position[0] += 10
        elif direction_2 == "LEFT":
            s2_position[0] -= 10

        s2_body.insert(0, list(s2_position))
        if s2_position == fruit_position:
            score_2 += 10
            fruit_spawn = False
            snake_speed += 2
        else:
            s2_body.pop()
        
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (xsize//10)) * 10, 
                          random.randrange(1, (ysize//10)) * 10]
        
    fruit_spawn = True
    game_window.fill(black)
    
    for pos in s_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    for pos in s2_body:
        pygame.draw.rect(game_window, blue, pygame.Rect(pos[0], pos[1], 10, 10))
    
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    if s_position[0] < 0 or s_position[0] > xsize-10:
        green_died()
    elif s_position[1] < 0 or s_position[1] > ysize-10:
        green_died()
    
    if s2_position[0] < 0 or s2_position[0] > xsize-10:
        blue_died()
    elif s2_position[1] < 0 or s2_position[1] > ysize-10:
        blue_died()
    
    for block in s_body:
        if s2_position == block:
            score += 25
            blue_died()
    
    for block in s2_body:
        if s_position == block:
            score_2 += 25
            green_died() 

    for block in s_body[1:]:
        if s_position == block:
            green_died()
    
    for block in s2_body[1:]:
        if s2_position == block:
            blue_died()

    if is_g_death == "Dead" and is_b_death == "Dead":
        game_over()
    
    show_score(1, green, "time new roman", 20, score, is_g_death)
    show_score(300, blue, "time new roman", 20, score_2, is_b_death)

    pygame.display.update()

    fps.tick(snake_speed)
