import pygame
from utils import *
  
def main():
    # init game
    window, flag = game_init()

    if not flag:
        pygame.time.delay(1000)
        pygame.quit()
        quit()

    # Game loop
    while True:
        # Check for event if user has pushed any event in queue
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_RETURN:
                    game_start(window)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

if __name__ == "__main__":
    main()