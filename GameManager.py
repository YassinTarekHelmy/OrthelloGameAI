
import enum
import time
from Board import Board, SlotStates
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
        self.Player2Strategy = Game.HumanStrategy(SlotStates.WHITE.value, self.boardState,self)
        self.players = {BoardStates.BLACK_TURN: self.Player1Strategy, BoardStates.WHITE_TURN: self.Player2Strategy}
        self.CurrentPlayer = self.players[self.boardState]

    def RunGame(self):
        while True:
            self.CurrentPlayer = self.players[self.boardState]
            if self.CalculateAvailableMoves():
                self.CurrentPlayer.Run_Game(self.screen, self.board)
                self.board.PrintBoard()
            else:
                self.ChangeTurn() 
                if not self.CalculateAvailableMoves():
                    break 
                else:
                    self.CurrentPlayer.Run_Game(self.screen, self.board)
                    self.board.PrintBoard()
            self.ChangeTurn()
            self.CalculateScore()
            self.NotifyPlayers()
        self.board.DeclareWinner(self.screen)
        time.sleep(5)

    
    
    def CalculateFlanks(self, x_pos, y_pos,board):
        flanks = []
        opponentColor = SlotStates.WHITE.value if self.CurrentPlayer.playerColor == SlotStates.BLACK.value else SlotStates.BLACK.value
        
        self.CalculateFlanksUtil(x_pos, y_pos, flanks,[(1,0),(-1,0)], opponentColor,board)
        self.CalculateFlanksUtil(x_pos, y_pos, flanks,[(0,1),(0,-1)], opponentColor,board)
        self.CalculateFlanksUtil(x_pos, y_pos, flanks,[(1,1),(-1,-1)], opponentColor,board)

        return flanks

    def CalculateAvailableMoves(self):
        self.ResetAvailableMoves()
        found_flank = False
        for i in range(self.board.size):
            for j in range(self.board.size):
                    if self.board.board[i][j] == 0:
                        flanks = self.CalculateFlanks(i, j,self.board)
                        if len(flanks) > 0:
                            self.board.UpdateBoard(i, j, SlotStates.AvailableMove.value)
                            found_flank = True

        return found_flank


    def CalculateFlanksUtil(self, x_pos, y_pos, flanks,directions,opponentColor, board):
        for dx, dy in directions:
            i = x_pos + dx
            j = y_pos + dy
            tmpFlanks = []
            while 0 <= i < board.size and 0 <= j < board.size and board.board[i][j] == opponentColor:
                tmpFlanks.append((i, j))
                i += dx
                j += dy
            if 0 <= i < board.size and 0 <= j < board.size and board.board[i][j] == self.CurrentPlayer.playerColor:
                flanks.extend(tmpFlanks)
            else:
                tmpFlanks.clear()



    def ResetAvailableMoves(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i][j] == SlotStates.AvailableMove.value:
                    self.board.UpdateBoard(i, j, 0)

            
    def NotifyPlayers(self):
        self.Player1Strategy.UpdateBoardState(self.boardState)
        self.Player2Strategy.UpdateBoardState(self.boardState)

    def ChangeTurn(self):
        self.boardState = BoardStates.WHITE_TURN if self.boardState == BoardStates.BLACK_TURN else BoardStates.BLACK_TURN
    
    def CalculateScore(self):
        self.board.Player1Score = 0
        self.board.Player2Score = 0
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i][j] == SlotStates.BLACK.value:
                    self.board.Player1Score += 1
                elif self.board.board[i][j] == SlotStates.WHITE.value:
                    self.board.Player2Score += 1