import pygame

pygame.init()

x_size, y_size = 900, 600
screen = x_size, y_size
fps = 60
font20 = pygame.font.Font(None, 20) 

pygame.display.set_caption("pong")
game_sc = pygame.display.set_mode(screen)
clock = pygame.time.Clock()

white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)

point = 0

class plate:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.color = color
        self.width = width
        self.speed = speed
        self.height = height
        self.geekrect = pygame.Rect(posx, posy, width, height)
        self.geek = pygame.draw.rect(game_sc, self.color, self.geekrect)

    def display(self):
        self.geek = pygame.draw.rect(game_sc, self.color, self.geekrect)

    def update(self, yFac):
        self.posy = self.posy + self.speed * yFac

        if self.posy <= 0:
            self.posy = 0
        
        if self.posy + self.height >= y_size :
            self.posy = y_size - self.height
        
        self.geekrect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def show_score(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        game_sc.blit(text, textRect)
    
    def getRect(self):
        return self.geekrect

class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.color = color
        self.speed = speed
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(game_sc, self.color, (self.posx, self.posy), self.radius)

    def display(self):
        self.ball = pygame.draw.circle(game_sc, self.color, (self.posx, self.posy), self.radius)
    
    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac

        if self.posy <= 0 or self.posy >= y_size - self.radius:
            self.yFac *= -1
        self.speed += 0.001
        
    def reset(self):
        global point
        self.posx = x_size//2
        self.posy = y_size//2
        self.xFac = 1
        self.yFac = -1
        self.speed = 3
        point = 0
        pygame.time.wait(1000)

    def hit(self):
        self.xFac *= -1
        self.speed += 1

    def getRect(self):
        return self.ball
    
    def score(self):
        global point
        if self.posx <= 0:
            point = 1 
        elif self.posx >= x_size:
            point = -1
        else:
            point = 0


def main():
    running = True

    score1, score2 = 0, 0
    yFac1, yFac2 = 0, 0

    player1 = plate(20, y_size//2, 10, 100, 10, white)
    player2 = plate(x_size - 30, y_size//2, 10, 100, 10, white)
    ball = Ball(x_size//2, y_size//2, 7, 3, white)
    

    players = [player1, player2]

    while running:
        game_sc.fill(black)
        pygame.draw.line(game_sc, white, (x_size//2, 0), (x_size//2, y_size))
        center1 = player1.posy + player1.height//2
        vector =  ball.posy - center1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    yFac2 -= 1
                elif event.key == pygame.K_DOWN:
                    yFac2 += 1
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    yFac2 = 0
        
        if abs(vector) >= 50:
             yFac1 = 1 if  vector >= 0 else -1
        else:
            yFac1 = 0
            

        for player in players:
            if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                ball.hit()

        player1.update(yFac1)
        player2.update(yFac2)
        ball.update()
        ball.score()

        if point == -1:
            score1 += 1
            ball.reset()
        elif point == 1:
            score2 += 1
            ball.reset()

        player1.display()
        player2.display()
        ball.display()

        player1.show_score("Player_1: ", score1, 100, 20, white)
        player2.show_score("Player_2: ", score2, x_size-100, 20, white)

        pygame.display.flip()
        clock.tick(fps)
    
main()
