import pygame, random, sys
from pygame.locals import *
import os

WINDOWWIDTH = 900
WINDOWHEIGHT = 500
TEXTCOLOR = (0, 0, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Poulet.png')
        self.rect = self.image.get_rect()
        self.MOVERATE = 5

player = Player()

class Tube(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Arbre.png')
        self.minsize = 100
        self.maxsize = 200
        self.minspeed = 2
        self.maxspeed = 2
        self.addnewrate = 50

tube = Tube()

class TubeHaut(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(pygame.image.load("Thunder.png"),180)
        self.minsize = 80
        self.maxsize = 150
        self.minspeed = 2
        self.maxspeed = 2
        self.addnewrate = 50

tubehaut = TubeHaut()

class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('EGG.png')
        self.minsize = 20
        self.maxsize = 40
        self.minspeed = 1
        self.maxspeed = 8
        self.addnewrate = 50

bonus = Bonus()

class Badegg(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('BadEgg.png')
        self.minsize = 20
        self.maxsize = 40
        self.minspeed = 1
        self.maxspeed = 8
        self.addnewrate = 20

badegg = Badegg()


def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def playerHasHitBaddie(playerRect, BONUS):
    for b in BONUS:
        if player.rect.colliderect(b['rect']):
            return True
    return False

def playerHasHitTube(playerRect, Tube):
    for t in Tube:
        if playerRect.colliderect(t['rect']):
            return True
    return False

def playerHasHitHaut(playerRect, Tube_Haut):
    for h in TUBEHaut:
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


# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Chicken run')
pygame.mouse.set_visible(True)

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('GameOver.wav')
PlayerHitBadEggSound = pygame.mixer.Sound('Aïe.wav')
PlayerHitGiftEggSound = pygame.mixer.Sound('Happy.wav')
pygame.mixer.music.load('Background.wav')

# Set up images.
Background = pygame.image.load('Background.png').convert()
GameOverBackground = pygame.image.load('Background-gameover.png')
StartBackground = pygame.image.load('StartBackground.png')

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
            font = pygame.font.SysFont('comicsansms', 40)
            text = font.render(self.text, 1, (0, 0, 0))
            windowSurface.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


#Show the start screen
Run = True
greenButton = button((0, 0, 0), 370, 220, 145, 60, 'START')
Howtoplaybutton = button((0, 0, 0), 40, 400, 220, 52, 'how to play')
while Run:
    windowSurface.blit(StartBackground, [0, 0])
    greenButton.draw(windowSurface, (0, 0, 0))
    Howtoplaybutton.draw(windowSurface, (0, 0, 0))
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEMOTION:
            if Howtoplaybutton.isOver(pos):
                Howtoplaybutton.color = (150, 150, 150)
            else:
                Howtoplaybutton.color = (10, 190, 255)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if Howtoplaybutton.isOver(pos):
                windowSurface.blit(GameOverBackground, [0, 0])

        if event.type == pygame.MOUSEMOTION:
            if greenButton.isOver(pos):
                greenButton.color = (150, 150, 150)
            else:
                greenButton.color = (255, 255, 255)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if greenButton.isOver(pos):

                # start of the game
                topScore = 0
                while True:
                    # Set up the start of the game.
                    BONUS = []
                    TUBE = []
                    BadEgg = []
                    TUBEHaut = []
                    score = 0
                    vie = 3
                    player.rect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
                    moveLeft = moveRight = moveUp = moveDown = False
                    reverseCheat = slowCheat = False
                    bonusAddCounter = 0
                    TubeAddCounter=0
                    BadEggAddCounter = 0
                    TubeHautAddCounter =0
                    pygame.mixer.music.play(-1, 0.0)
                    windowSurface.blit(Background, [0, 0])
                    pygame.mouse.set_visible(False)

                    while True: # The game loop runs while the game part is playing.
                        score += 1 # Increase score.

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
                        if bonusAddCounter == bonus.addnewrate:
                            bonusAddCounter = 0
                            bonusSize = random.randint(bonus.minsize, bonus.maxsize)
                            newBonus = {'rect': pygame.Rect(WINDOWWIDTH-bonusSize, random.randint(0, WINDOWWIDTH - bonusSize), bonusSize, bonusSize),
                                        'speed': random.randint(bonus.minspeed, bonus.maxspeed),
                                        'surface':pygame.transform.scale(bonus.image, (bonusSize, bonusSize)),
                                        }

                            BONUS.append(newBonus)

                        #Add new tube
                        if not reverseCheat and not slowCheat:
                            TubeAddCounter += 1
                        if TubeAddCounter == tube.addnewrate:
                            TubeAddCounter = 0
                            tubeSize = random.randint(tube.minsize, tube.maxsize)
                            newTube = { 'rect': pygame.Rect(WINDOWWIDTH-tubeSize,WINDOWHEIGHT-tubeSize, tubeSize, tubeSize),
                                        'speed': random.randint(tube.minspeed, tube.maxspeed),
                                        'surface':pygame.transform.scale(tube.image, (40, tubeSize)),
                                        }
                            TUBE.append(newTube)

                        #Add new tube_haut
                        if not reverseCheat and not slowCheat:
                            TubeHautAddCounter+= 1
                        if TubeHautAddCounter == tubehaut.addnewrate:
                            TubeHautAddCounter = 0
                            TubeHautSize=random.randint(tubehaut.minsize,tubehaut.maxsize)
                            newTubeHaut = {"rect":pygame.Rect(WINDOWWIDTH-TubeHautSize,-0,TubeHautSize,TubeHautSize),
                                        "speed": random.randint(tubehaut.minspeed,tubehaut.maxspeed),
                                        "surface": pygame.transform.scale(tubehaut.image,(TubeHautSize,TubeHautSize)),
                                        }
                            TUBEHaut.append(newTubeHaut)

                        #Add new badegg
                        if not reverseCheat and not slowCheat:
                            BadEggAddCounter += 1
                        if BadEggAddCounter == badegg.addnewrate:
                            BadEggAddCounter = 0
                            BadEggSize = random.randint(badegg.minsize, badegg.maxsize)
                            newBadEgg = {'rect': pygame.Rect(WINDOWWIDTH-BadEggSize, random.randint(0, WINDOWWIDTH - BadEggSize), BadEggSize, BadEggSize),
                                        'speed': random.randint(badegg.minspeed, badegg.maxspeed),
                                        'surface':pygame.transform.scale(badegg.image, (BadEggSize, BadEggSize)),
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

                        # Move the bonus
                        for b in BONUS:
                            if not reverseCheat and not slowCheat:
                                b ['rect'].move_ip(-b['speed'],0 )
                            elif reverseCheat:
                                b['rect'].move_ip(-5, 0)
                            elif slowCheat:
                                b['rect'].move_ip(1, 0)

                        # Move the tubes
                        for t in TUBE:
                            if not reverseCheat and not slowCheat:
                                t['rect'].move_ip(-t['speed'], 0)
                            elif reverseCheat:
                                t['rect'].move_ip(-5, 0)
                            elif slowCheat:
                                t['rect'].move_ip(1, 0)

                        #move the tubeHaut
                        for h in TUBEHaut:
                            if not reverseCheat and not slowCheat:
                                h["rect"].move_ip(-h["speed"],0)
                            elif reverseCheat:
                                h["rect"].move_ip(-5,0)
                            elif slowCheat:
                                h["rect"].move_ip(1,0)

                        # Move the badegg
                        for e in BadEgg:
                            if not reverseCheat and not slowCheat:
                                e['rect'].move_ip(-e['speed'], 0)
                            elif reverseCheat:
                                e['rect'].move_ip(-5, 0)
                            elif slowCheat:
                                e['rect'].move_ip(1, 0)

                        # Delete bonus that have fallen past the bottom.
                        for b in BONUS[:]:
                            if -b['rect'].top > WINDOWWIDTH:
                                BONUS.remove(b)

                        # Delete tubes that have fallen past the bottom.
                        for t in TUBE[:]:
                            if -t['rect'].top > WINDOWWIDTH:
                                TUBE.remove(t)

                        # Delete tube_haut have fallen past the bottom
                        for h in TUBEHaut[:]:
                            if -h["rect"].top > WINDOWWIDTH:
                                TUBEHaut.remove(h)

                        # Delete badegg that have fallen past the bottom.
                        for e in BadEgg[:]:
                            if -e['rect'].top > WINDOWWIDTH:
                                BadEgg.remove(e)

                        # Draw the game world on the window.
                        #windowSurface.fill(BACKGROUNDCOLOR)

                        # Background game
                        windowSurface.blit(Background, [0, 0])

                        # Draw tube
                        for t in TUBE:
                            windowSurface.blit(t["surface"], t['rect'])
                        pygame.display.update()

                        #draw Tube_Haut
                        for h in TUBEHaut:
                            windowSurface.blit(h["surface"], h["rect"])
                        pygame.display.update()

                        # Draw the score and top score.
                        fichier = open("data.txt","r")
                        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
                        drawText('Top Score: %s' % (fichier.read()), font, windowSurface, 10, 40)
                        drawText("vie: %s" % (vie), font, windowSurface, 10, 80)
                        fichier.close()

                        # Draw the player's rectangle.
                        windowSurface.blit(player.image, player.rect)

                        # Draw each bonus.
                        for b in BONUS:
                            windowSurface.blit(b["surface"], b['rect'])
                        pygame.display.update()

                        # Draw each BadEgg.
                        for e in BadEgg:
                            windowSurface.blit(e["surface"], e['rect'])
                        pygame.display.update()

                        # Check if any of the bonus have hit the player.
                        if playerHasHitBaddie(player.rect, BONUS):
                            PlayerHitGiftEggSound.play()
                            bonuss = random.choice([1, 100])
                            if bonuss == 100:
                                score = score+bonuss
                            else:
                                vie = vie+bonuss

                            BONUS.remove(b)

                        # Check if any of the tube have hit the player.
                        if playerHasHitTube(player.rect, TUBE):
                            if score > topScore:
                                topScore = score # set new top score
                                os.remove("data.txt")
                                fichier = open("data.txt", "w")
                                topscore = str(topScore)
                                fichier.write(topscore)
                                fichier.close()
                            break

                        # chech if any of tube Haut have hit the player
                        if playerHasHitHaut(player.rect, TUBEHaut):
                            if score > topScore:
                                topScore = score
                                os.remove("data.txt")
                                fichier = open("data.txt", "w")
                                topscore = str(topScore)
                                fichier.write(topscore)
                                fichier.close()
                            break

                        # Check if any of the badegg have hit the player.
                        if playerHasHitBadEgg(player.rect, BadEgg):
                            PlayerHitBadEggSound.play()
                            for e in BadEgg[:]:
                                if playerHasHitBadEgg(player.rect, BadEgg):
                                    BadEgg.remove(e)
                            if vie < 2:
                                if score > topScore:
                                    topScore=score
                                    os.remove("data.txt")
                                    fichier = open("data.txt","w")
                                    topscore = str(topScore)
                                    fichier.write(topscore)
                                    fichier.close()
                                break
                            else:
                                vie=vie-1


                    # Stop the game and show the "Game Over" screen.
                    pygame.mixer.music.stop()
                    gameOverSound.play()

                    windowSurface.blit(GameOverBackground, [0, 0])
                    pygame.mouse.set_visible(True)

                    drawText('GAME OVER', font, windowSurface, 370, 220)
                    drawText('Press a key to play again.', font, windowSurface, 280, 280)
                    pygame.display.update()
                    waitForPlayerToPressKey()

                    gameOverSound.stop()