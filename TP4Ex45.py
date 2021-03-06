import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 900
WINDOWHEIGHT = 500
TEXTCOLOR = (0, 0, 0)
# BACKGROUNDCOLOR = (75, 255, 100) #YELLOW GREEN BLUE
# FPS = 60
BONUSMINSIZE = 20
BONUSMAXSIZE = 40
BONUSMINSPEED = 1
BONUSMAXSPEED = 8
ADDNEWBONUSRATE = 20
TUBEMINSIZE = 40
TUBEMAXSIZE = 140
TUBEMAXSPEED = 4
TUBEMINSPEED = 4
ADDNEWTUBERATE = 5000
BADEGGMINSIZE = 20
BADEGGMAXSIZE = 40
BADEGGMINSPEED = 1
BADEGGMAXSPEED = 8
ADDNEWBADEGGRATE = 6000
PLAYERMOVERATE = 5
Tube_HautMAXSIZE = 80
Tube_HautMINSIZE = 50
Tube_HautMAXSPEED = 4
Tube_HautMINSPEED = 4
ADDNEWTube_HAUTRATE = 5000


def terminate():
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
                return


def playerHasHitBaddie(playerRect, bonus):
    for b in bonus:
        if player.rect.colliderect(b['rect']):
            return True
    return False


def playerHasHitTube(playerRect, Tube):
    for t in Tube:
        if playerRect.colliderect(t['rect']):
            return True
    return False


def playerHasHitHaut(playerRect, Tube_Haut):
    for h in Tube_Haut:
        if playerRect.colliderect(h["rect"]):
            return True
    return False


def playerHasHitBadEgg(playerRect, BadEgg):
    for e in BadEgg:
        if playerRect.colliderect(e['rect']):
            return True
    return False


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Poulet.png')
        self.rect = self.image.get_rect()
        self.MOVERATE = 5


player = Player()

# Set up pygame, the window, and the mouse cursor.
pygame.init()
# mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
# pygame.display.set_caption('Dodger') #Remplacer dodger par chicken run
pygame.mouse.set_visible(True)

# Set up the fonts.
font = pygame.font.SysFont('Corbel', 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('GameOver.wav')
PlayerHitBadEggSound = pygame.mixer.Sound('Aïe.wav')
pygame.mixer.music.load('Background.wav')

# Set up images. #todo : ajouter image chasseur(qui tire depuis le fond)/renard/balles

bonusImage = pygame.image.load('EGG.png')
tube = pygame.image.load('Tube.png').convert_alpha()
badegg = pygame.image.load('BadEgg.png').convert_alpha()
Background = pygame.image.load('Background.jpg').convert()
tube_Haut = pygame.transform.rotate(pygame.image.load("tube.png").convert_alpha(), 180)
GameOverBackground = pygame.image.load('Background-gameover.png')
StartBackground = pygame.image.load('StartBackground.png')


# tube du haut = pygame.transform.rotate(pygame.image.load("Tube.png").convert_alpha(),180)

# Set up start button
class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, windowSurface, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(windowSurface, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(windowSurface, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            windowSurface.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


# Show the "Start" screen.
windowSurface.blit(StartBackground, [0, 0])
# drawText('Chicken Run', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
# waitForPlayerToPressKey()
button((0, 255, 0), 150, 225, 250, 100, 'START')




topScore = 0
while True:
            # Set up the start of the game.
            bonus = []
            Tube = []
            BadEgg = []
            Tube_Haut = []
            score = 0
            vie = 3
            player.rect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
            moveLeft = moveRight = moveUp = moveDown = False
            reverseCheat = slowCheat = False
            bonusAddCounter = 0
            TubeAddCounter = 0
            BadEggAddCounter = 0
            Tube_HautAddCounter = 0
            pygame.mixer.music.play(-1, 0.0)
            windowSurface.blit(Background, [0, 0])
            pygame.mouse.set_visible(False)
            # Button = button((0, 0, 0), 150, 225, 250, 100, 'START')

            while True:  # The game loop runs while the game part is playing.
                score += 1  # Increase score.

                for event in pygame.event.get():
                    if event.type == QUIT:
                        terminate()

                    if event.type == MOUSEMOTION:
                        # If the mouse moves, move the player where to the cursor.
                        player.rect.centerx = event.pos[0]
                        player.rect.centery = event.pos[1]

                # Add new bonus at the top of the screen, if needed.
                if not reverseCheat and not slowCheat:
                    bonusAddCounter += 1
                if bonusAddCounter == ADDNEWBONUSRATE:
                    bonusAddCounter = 0
                    bonusSize = random.randint(BONUSMINSIZE, BONUSMAXSIZE)
                    newBonus = {
                        'rect': pygame.Rect(WINDOWWIDTH - bonusSize, random.randint(0, WINDOWWIDTH - bonusSize), bonusSize,
                                            bonusSize),
                        'speed': random.randint(BONUSMINSPEED, BONUSMAXSPEED),
                        'surface': pygame.transform.scale(bonusImage, (bonusSize, bonusSize)),
                        }

                    bonus.append(newBonus)

                # Add new tube
                if not reverseCheat and not slowCheat:
                    TubeAddCounter += 1
                if TubeAddCounter == ADDNEWTUBERATE:
                    TubeAddCounter = 0
                    tubeSize = random.randint(TUBEMINSIZE, TUBEMAXSIZE)
                    newTube = {'rect': pygame.Rect(WINDOWWIDTH - tubeSize, WINDOWHEIGHT - tubeSize, tubeSize, tubeSize),
                               'speed': random.randint(TUBEMINSPEED, TUBEMAXSPEED),
                               'surface': pygame.transform.scale(tube, (40, tubeSize)),
                               }
                    Tube.append(newTube)

                # Add new tube_haut
                if not reverseCheat and not slowCheat:
                    Tube_HautAddCounter += 1
                if Tube_HautAddCounter == ADDNEWTube_HAUTRATE:
                    Tube_HautAddCounter = 0
                    Tube_HautSize = random.randint(Tube_HautMINSIZE, Tube_HautMAXSIZE)
                    newTube_Haut = {"rect": pygame.Rect(WINDOWWIDTH - Tube_HautSize, -0, Tube_HautSize, Tube_HautSize),
                                    "speed": random.randint(Tube_HautMINSPEED, Tube_HautMAXSPEED),
                                    "surface": pygame.transform.scale(tube_Haut, (Tube_HautSize, Tube_HautSize)),
                                    }
                    Tube_Haut.append(newTube_Haut)

                # Add new badegg
                if not reverseCheat and not slowCheat:
                    BadEggAddCounter += 1
                if BadEggAddCounter == ADDNEWBADEGGRATE:
                    BadEggAddCounter = 0
                    BadEggSize = random.randint(BADEGGMINSIZE, BADEGGMAXSIZE)
                    newBadEgg = {'rect': pygame.Rect(WINDOWWIDTH - BadEggSize, random.randint(0, WINDOWWIDTH - BadEggSize),
                                                     BadEggSize, BadEggSize),
                                 'speed': random.randint(BADEGGMINSPEED, BADEGGMAXSPEED),
                                 'surface': pygame.transform.scale(badegg, (BadEggSize, BadEggSize)),
                                 }

                    BadEgg.append(newBadEgg)

                # Move the player around.
                if moveLeft and player.rect.left > 0:
                    player.rect.move_ip(-1 * player.MOVERATE, 0)
                if moveRight and player.rect.right < WINDOWWIDTH:
                    player.rect.move_ip(player.MOVERATE, 0)
                if moveUp and player.rect.top > 0:
                    player.rect.move_ip(0, -1 * player.MOVERATE)
                if moveDown and player.rect.bottom < WINDOWHEIGHT:
                    player.rect.move_ip(0, player.MOVERATE)

                # Move the bonus down.
                for b in bonus:
                    if not reverseCheat and not slowCheat:
                        b['rect'].move_ip(-b['speed'], 0)
                    elif reverseCheat:
                        b['rect'].move_ip(-5, 0)
                    elif slowCheat:
                        b['rect'].move_ip(1, 0)

                # Move the tubes down.
                for t in Tube:
                    if not reverseCheat and not slowCheat:
                        t['rect'].move_ip(-t['speed'], 0)
                    elif reverseCheat:
                        t['rect'].move_ip(-5, 0)
                    elif slowCheat:
                        t['rect'].move_ip(1, 0)

                # move the tube_Haut down
                for h in Tube_Haut:
                    if not reverseCheat and not slowCheat:
                        h["rect"].move_ip(-h["speed"], 0)
                    elif reverseCheat:
                        h["rect"].move_ip(-5, 0)
                    elif slowCheat:
                        h["rect"].move_ip(1, 0)

                # Move the badegg down
                for e in BadEgg:
                    if not reverseCheat and not slowCheat:
                        e['rect'].move_ip(-e['speed'], 0)
                    elif reverseCheat:
                        e['rect'].move_ip(-5, 0)
                    elif slowCheat:
                        e['rect'].move_ip(1, 0)

                # Delete bonus that have fallen past the bottom.
                for b in bonus[:]:
                    if -b['rect'].top > WINDOWWIDTH:
                        bonus.remove(b)

                # Delete tubes that have fallen past the bottom.
                for t in Tube[:]:
                    if -t['rect'].top > WINDOWWIDTH:
                        Tube.remove(t)
                # Delete tube_haut have fallen past the bottom
                for h in Tube_Haut[:]:
                    if -h["rect"].top > WINDOWWIDTH:
                        Tube_Haut.remove(h)

                # Delete badegg that have fallen past the bottom.
                for e in BadEgg[:]:
                    if -e['rect'].top > WINDOWWIDTH:
                        BadEgg.remove(e)

                # Draw the game world on the window.
                # windowSurface.fill(BACKGROUNDCOLOR)

                # Background game
                windowSurface.blit(Background, [0, 0])

                # Draw tube
                for t in Tube:
                    windowSurface.blit(t["surface"], t['rect'])
                pygame.display.update()

                # draw Tube_Haut
                for h in Tube_Haut:
                    windowSurface.blit(h["surface"], h["rect"])
                pygame.display.update()

                # Draw the score and top score.
                drawText('Score: %s' % (score), font, windowSurface, 10, 0)
                drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
                drawText("vie: %s" % (vie), font, windowSurface, 10, 80)

                # Draw the player's rectangle.
                windowSurface.blit(player.image, player.rect)

                # Draw each bonus.
                for b in bonus:
                    windowSurface.blit(b["surface"], b['rect'])
                pygame.display.update()

                # Draw each BadEgg.
                for e in BadEgg:
                    windowSurface.blit(e["surface"], e['rect'])
                pygame.display.update()

                # Check if any of the bonus have hit the player.
                if playerHasHitBaddie(player.rect, bonus):
                    score = score + 100
                    bonus.remove(b)

                # Check if any of the tube have hit the player.
                if playerHasHitTube(player.rect, Tube):
                    if score > topScore:
                        topScore = score  # set new top score
                    break
                # chech if any of tube_Haut have hit the player
                if playerHasHitHaut(player.rect, Tube_Haut):
                    if score > topScore:
                        topScore = score
                    break

                # Check if any of the badegg have hit the player.
                if playerHasHitBadEgg(player.rect, BadEgg):
                    PlayerHitBadEggSound.play()
                    for e in BadEgg[:]:
                        if playerHasHitBadEgg(player.rect, BadEgg):
                            BadEgg.remove(e)
                    if vie < 2:
                        if score > topScore:
                            topScore = score
                        break
                    else:
                        vie = vie - 1

                # Stop the game and show the "Game Over" screen.
            pygame.mixer.music.stop()
            gameOverSound.play()

            windowSurface.blit(GameOverBackground, [0, 0])
            pygame.mouse.set_visible(True)

            drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
            drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
            pygame.display.update()
            waitForPlayerToPressKey()

            gameOverSound.stop()


