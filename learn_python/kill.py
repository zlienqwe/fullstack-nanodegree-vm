import pygame
from pygame.locals import *

def main():
	screen = pygame.display.set_mode((480, 800))

	pygame.display.set_caption("my game")

	clock = pygame.time.Clock()

	bg = pygame.image.load('images/background.png').convert()
	plane = pygame.image.load('images/plane.png').convert_alpha()

	while True:
		
		clock.tick(30)

		screen.blit(bg, (0, 0))

		(x, y) = pygame.mouse.get_pos()

		x -= plane.get_width() / 2
		y -= plane.get_height() / 2

		screen.blit(plane, (x, y))

		for event in pygame.event.get():
			if event.type == QUIT:
				return

		pygame.display.update()



if __name__ == "__main__":
	main()