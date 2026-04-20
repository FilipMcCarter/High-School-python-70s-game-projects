import random
import pygame

x_size = 720
y_size = 480

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

pygame.init()

pygame.display.set_caption("flying poop")
game_window = pygame.display.set_mode((x_size, y_size))

fps = pygame.time.Clock()

x = 0

b_position = [50, 200]
pipe_x = x_size 
bird_speed = 10

pipe = []
def pipes():
    global y_size
    global pipe
    global x_size
    global x 
    y = 0
    hole_start = random.choice(range(0, 24))
    while y < y_size:
        y += 20
        if y//20 not in range(hole_start, (hole_start + 5)):
            pipe.append([x_size, y]) 
    


    
score = 0   
counter = 0 

def show_score(x, color, font, size, points):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score : " + str(round(points)), True, color)
    game_window.blit(score_surface, [x, 5])
    pygame.display.flip()

def game_over():
    my_font = pygame.font.SysFont("time new roman", 50)
    game_over_surface = my_font.render("Your score was : " + str(round(score)), True , green)
    game_over_rect = game_over_surface.get_rect()
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    pygame.time.wait(5000)
    pygame.quit()

jump = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump = True
            else:
                jump = False
    if jump == True:
        b_position[1] -= 30
    else:
        b_position[1] += 20

    game_window.fill(black)

    if counter % 25 == 0:
        x += 24
        pipes()

    for p in pipe:
        p[0] -= 10
        pygame.draw.rect(game_window, green, pygame.Rect(p[0], p[1], 30, 20) )

    for p in pipe:
        if p[0] < 0:
            pipe.remove(p)

    pygame.draw.rect(game_window, white, pygame.Rect(b_position[0], b_position[1], 10, 10))

    for p in pipe:
        if b_position == p:
            game_over()
        
    if b_position[1] < 0 or b_position[1] > y_size:
        game_over()

    for p in pipe:
        if b_position[0] == p[0]:
            score += 0.05

    show_score(1, white, "time new roman", 20, score)

    jump = False
    pipe_x -= 10
    counter += 1

    pygame.display.update()

    fps.tick(bird_speed)



