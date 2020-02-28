import pygame
import os
import os 
import sys
import io
import pygame
from lol_winrates.main import Window

if __name__ == '__main__':
	pygame.init()
	win = pygame.display.set_mode((960, 540))
	start = Window(win)
	pygame.display.set_caption('LoL Tierlist Tool')

	pygame.display.set_icon(start.icon)
	start.run()