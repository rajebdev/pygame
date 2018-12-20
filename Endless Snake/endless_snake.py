'''

Tugas PyGame make Game SNAKE

'''

import random
import pygame


# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set the width and height of each snake segment
segment_width = 15
segment_height = 15
# Margin between each segment
segment_margin = 3

gridSize = (segment_width + segment_margin)
# Set initial speed
x_change = segment_width + segment_margin
y_change = 0

SCREEN_WIDTH = gridSize * 45
SCREEN_HEIGHT = gridSize * 34


class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """
    # -- Methods
    # Constructor function

    def __init__(self, x, y, color):
        self.__fill = color
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.surface.Surface([segment_width, segment_height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def set_fill(self, color):
        self.image.fill(color)
        self.__fill = color

    def get_fill(self):
        return self.__fill


class Makan(pygame.sprite.Sprite):
    """ This class represents a food """

    def __init__(self):
        super().__init__()
        self.image = pygame.surface.Surface([15, 15])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(gridSize, SCREEN_WIDTH, gridSize)
        self.rect.y = random.randrange(gridSize, SCREEN_HEIGHT, gridSize)

    def updatePos(self):
        self.rect.x = random.randrange(gridSize, SCREEN_WIDTH, gridSize)
        self.rect.y = random.randrange(gridSize, SCREEN_HEIGHT, gridSize)


class Poison(pygame.sprite.Sprite):
    """ This class represents a poison """

    def __init__(self):
        super().__init__()
        self.image = pygame.surface.Surface([15, 15])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(gridSize, SCREEN_WIDTH, gridSize)
        self.rect.y = random.randrange(gridSize, SCREEN_HEIGHT, gridSize)

    def updatePos(self):
        self.rect.x = random.randrange(gridSize, SCREEN_WIDTH, gridSize)
        self.rect.y = random.randrange(gridSize, SCREEN_HEIGHT, gridSize)

class Wall(pygame.sprite.Sprite):
    """This class represents the bar at the bottom that the player controls """
    def __init__(self, color):
        """ Constructor function """
        # Call the parent's constructor
        super().__init__()
        if random.randint(0, 10) % 2 == 0:
            width = segment_width
            height = random.randrange(gridSize*5, gridSize*10, gridSize)
        else:
            height = segment_height
            width = random.randrange(gridSize*5, gridSize*10, gridSize)
        # Make a BLUE wall, of the size specified in the parameters
        self.image = pygame.surface.Surface([width, height])
        self.image.fill(color)
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        
        self.rect.x = random.randrange(gridSize, SCREEN_WIDTH, gridSize)
        self.rect.y = random.randrange(gridSize, SCREEN_HEIGHT, gridSize)

class WallManual(pygame.sprite.Sprite):
    """This class represents the bar at the bottom that the player controls """
    def __init__(self, x, y, width, height, color):
        """ Constructor function """
        # Call the parent's constructor
        super().__init__()
        # Make a BLUE wall, of the size specified in the parameters
        self.image = pygame.surface.Surface([width, height])
        self.image.fill(color)
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class ArrowKeyboard(object):
    """ Class Arrow Keyboard """

    def __init__(self):
        self.leftPressed = False
        self.rightPressed = False
        self.downPressed = False
        self.upPressed = False

    def update(self):
        self.__init__()


class Game(object):
    lvl = 1
    """ Class Game """

    def __init__(self, screen):
        self.over = False
        self.done = False
        self.pause = False
        self.score = 0
        self.allspriteslist = pygame.sprite.Group()
        self.snake_groups = pygame.sprite.Group()
        self.snake_segments = []
        self.makan_groups = pygame.sprite.Group()
        self.makan_list = []
        self.poison_groups = pygame.sprite.Group()
        self.poison_list = []
        self.update_poison = 0
        self.update_makan = 0
        self.eated_food = []
        self.eated_poison = []
        self.happened_crash = []

        # Start Engine
        self.__createFirstSnake()
        self.addFood()
        self.addPoison()
        self.showScore(screen)
        self.showLengthSnake(screen)

    def __createFirstSnake(self):
        for i in range(5):
            x = gridSize * (11 - i)
            y = gridSize * 3
            segment = Segment(x, y, WHITE)
            self.snake_segments.append(segment)
            self.snake_groups.add(segment)
            self.allspriteslist.add(segment)

    def run_Snake(self):
        old_segment = self.snake_segments.pop()
        self.snake_groups.remove(old_segment)
        self.allspriteslist.remove(old_segment)

        self.addSnake(BLUE)

        # Fill Kepala Ular
        for i in range(len(self.snake_segments)):
            if self.snake_segments[i].get_fill() == WHITE or self.snake_segments[i].get_fill() == BLUE:
                if i == 0:
                    self.snake_segments[i].set_fill(BLUE)
                else:
                    self.snake_segments[i].set_fill(WHITE)

    def cutSnake(self):
        for sg in self.snake_segments:
            sg.image.fill(RED)
        old_segment = self.snake_segments.pop()
        self.snake_groups.remove(old_segment)
        self.allspriteslist.remove(old_segment)

    def addSnake(self, color):
        x = self.snake_segments[0].rect.x + x_change
        y = self.snake_segments[0].rect.y + y_change
        self.segment = Segment(x, y, color)

        # Insert new segment into the list

        self.snake_segments.insert(0, self.segment)
        self.snake_groups.add(self.segment)
        self.allspriteslist.add(self.segment)

    def addFood(self):
        makan = Makan()
        for i in range(len(self.snake_segments)):
            rect = self.snake_segments[i].rect
            if makan.rect == rect:
                makan.updatePos()

        self.makan_list.append(makan)
        self.makan_groups.add(makan)
        self.allspriteslist.add(makan)

    def updateFood(self):
        old_makan = self.makan_list.pop(0)
        self.makan_groups.remove(old_makan)
        self.allspriteslist.remove(old_makan)

        self.addFood()

    def addPoison(self):
        racun = Poison()
        for i in range(len(self.snake_segments)):
            rect = self.snake_segments[i].rect
            if racun.rect == rect:
                racun.updatePos()
        self.poison_list.append(racun)
        self.poison_groups.add(racun)
        self.allspriteslist.add(racun)

    def updatePoison(self):
        old_racun = self.poison_list.pop(0)
        self.poison_groups.remove(old_racun)
        self.allspriteslist.remove(old_racun)

        self.addPoison()

    def eatingFood(self):
        makanan_termakan = pygame.sprite.spritecollide(
            self.segment, self.makan_groups, True)
        # Check the list of collisions.
        for makanan in makanan_termakan:
            self.eated_food.append(makanan)
            self.makan_list.remove(makanan)
            self.score += 1
            print(self.score)
            self.addSnake(BLUE)
            self.snake_segments[1].set_fill(GREEN)

    def eatingPoison(self):
        posion_termakan = pygame.sprite.spritecollide(
            self.segment, self.poison_groups, True)

        # Check the list of collisions.
        for poison in posion_termakan:
            self.addSnake(BLUE)
            self.eated_poison.append(poison)
            for sg in self.snake_segments:
                sg.set_fill(RED)
            self.score -= 1
            print(self.score)

    def collideSelf(self):
        self.snake_groups.remove(self.segment)
        nabrak_sendiri = pygame.sprite.spritecollide(
            self.segment, self.snake_groups, True)

        for nabrak in nabrak_sendiri:
            self.happened_crash.append(nabrak)
            for sg in self.snake_segments:
                sg.image.fill(BLUE)
            self.over = True

        self.snake_groups.add(self.segment)

    def showScore(self, screen):
        font = pygame.font.SysFont("serif", 20)
        txt = "Score : {}".format(self.score)
        text = font.render(txt, True, WHITE)
        screen.blit(text, [SCREEN_WIDTH-120, 30])

    def showLengthSnake(self, screen):
        font = pygame.font.SysFont("serif", 20)
        txt = "Panjang Ular : {}".format(len(self.snake_segments))
        text = font.render(txt, True, WHITE)
        screen.blit(text, [25, 30])

    def showLevel(self, screen):
        font = pygame.font.SysFont("serif", 20)
        txt = "Level : {}".format(self.lvl)
        text = font.render(txt, True, WHITE)
        screen.blit(text, [SCREEN_WIDTH//2-25, 30])

    def showGameOver(self, screen):
        screen.fill(WHITE)
        font = pygame.font.SysFont("serif", 30)
        txt = "GAME OVER, YOUR SCORE : {}".format(self.score)
        text = font.render(txt, True, BLACK)
        center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
        center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
        screen.blit(text, [center_x, center_y])

    def collWindow(self):
        for ss in self.snake_segments:
            if ss.rect.x < 0:  # jalan ke kiri
                ss.rect.x = SCREEN_WIDTH-18
            if ss.rect.x >= SCREEN_WIDTH:  # jalan ke kanan
                ss.rect.x = 0
            if ss.rect.y < 0:  # jalan keatas
                ss.rect.y = SCREEN_HEIGHT-18
            if ss.rect.y >= SCREEN_HEIGHT:  # jalan ke bawah
                ss.rect.y = 0

class Game2(Game):
    lvl = 2
    wall_groups = pygame.sprite.Group()
    wall_list = []
    update_wall = 5
    crashed_wall = []
    def addWall(self):
        wall = Wall(PINK)
        # for i in range(len(self.wall_list)):
        #     rect = self.wall_list[i].rect
        #     if wall.rect == rect:
        #         wall.updatePos()

        self.wall_list.append(wall)
        self.wall_groups.add(wall)
        self.allspriteslist.add(wall)

    def updateWall(self):
        old_wall = self.wall_list.pop(0)
        self.wall_groups.remove(old_wall)
        self.allspriteslist.remove(old_wall)

        self.addWall()

    def collideWall(self):
        wall_tertabrak = pygame.sprite.spritecollide(
            self.segment, self.wall_groups, True)
        # Check the list of collisions.
        for wall in wall_tertabrak:
            self.crashed_wall.append(wall)
            self.wall_groups.remove(wall)
            self.allspriteslist.remove(wall)
            self.over = True

class Game3(Game2):
    lvl = 3
    def createOuterWall(self):
        wallt = WallManual(0, 0, SCREEN_WIDTH, gridSize, PINK)
        wallr = WallManual(SCREEN_WIDTH-gridSize, 0, gridSize, SCREEN_HEIGHT, PINK)
        wallb = WallManual(0, SCREEN_HEIGHT-gridSize, SCREEN_WIDTH, gridSize, PINK)
        walll = WallManual(0, 0, gridSize, SCREEN_HEIGHT, PINK)
        
        wall_list = [wallt, wallr, wallb, walll]
        for wall in wall_list:
            self.wall_groups.add(wall)
            self.allspriteslist.add(wall)
    def collideOuterWall(self):
        wall_tertabrak = pygame.sprite.spritecollide(
            self.segment, self.wall_groups, True)
        # Check the list of collisions.
        for wall in wall_tertabrak:
            self.wall_groups.remove(wall)
            self.over = True


    


# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the window
pygame.display.set_caption('Snake Games UTM')

clock = pygame.time.Clock()

arrowKey = ArrowKeyboard()

game = Game(screen)


while not game.done:
    if game.score == 7 and game.lvl == 1:
        x_change = gridSize
        y_change = 0
        arrowKey.update()
        game = Game2(screen)

    elif game.score == 5 and game.lvl == 2:
        x_change = gridSize
        y_change = 0
        arrowKey.update()
        game = Game3(screen)


    for event in pygame.event.get():
        if event.type == pygame.constants.QUIT:
            game.done = True

        elif event.type == pygame.constants.MOUSEBUTTONDOWN:
            game.done = False

        # Set the speed based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        elif event.type == pygame.constants.KEYDOWN:

            if event.key == pygame.constants.K_ESCAPE:
                game.done = True

            # Pause
            elif event.key == pygame.constants.K_SPACE:
                if not game.pause:
                    game.pause = True
                else:
                    game.pause = False

            else:
                if not game.pause:
                    if event.key == pygame.constants.K_LEFT and not arrowKey.rightPressed:
                        x_change = gridSize * -1
                        y_change = 0
                        arrowKey.update()
                        arrowKey.leftPressed = True

                    if event.key == pygame.constants.K_RIGHT and not arrowKey.leftPressed:
                        x_change = gridSize
                        y_change = 0
                        arrowKey.update()
                        arrowKey.rightPressed = True

                    if event.key == pygame.constants.K_UP and not arrowKey.downPressed:
                        x_change = 0
                        y_change = (segment_height + segment_margin) * -1
                        arrowKey.update()
                        arrowKey.upPressed = True

                    if event.key == pygame.constants.K_DOWN and not arrowKey.upPressed:
                        x_change = 0
                        y_change = (segment_height + segment_margin)
                        arrowKey.update()
                        arrowKey.downPressed = True

    if not game.pause:

        # Agar Snake bisa jalan
        game.run_Snake()

        # print(len(game.snake_segments))

        game.eatingFood()

        game.eatingPoison()

        game.collWindow()

        if game.lvl > 1:
            game.collideWall()

        # Clear screen
        screen.fill(BLACK)

        game.allspriteslist.draw(screen)

        # Flip screen
        game.showScore(screen)

        game.showLevel(screen)

        game.showLengthSnake(screen)

        game.collideSelf()

        while game.over:
            clock.tick(1)
            game.showGameOver(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    game.over = False
                    game.done = True
                if event.type == pygame.constants.MOUSEBUTTONDOWN:
                    x_change = gridSize
                    y_change = 0
                    arrowKey.update()
                    game = Game(screen)

        pygame.display.flip()
        # Kecepatan
        clock.tick(10)

    game.update_makan += 1
    game.update_poison += 1

    if game.lvl > 1 :
        game.update_wall +=1

    if game.update_makan % 15 == 0 and not game.pause:
        if len(game.makan_list) == 3:
            game.updateFood()

        elif len(game.makan_list) < 3:
            game.addFood()

    if game.update_poison % 10 == 0 and not game.pause:
        if len(game.poison_list) == 3:
            game.updatePoison()

        elif len(game.poison_list) < 3:
            game.addPoison()

    if game.lvl > 1 :
        if game.update_wall % 35 == 0 and not game.pause:
            if len(game.wall_list) == 3:
                game.updateWall()

            elif len(game.wall_list) < 3:
                game.addWall()
    if game.lvl > 2:
        game.createOuterWall()

pygame.quit()
