import Board
import pygame
import InputManager

class GameStrategy(object):
    def __init__(self,playerColor,boardState, gameManager):
        self.playerColor = playerColor
        self.boardState = boardState
        self.gameManager = gameManager
    
    def Run_Game(self,screen,board):
        board.draw(screen)
        pygame.display.update()


    def UpdateBoardState(self, boardState):
        self.boardState = boardState




class AIStrategy(GameStrategy):
    def Run_Game(self,screen,board):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        self.MakeMove(board)
        GameStrategy.Run_Game(self, screen, board)


    def MakeMove(self,board):
        print("AI is making a move")

class HumanStrategy(GameStrategy):
    def Run_Game(self,screen,board):
        isTurnOver = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.OnCellClicked(board):
                        isTurnOver = True

            InputManager.InputManager.update_hovered_index(pygame.mouse.get_pos(), board)
            GameStrategy.Run_Game(self, screen, board)
            if isTurnOver:
                break


    def MakeMove(self,board):
        pass

    def OnCellClicked(self,board):
        (x_pos, y_pos) = InputManager.InputManager.get_input()

        if (board.board[y_pos][x_pos] != Board.SlotStates.AvailableMove.value):
            return False
        
        self
        flanks = self.gameManager.CalculateFlanks(y_pos, x_pos,board)
        
        for (x, y) in flanks:
            board.UpdateBoard(x, y, self.playerColor)

        board.UpdateBoard(y_pos, x_pos, self.playerColor)
        return True