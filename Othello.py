import Board
import pygame
import GameManager

class MainClass(object):
    def __init__(self) -> None:
        pass

    def main(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Othello')
        pygame.display.flip()

        game_manager = GameManager.GameManager(screen, Board.Board(screen, 8))
        
        game_manager.RunGame()

                
mainclass = MainClass() 
mainclass.main()
