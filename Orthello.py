import pygame


class MainClass(object):
    def __init__(self) -> None:
        pass

    def main(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Orthello')
        pygame.display.flip()

        #game = GameBoard.GameBoard()
        #game.draw(screen)
        rect = pygame.Rect(0, 0, 800, 600)
        pygame.draw.rect(screen, (255, 0, 0), rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            pygame.display.update()
                
mainclass = MainClass() 
mainclass.main()