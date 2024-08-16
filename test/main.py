import sys, os
import pygame
import theta

game = theta.Game(1000, 800, 60)

while True:
    for event in game.input.get():
        match event.type:
            case theta.input.QUIT:
                pygame.quit()
                sys.exit()
    game.update()

