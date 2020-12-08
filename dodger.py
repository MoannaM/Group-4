import pygame
import random
import sys
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


class Arbre(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Arbre.png')
        self.minsize = 100
        self.maxsize = 200
        self.minspeed = 2
        self.maxspeed = 2
        self.addnewrate = 50


arbre = Arbre()


class Thunder(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(pygame.image.load("Thunder.png"), 180)
        self.minsize = 80
        self.maxsize = 150
        self.minspeed = 2
        self.maxspeed = 2
        self.addnewrate = 50


thunder = Thunder()


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


def wait_for_player_to_pressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
                return


def player_has_hit_baddie(playerRect, BONUS):
    for b in BONUS:
        if player.rect.colliderect(b['rect']):
            return True
    return False


def player_has_hit_arbre(playerRect, Arbre):
    for t in Arbre:
        if playerRect.colliderect(t['rect']):
            return True
    return False


def player_has_hit_thunder(playerRect, Thunder):
    for h in Thunder:
        if playerRect.colliderect(h["rect"]):
            return True
    return False


def player_has_hit_badEgg(playerRect, BadEgg):
    for e in BadEgg:
        if playerRect.colliderect(e['rect']):
            return True
    return False


def draw_text(text, font, surface, x, y):
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


class Button:
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

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x < self.x + self.width:
            if pos[1] > self.y < self.y + self.height:
                return True

        return False


# Show the start screen
Run = True
greenButton = Button((0, 0, 0), 370, 220, 145, 60, 'START')
Howtoplaybutton = Button((0, 0, 0), 40, 400, 220, 52, 'how to play')
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
            if Howtoplaybutton.is_over(pos):
                Howtoplaybutton.color = (150, 150, 150)
            else:
                Howtoplaybutton.color = (10, 190, 255)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if Howtoplaybutton.is_over(pos):
                windowSurface.blit(GameOverBackground, [0, 0])

        if event.type == pygame.MOUSEMOTION:
            if greenButton.is_over(pos):
                greenButton.color = (150, 150, 150)
            else:
                greenButton.color = (255, 255, 255)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if greenButton.is_over(pos):

                # start of the game
                topScore = 0
                while True:
                    # Set up the start of the game.
                    BONUS = []
                    Arbre = []
                    BadEgg = []
                    Thunder = []
                    score = 0
                    vie = 3
                    player.rect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
                    moveLeft = moveRight = moveUp = moveDown = False
                    reverseCheat = slowCheat = False
                    bonusAddCounter = 0
                    ArbreAddCounter = 0
                    BadEggAddCounter = 0
                    ThunderAddCounter = 0
                    pygame.mixer.music.play(-1, 0.0)
                    windowSurface.blit(Background, [0, 0])
                    pygame.mouse.set_visible(False)

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
                        if bonusAddCounter == bonus.addnewrate:
                            bonusAddCounter = 0
                            bonusSize = random.randint(bonus.minsize, bonus.maxsize)
                            newBonus = {'rect': pygame.Rect(WINDOWWIDTH-bonusSize, random.randint(0, WINDOWWIDTH - bonusSize), bonusSize, bonusSize),
                                        'speed': random.randint(bonus.minspeed, bonus.maxspeed),
                                        'surface': pygame.transform.scale(bonus.image, (bonusSize, bonusSize)),
                                        }

                            BONUS.append(newBonus)

                        # Add new arbre
                        if not reverseCheat and not slowCheat:
                            ArbreAddCounter += 1
                        if ArbreAddCounter == arbre.addnewrate:
                            ArbreAddCounter = 0
                            ArbreSize = random.randint(arbre.minsize, arbre.maxsize)
                            newTube = {'rect': pygame.Rect(WINDOWWIDTH-ArbreSize, WINDOWHEIGHT-ArbreSize, ArbreSize, ArbreSize),
                                       'speed': random.randint(arbre.minspeed, arbre.maxspeed),
                                       'surface': pygame.transform.scale(arbre.image, (40, ArbreSize)),
                                       }
                            Arbre.append(newTube)

                        # Add new thunder
                        if not reverseCheat and not slowCheat:
                            ThunderAddCounter += 1
                        if ThunderAddCounter == thunder.addnewrate:
                            ThunderAddCounter = 0
                            ThunderSize = random.randint(thunder.minsize, thunder.maxsize)
                            newThunder = {"rect": pygame.Rect(WINDOWWIDTH-ThunderSize, -0, ThunderSize, ThunderSize),
                                          "speed": random.randint(thunder.minspeed, thunder.maxspeed),
                                          "surface": pygame.transform.scale(thunder.image, (ThunderSize, ThunderSize)),
                                          }
                            Thunder.append(newThunder)

                        # Add new badegg
                        if not reverseCheat and not slowCheat:
                            BadEggAddCounter += 1
                        if BadEggAddCounter == badegg.addnewrate:
                            BadEggAddCounter = 0
                            BadEggSize = random.randint(badegg.minsize, badegg.maxsize)
                            newBadEgg = {'rect': pygame.Rect(WINDOWWIDTH-BadEggSize, random.randint(0, WINDOWWIDTH - BadEggSize), BadEggSize, BadEggSize),
                                         'speed': random.randint(badegg.minspeed, badegg.maxspeed),
                                         'surface': pygame.transform.scale(badegg.image, (BadEggSize, BadEggSize)),
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
                                b['rect'].move_ip(-b['speed'], 0)
                            elif reverseCheat:
                                b['rect'].move_ip(-5, 0)
                            elif slowCheat:
                                b['rect'].move_ip(1, 0)

                        # Move the arbre
                        for t in Arbre:
                            if not reverseCheat and not slowCheat:
                                t['rect'].move_ip(-t['speed'], 0)
                            elif reverseCheat:
                                t['rect'].move_ip(-5, 0)
                            elif slowCheat:
                                t['rect'].move_ip(1, 0)

                        # move the thunder
                        for h in Thunder:
                            if not reverseCheat and not slowCheat:
                                h["rect"].move_ip(-h["speed"], 0)
                            elif reverseCheat:
                                h["rect"].move_ip(-5, 0)
                            elif slowCheat:
                                h["rect"].move_ip(1, 0)

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

                        # Delete arbre that have fallen past the bottom.
                        for t in Arbre[:]:
                            if -t['rect'].top > WINDOWWIDTH:
                                Arbre.remove(t)

                        # Delete thunder have fallen past the bottom
                        for h in Thunder[:]:
                            if -h["rect"].top > WINDOWWIDTH:
                                Thunder.remove(h)

                        # Delete badegg that have fallen past the bottom.
                        for e in BadEgg[:]:
                            if -e['rect'].top > WINDOWWIDTH:
                                BadEgg.remove(e)

                        # Draw the game world on the window.
                        # windowSurface.fill(BACKGROUNDCOLOR)

                        # Background game
                        windowSurface.blit(Background, [0, 0])

                        # Draw arbre
                        for t in Arbre:
                            windowSurface.blit(t["surface"], t['rect'])
                        pygame.display.update()

                        # draw Thunder
                        for h in Thunder:
                            windowSurface.blit(h["surface"], h["rect"])
                        pygame.display.update()

                        # Draw the score and top score.
                        fichier = open("data.txt", "r")
                        draw_text('Score: %s' % score, font, windowSurface, 10, 0)
                        draw_text('Top Score: %s' % (fichier.read()), font, windowSurface, 10, 40)
                        draw_text("vie: %s" % vie, font, windowSurface, 10, 80)
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
                        if player_has_hit_baddie(player.rect, BONUS):
                            PlayerHitGiftEggSound.play()
                            bonuss = random.choice([1, 100])
                            if bonuss == 100:
                                score = score+bonuss
                            else:
                                vie = vie+bonuss

                            BONUS.remove(b)

                        # Check if any of the arbre have hit the player.
                        if player_has_hit_arbre(player.rect, Arbre):
                            if score > topScore:
                                topScore = score  # set new top score
                                os.remove("data.txt")
                                fichier = open("data.txt", "w")
                                topscore = str(topScore)
                                fichier.write(topscore)
                                fichier.close()
                            break

                        # chech if any of thunder have hit the player
                        if player_has_hit_thunder(player.rect, Thunder):
                            if score > topScore:
                                topScore = score
                                os.remove("data.txt")
                                fichier = open("data.txt", "w")
                                topscore = str(topScore)
                                fichier.write(topscore)
                                fichier.close()
                            break

                        # Check if any of the badegg have hit the player.
                        if player_has_hit_badEgg(player.rect, BadEgg):
                            PlayerHitBadEggSound.play()
                            for e in BadEgg[:]:
                                if player_has_hit_badEgg(player.rect, BadEgg):
                                    BadEgg.remove(e)
                            if vie < 2:
                                if score > topScore:
                                    topScore = score
                                    os.remove("data.txt")
                                    fichier = open("data.txt", "w")
                                    topscore = str(topScore)
                                    fichier.write(topscore)
                                    fichier.close()
                                break
                            else:
                                vie = vie-1

                    # Stop the game and show the "Game Over" screen.
                    pygame.mixer.music.stop()
                    gameOverSound.play()

                    windowSurface.blit(GameOverBackground, [0, 0])
                    pygame.mouse.set_visible(True)

                    draw_text('GAME OVER', font, windowSurface, 370, 220)
                    draw_text('Press a key to play again.', font, windowSurface, 280, 280)
                    pygame.display.update()
                    wait_for_player_to_pressKey()

                    gameOverSound.stop()
