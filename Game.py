
import random
import time
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
    def __init__(self,playerColor,boardState, gameManager, depth):
        GameStrategy.__init__(self, playerColor, boardState, gameManager)
        self.depth = depth
    def Run_Game(self,screen,board,depth = 3):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        self.MakeMove(board,depth)
        GameStrategy.Run_Game(self, screen, board)

    def MakeMove(self, board, depth):
        bestVal = -1000
        worstVal = 1000
        bestMove = None
        opponentColor = Board.SlotStates.WHITE.value if self.playerColor == Board.SlotStates.BLACK.value else Board.SlotStates.BLACK.value
        available = self.gameManager.CalculateAvailableMoves(board, self.playerColor)
        if len(available) > 0:
            for (x, y) in available:
                simulationBoard = board.CopyBoard()
                flanks = self.gameManager.CalculateFlanks(x, y, simulationBoard, self.playerColor)
                self.gameManager.PlotFlank(x, y, flanks ,self.playerColor, simulationBoard)                
                value = self.AlphaBetaBruining(simulationBoard, opponentColor, depth - 1, bestVal, worstVal)
                if value > bestVal:
                    bestVal = value
                    bestMove = (x, y)
        if bestMove is not None:
            flanks = self.gameManager.CalculateFlanks(bestMove[0], bestMove[1], board, self.playerColor)
            self.gameManager.PlotFlank(bestMove[0], bestMove[1],flanks,self.playerColor, board)
            time.sleep(1)
        return bestMove


    def AlphaBetaBruining(self, board, playerColor, depth, alpha, beta):
        if depth == 0:
            self.gameManager.CalculateScore(board)
            return board.Player2Score - board.Player1Score
        if playerColor == self.playerColor:
            opponentColor = Board.SlotStates.WHITE.value if playerColor == Board.SlotStates.BLACK.value else Board.SlotStates.BLACK.value
            bestValue = -1000
            available = self.gameManager.CalculateAvailableMoves(board, playerColor)
            if len(available) > 0:
                for (x, y) in available:
                    flanks = self.gameManager.CalculateFlanks(x, y, board, playerColor)
                    simulationBoard = board.CopyBoard()
                    self.gameManager.PlotFlank(x, y,flanks ,playerColor, simulationBoard)
                    value = self.AlphaBetaBruining(simulationBoard, opponentColor, depth - 1, alpha, beta)
                    bestValue = max(bestValue, value)
                    alpha = max(alpha, bestValue)
                    if beta <= alpha:
                        break        
            return bestValue
        else:
            opponentColor = Board.SlotStates.WHITE.value if playerColor == Board.SlotStates.BLACK.value else Board.SlotStates.BLACK.value
            bestValue = 1000
            available = self.gameManager.CalculateAvailableMoves(board, playerColor)
            if len(available) > 0:
                for (x, y) in available:
                    
                    flanks = self.gameManager.CalculateFlanks(x, y, board, playerColor)
                    simulationBoard = board.CopyBoard()
                    self.gameManager.PlotFlank(x, y,flanks ,playerColor, simulationBoard)
                    value = self.AlphaBetaBruining(simulationBoard, opponentColor, depth - 1, alpha, beta)    
                    bestValue = min(bestValue, value)
                    beta = min(beta, bestValue)
                    if beta <= alpha:
                        break
            return bestValue

        
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

    def OnCellClicked(self,board):
        (x_pos, y_pos) = InputManager.InputManager.get_input()

        if (board.board[y_pos][x_pos] != Board.SlotStates.AvailableMove.value):
            return False
        
        flanks = self.gameManager.CalculateFlanks(y_pos, x_pos,board, self.playerColor)
        
        for (x, y) in flanks:
            board.UpdateBoard(x, y, self.playerColor)

        board.UpdateBoard(y_pos, x_pos, self.playerColor)
        return True
