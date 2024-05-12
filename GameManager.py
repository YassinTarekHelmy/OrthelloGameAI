
import enum
import time

import pygame
from Board import SlotStates
import Game

class BoardStates(enum.Enum):
    BLACK_TURN = 1
    WHITE_TURN = -1
    GAME_OVER = 0


class GameManager(object):
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.board.draw(self.screen)
        self.boardState = BoardStates.BLACK_TURN
        self.Player1Strategy = Game.HumanStrategy(SlotStates.BLACK.value, self.boardState, self)
        self.Player2Strategy = Game.AIStrategy(SlotStates.WHITE.value, self.boardState,self)
        self.players = {BoardStates.BLACK_TURN: self.Player1Strategy, BoardStates.WHITE_TURN: self.Player2Strategy}
        self.CurrentPlayer = self.players[self.boardState]

    def RunGame(self):
        NoValid = 0
        while self.boardState != BoardStates.GAME_OVER:
            self.CurrentPlayer = self.players[self.boardState]
            if len(self.CalculateAvailableMoves(self.board, self.CurrentPlayer.playerColor)) > 0:
                self.CurrentPlayer.Run_Game(self.screen, self.board)
                NoValid = 0
            else:
                NoValid += 1
                if NoValid == 2:
                    self.boardState = BoardStates.GAME_OVER
            self.ChangeTurn()
            self.NotifyPlayers()
            self.CalculateScore(self.board)
            self.board.draw(self.screen)
        self.board.DeclareWinner(self.screen)
        pygame.display.update()
        time.sleep(5)

    
    
    def CalculateFlanks(self, x_pos, y_pos,board, currentColor):
        flanks = []
        opponentColor = SlotStates.WHITE.value if currentColor == SlotStates.BLACK.value else SlotStates.BLACK.value
        
        self.CalculateFlanksUtil(x_pos, y_pos, flanks,[(1,0),(-1,0)],currentColor,opponentColor,board)
        self.CalculateFlanksUtil(x_pos, y_pos, flanks,[(0,1),(0,-1)], currentColor,opponentColor,board)
        self.CalculateFlanksUtil(x_pos, y_pos, flanks,[(1,1),(-1,-1)], currentColor,opponentColor,board)
        return flanks

    def CalculateAvailableMoves(self,board, playerColor):
        self.ResetAvailableMoves(board)
        available = []
        for i in range(board.size):
            for j in range(board.size):
                    if board.board[i][j] == 0:
                        flanks = self.CalculateFlanks(i, j,board,playerColor)
                        if len(flanks) > 0:
                            available.append((i, j))
                            board.UpdateBoard(i, j, SlotStates.AvailableMove.value)
        return available


    def CalculateFlanksUtil(self, x_pos, y_pos, flanks,directions,currentColor,opponentColor, board):
        for dx, dy in directions:
            i = x_pos + dx
            j = y_pos + dy
            tmpFlanks = []
            while 0 <= i < board.size and 0 <= j < board.size and board.board[i][j] == opponentColor:
                tmpFlanks.append((i, j))
                i += dx
                j += dy
            if 0 <= i < board.size and 0 <= j < board.size and board.board[i][j] == currentColor:
                flanks.extend(tmpFlanks)
            else:
                tmpFlanks.clear()



    def ResetAvailableMoves(self,board):
        for i in range(board.size):
            for j in range(self.board.size):
                if board.board[i][j] == SlotStates.AvailableMove.value:
                    board.UpdateBoard(i, j, 0)

            
    def NotifyPlayers(self):
        self.Player1Strategy.UpdateBoardState(self.boardState)
        self.Player2Strategy.UpdateBoardState(self.boardState)

    def ChangeTurn(self):
        if (self.boardState != BoardStates.GAME_OVER):
            self.boardState = BoardStates.WHITE_TURN if self.boardState == BoardStates.BLACK_TURN else BoardStates.BLACK_TURN
    
    def CalculateScore(self,board):
        board.Player1Score = 0
        board.Player2Score = 0
        for i in range(self.board.size):
            for j in range(self.board.size):
                if board.board[i][j] == SlotStates.BLACK.value:
                    board.Player1Score += 1
                elif board.board[i][j] == SlotStates.WHITE.value:
                    board.Player2Score += 1
    
    def PlotFlank(self, x , y ,flanks, playerColor, board):
        for (fx, fy) in flanks:
            board.UpdateBoard(fx, fy, playerColor)
        board.UpdateBoard(x, y, playerColor)