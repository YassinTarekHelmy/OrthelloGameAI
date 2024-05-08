import Board
import pygame
import InputManager


class MainClass(object):
    def __init__(self) -> None:
        pass

    def main(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Othello')
        pygame.display.flip()

        
        board = Board.Board(screen,8)
        board.UpdateBoard(2,2,Board.SlotStates.BLACK.value) 
        board.UpdateBoard(1,2,Board.SlotStates.WHITE.value)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            InputManager.InputManager.update_hovered_index(pygame.mouse.get_pos(), board)
            board.draw(screen)
            pygame.display.update()
                
mainclass = MainClass() 
mainclass.main()
