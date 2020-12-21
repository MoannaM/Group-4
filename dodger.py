import pygame
import random
import sys
from pygame.locals import *
import os
from button import Button

FPS = 60
fpsClock = pygame.time.Clock()

WINDOWWIDTH = 900
WINDOWHEIGHT = 500
TEXTCOLOR = (0, 0, 0)


# Set up of classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Poulet.png')
        self.rect = self.image.get_rect()
        self.MOVERATE = 4


class Arbre(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Arbre.png')
        self.minsize = 100
        self.maxsize = 200
        self.speed = 2
        self.addnewrate = 50


class Thunder(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(pygame.image.load("Thunder.png"), 180)
        self.minsize = 80
        self.maxsize = 150
        self.speed = 2
        self.addnewrate = 130


class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('EGG.png')
        self.minsize = 20
        self.maxsize = 40
        self.minspeed = 1
        self.maxspeed = 8
        self.addnewrate = 50


class Badegg(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('BadEgg.png')
        self.minsize = 20
        self.maxsize = 40
        self.minspeed = 1
        self.maxspeed = 8
        self.addnewrate = 30


class Game(pygame.sprite.Sprite):
    def __init__(self):
        self.player = Player()
        self.arbre = Arbre()
        self.thunder = Thunder()
        self.bonus = Bonus()
        self.badegg = Badegg()

    def player_has_hit_bonus(playerRect, b, BONUS):
        for b in BONUS:
            if Game.player.rect.colliderect(b['rect']):
                return True
        return False

    def player_has_hit_arbre(playerRect, t, Arbre):
        for t in Arbre:
            if Game.player.rect.colliderect(t['rect']):
                return True
        return False

    def player_has_hit_thunder(playerRect, h, Thunder):
        for h in Thunder:
            if Game.player.rect.colliderect(h["rect"]):
                return True
        return False

    def player_has_hit_badEgg(playerRect, e, BadEgg):
        for e in BadEgg:
            if Game.player.rect.colliderect(e['rect']):
                return True
        return False


Game = Game()


def terminate():
    pygame.quit()
    sys.exit()


# set up of a function with a text style
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
font = pygame.font.SysFont('ComicSansMs', 35)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('GameOver.wav')
PlayerHitBadEggSound = pygame.mixer.Sound('Aïe.wav')
PlayerHitGiftEggSound = pygame.mixer.Sound('Happy.wav')
pygame.mixer.music.load('Background.wav')

# Set up images.
Background = pygame.image.load('Background.png').convert()
GameOverBackground = pygame.image.load('Background-gameover.png')
StartBackground = pygame.image.load('StartBackground.png')
HowToPlayBackground = pygame.image.load('How-to-play.png')

#game = Game


def play():  # set up of a function to organise the game better
    # start of the game
    fichier = open("data.txt", "r")
    topScore = int(fichier.read())
    fichier.close()
    while True:
        # Set up the start of the game.
        BonusCollection = []
        TreeCollection = []
        BadEgg = []
        Thunder = []
        score = 0
        vie = 3
        Game.player.rect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
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
                    Game.player.rect.centerx = event.pos[0]
                    Game.player.rect.centery = event.pos[1]

            # Add new bonus at the top of the screen, if needed.
            if not reverseCheat and not slowCheat:
                bonusAddCounter += 1
            if score > 1000:
                Game.bonus.addnewrate = 100
                Game.badegg.addnewrate = 20
            if score > 2000:
                Game.bonus.addnewrate = 200
            if bonusAddCounter == Game.bonus.addnewrate:
                bonusAddCounter = 0
                bonusSize = random.randint(Game.bonus.minsize, Game.bonus.maxsize)
                newBonus = {
                    'rect': pygame.Rect(WINDOWWIDTH - bonusSize, random.randint(0, WINDOWWIDTH - bonusSize),
                                        bonusSize, bonusSize),
                    'speed': random.randint(Game.bonus.minspeed, Game.bonus.maxspeed),
                    'surface': pygame.transform.scale(Game.bonus.image, (bonusSize, bonusSize)),
                }

                BonusCollection.append(newBonus)

            # Add new arbre
            if not reverseCheat and not slowCheat:
                ArbreAddCounter += 1
            if ArbreAddCounter == Game.arbre.addnewrate:
                ArbreAddCounter = 0
                ArbreSize = random.randint(Game.arbre.minsize, Game.arbre.maxsize)
                newTube = {'rect': pygame.Rect(WINDOWWIDTH, WINDOWHEIGHT - ArbreSize, ArbreSize, ArbreSize),
                           'speed': Game.arbre.speed,
                           'surface': pygame.transform.scale(Game.arbre.image, (40, ArbreSize)),
                           }
                TreeCollection.append(newTube)

            # Add new thunder
            if not reverseCheat and not slowCheat:
                ThunderAddCounter += 1
            if ThunderAddCounter == Game.thunder.addnewrate:
                ThunderAddCounter = 0
                ThunderSize = random.randint(Game.thunder.minsize, Game.thunder.maxsize)
                newThunder = {"rect": pygame.Rect(WINDOWWIDTH, -0, ThunderSize, ThunderSize),
                              "speed": Game.thunder.speed,
                              "surface": pygame.transform.scale(Game.thunder.image, (ThunderSize, ThunderSize)),
                              }
                Thunder.append(newThunder)

            # Add new badegg
            if not reverseCheat and not slowCheat:
                BadEggAddCounter += 1
            if BadEggAddCounter == Game.badegg.addnewrate:
                BadEggAddCounter = 0
                BadEggSize = random.randint(Game.badegg.minsize, Game.badegg.maxsize)
                newBadEgg = {'rect': pygame.Rect(WINDOWWIDTH - BadEggSize,
                                                 random.randint(0, WINDOWWIDTH - BadEggSize), BadEggSize,
                                                 BadEggSize),
                             'speed': random.randint(Game.badegg.minspeed, Game.badegg.maxspeed),
                             'surface': pygame.transform.scale(Game.badegg.image, (BadEggSize, BadEggSize)),
                             }

                BadEgg.append(newBadEgg)

            # Move the player around.
            if moveLeft and Game.player.rect.left > 0:
                Game.player.rect.move_ip(-1 * Game.player.MOVERATE, 0)
            if moveRight and Game.player.rect.right < WINDOWWIDTH:
                Game.player.rect.move_ip(Game.player.MOVERATE, 0)
            if moveUp and Game.player.rect.top > 0:
                Game.player.rect.move_ip(0, -1 * Game.player.MOVERATE)
            if moveDown and Game.player.rect.bottom < WINDOWHEIGHT:
                Game.player.rect.move_ip(0, Game.player.MOVERATE)

            # Move the bonus
            for b in BonusCollection:
                if not reverseCheat and not slowCheat:
                    b['rect'].move_ip(-b['speed'], 0)
                elif reverseCheat:
                    b['rect'].move_ip(-5, 0)
                elif slowCheat:
                    b['rect'].move_ip(1, 0)

            # Move the arbre
            for t in TreeCollection:
                if not reverseCheat and not slowCheat:
                    t['rect'].move_ip(-t['speed'], 0)
                elif reverseCheat:
                    t['rect'].move_ip(-5, 0)
                elif slowCheat:
                    t['rect'].move_ip(1, 0)

            # Move the thunder
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

            # Delete bonus that have fallen past the have gone past the screen.
            for b in BonusCollection[:]:
                if -b['rect'].top > WINDOWWIDTH:
                    BonusCollection.remove(b)

            # Delete arbre that have fallen past the have gone past the screen.
            for t in TreeCollection[:]:
                if -t['rect'].top > WINDOWWIDTH:
                    TreeCollection.remove(t)

            # Delete thunder that have fallen past the have gone past the screen.
            for h in Thunder[:]:
                if -h["rect"].top > WINDOWWIDTH:
                    Thunder.remove(h)

            # Delete badegg that have fallen past the have gone past the screen.
            for e in BadEgg[:]:
                if -e['rect'].top > WINDOWWIDTH:
                    BadEgg.remove(e)

            # Background game
            windowSurface.blit(Background, [0, 0])

            # Draw arbre
            for t in TreeCollection:
                windowSurface.blit(t["surface"], t['rect'])

            # Draw Thunder
            for h in Thunder:
                windowSurface.blit(h["surface"], h["rect"])

            # Draw the score and top score.
            fichier = open("data.txt", "r")
            draw_text('Score: %s' % score, font, windowSurface, 10, 0)
            draw_text('Top Score: %s' % (fichier.read()), font, windowSurface, 10, 40)
            draw_text("vie: %s" % vie, font, windowSurface, 10, 80)
            fichier.close()

            # Draw the player's rectangle.
            windowSurface.blit(Game.player.image, Game.player.rect)

            # Draw each bonus.
            for b in BonusCollection:
                windowSurface.blit(b["surface"], b['rect'])

            # Draw each BadEgg.
            for e in BadEgg:
                windowSurface.blit(e["surface"], e['rect'])

            # Check if any of the bonus have hit the player.
            if Game.player_has_hit_bonus(Game.player.rect, BonusCollection):
                element_touche = None
                for b in BonusCollection:
                    if Game.player.rect.colliderect(b['rect']):
                        element_touche = b
                BonusCollection.remove(element_touche)

                PlayerHitGiftEggSound.play()

                bonuss = random.choice([1, 2])  # code to randomize the bonus.
                print(bonuss)
                if bonuss == 1:
                    score += 100
                else:
                    vie += 1

            # Check if any of the arbre have hit the player.
            if Game.player_has_hit_arbre(Game.player.rect, TreeCollection):
                if score > topScore:
                    topScore = score  # set new top score
                    os.remove("data.txt")
                    fichier = open("data.txt", "w")
                    topscore = str(topScore)
                    fichier.write(topscore)
                    fichier.close()
                break

            # Check if any of thunder have hit the player.
            if Game.player_has_hit_thunder(Game.player.rect, Thunder):
                if score > topScore:
                    topScore = score
                    os.remove("data.txt")
                    fichier = open("data.txt", "w")
                    topscore = str(topScore)
                    fichier.write(topscore)
                    fichier.close()
                break

            # Check if any of the badegg have hit the player.
            if Game.player_has_hit_badEgg(Game.player.rect, BadEgg):
                element_touche = None
                for e in BadEgg:
                    if Game.player.rect.colliderect(e['rect']):
                        element_touche = e
                BadEgg.remove(element_touche)

                PlayerHitBadEggSound.play()

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
                    vie = vie - 1

            pygame.display.flip()  # Help to refresh the entire screen
            fpsClock.tick(FPS)  # Help to time the frame per seconds

        # Stop the game and show the "Game Over" screen.
        GameOver = True
        GameOverButton = Button((0, 0, 0), 370, 250, 200, 55, 'Play Again')

        while GameOver:
            GameOverButton.draw(windowSurface, (0, 0, 0))
            pygame.display.flip()

            pygame.mixer.music.stop()
            gameOverSound.play()

            windowSurface.blit(GameOverBackground, [0, 0])
            pygame.mouse.set_visible(True)

            draw_text('GAME OVER', font, windowSurface, 365, 180)

            gameOverSound.stop()

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEMOTION:
                    if GameOverButton.is_over(pos):
                        GameOverButton.color = (150, 150, 150)
                    else:
                        GameOverButton.color = (150, 180, 150)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if GameOverButton.is_over(pos):
                        play()


# Show the start screen.
Run = True
StartButton = Button((0, 0, 0), 370, 220, 145, 60, 'START')
HowToPlayButton = Button((0, 0, 0), 40, 400, 220, 52, 'how to play')

while Run:
    windowSurface.blit(StartBackground, [0, 0])
    StartButton.draw(windowSurface, (0, 0, 0))
    HowToPlayButton.draw(windowSurface, (0, 0, 0))
    pygame.display.flip()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEMOTION:
            if HowToPlayButton.is_over(pos):
                HowToPlayButton.color = (150, 150, 150)
            else:
                HowToPlayButton.color = (10, 190, 255)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if HowToPlayButton.is_over(pos):
                while True:
                    windowSurface.blit(HowToPlayBackground, [0, 0])
                    pygame.display.flip()
                    pygame.time.wait(10000)
                    play()

        if event.type == pygame.MOUSEMOTION:
            if StartButton.is_over(pos):
                StartButton.color = (150, 150, 150)
            else:
                StartButton.color = (255, 255, 255)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if StartButton.is_over(pos):
                play()
