import pygame, random

pygame.init()

x_size = 450
y_size = 700
screen = x_size, y_size
game_sc = pygame.display.set_mode(screen)
pygame.display.set_caption("Crossy Rode")
fps = 40
clock = pygame.time.Clock()

white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
gray = pygame.Color(127, 127, 127)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)

font = pygame.font.Font(None, 20)

class Road:
    def __init__(self, posy, color):
        self.posx = -1
        self.posy = posy
        self.full = 0
        self.width = x_size + 2
        self.height = 100
        self.color = color
        self.Rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        self.DrawRect = pygame.draw.rect(game_sc, self.color, self.Rect, self.full)

    def display(self):
        self.DrawRect = pygame.draw.rect(game_sc, self.color, self.Rect, self.full)

    def getRoad(self):
        return self.Rect

class Chicken:
    def __init__(self, posx, posy, color, width, height, speed):
        self.posx = posx
        self.posy = posy
        self.color = color
        self.width = width
        self.height = height
        self.speed = speed
        self.Rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        self.DRect = pygame.draw.rect(game_sc, self.color, self.Rect)

    def display(self):
        self.DRect = pygame.draw.rect(game_sc, self.color, self.Rect)

    def update(self, Facx, Facy):
        self.posx = self.posx + self.speed * Facx
        self.posy = self.posy + self.speed * Facy
      
        if self.posx < 0:
            self.posx = 0
        elif self.posx + self.width > x_size:
            self.posx = x_size - self.width

        if self.posy < 0:
            self.posy = 0
        elif self.posy + self.height > y_size:
            self.posy = y_size - self.height
        
        self.Rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
      
    def showscore(self, text, font, score, x, y, color):
        text = font.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        game_sc.blit(text, textRect)

    def get_rect(self):
        return self.Rect

class Car:
    def __init__(self, posx, posy, width, height, speed, color, Vel):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.Vel = Vel
        self.Rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        self.DRect = pygame.draw.rect(game_sc, green, self.Rect)

    def display(self):
        self.DRect = pygame.draw.rect(game_sc, green, self.Rect)

    def update(self):
        self.posx += self.speed * self.Vel

        if self.posx < 0 or self.posx > x_size - self.width:
            self.Vel *= -1

        self.Rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
    
    def get_rect(self):
        return self.Rect
class Ball:
    def __init__(self, posx, posy, radius, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.color = color
        self.ball = pygame.draw.circle(game_sc, red, (self.posx, self.posy), self.radius)

    def display(self):
        self.ball = pygame.draw.circle(game_sc, red, (self.posx, self.posy), self.radius)

    def reset(self):
        self.posx = random.choice(range(x_size))
        self.posy = random.choice(range(y_size))
    
    def get_rect(self):
        return self.ball
    
def game_over(score):
    my_font = pygame.font.SysFont("time new roman", 50)
    game_over_surface = my_font.render("Your score was : " + str(round(score)), True , white)
    game_over_rect = game_over_surface.get_rect()
    game_sc.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    pygame.time.wait(5000)
    pygame.quit()

def main():
    road1 = Road(100, gray)
    road2 = Road(300, gray)
    road3 = Road(500, gray)
    roads = [road1, road2, road3]

    chicken = Chicken(x_size//2, y_size - 50, white, 20, 20, 10)
    running = True
    Facx = 0
    Facy = 0
    score = 0
    next = "UP"

    car1 = Car(x_size - 50, 110, 50, 30, 5, green, -1)
    car2 = Car(0, 160, 50, 30, 5, green,1)
    car3 = Car(x_size - 50, 310, 50, 30, 5, green, -1)
    car4 = Car(0, 360, 50, 30, 5, green, 1)
    car5 =  Car(x_size - 50, 510, 50, 30, 5, green, -1)
    car6 = Car(0, 560, 50, 30, 5, green, 1)
    cars = [car1, car2, car3, car4, car5, car6]

    ball = Ball(random.choice(range(x_size)), random.choice(range(y_size)), 5, red)

    while running:
        game_sc.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    Facy -= 1
                elif event.key == pygame.K_DOWN:
                    Facy += 1
                elif event.key == pygame.K_LEFT:
                    Facx -= 1
                elif event.key == pygame.K_RIGHT:
                    Facx += 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    Facy = 0
                elif event.key == pygame.K_DOWN:
                    Facy = 0
                elif event.key == pygame.K_LEFT:
                    Facx = 0
                elif event.key == pygame.K_RIGHT:
                    Facx = 0
        if chicken.posy == 0 and next == "UP":
            score += 1
            next = "DOWN"
            if chicken.speed != 1:
                chicken.speed -= 1
            
        elif chicken.posy == y_size - chicken.height and next == "DOWN":
            score += 1
            next = "UP"
            if chicken.speed != 1:
                chicken.speed -= 1

        for car in cars:
            if pygame.Rect.colliderect(chicken.get_rect(), car.get_rect()):
                game_over(score)

        if pygame.Rect.colliderect(chicken.get_rect(), ball.get_rect()):
            score += 1
            ball.reset()
            if chicken.speed != 1:
                chicken.speed -= 1

        [road.display() for road in roads]
        chicken.update(Facx, Facy)
        [car.update() for car in cars]
        chicken.display()
        [car.display() for car in cars]
        ball.display()
        chicken.showscore("Score : ", font, score, 50, 20, white)


        pygame.display.flip()
        clock.tick(fps)


main()
