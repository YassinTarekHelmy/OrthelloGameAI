import Board
import pygame
import InputManager
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
        game_manager.CalculateAvailableMoves()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    game_manager.OnCellClicked()

            InputManager.InputManager.update_hovered_index(pygame.mouse.get_pos(), game_manager.board)
            game_manager.board.draw(screen)
            pygame.display.update()
                
mainclass = MainClass() 
mainclass.main()
