
import enum
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
        while self.boardState != BoardStates.GAME_OVER:
            self.CurrentPlayer = self.players[self.boardState]
            self.CalculateAvailableMoves()
            self.CurrentPlayer.Run_Game(self.screen, self.board)
            self.CalculateBoardState()
            self.ChangeTurn()
            self.NotifyPlayers()
    
    
    def CalculateFlanks(self, x_pos, y_pos,board):
        flanks = []
        opponentColor = SlotStates.WHITE.value if self.CurrentPlayer.playerColor == SlotStates.BLACK.value else SlotStates.BLACK.value
        
        flanks = self.CalculateHorizontalFlanks(x_pos, y_pos, flanks, opponentColor,board)
        flanks = self.CalculateVerticalFlanks(x_pos, y_pos, flanks, opponentColor,board)

        return flanks

    def CalculateAvailableMoves(self):
        self.ResetAvailableMoves(self.board)
        found_flank = False
        for i in range(self.board.size):
            for j in range(self.board.size):
                    if self.board.board[i][j] == 0:
                        flanks = self.CalculateFlanks(i, j,self.board)
                        if len(flanks) > 0:
                            self.board.UpdateBoard(i, j, SlotStates.AvailableMove.value)
                            found_flank = True

        return found_flank

        
    def CalculateHorizontalFlanks(self, x_pos, y_pos, flanks, opponentColor, board):
        for dx, dy in [(1, 0), (-1, 0)]: 
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

        return flanks

    def CalculateVerticalFlanks(self, x_pos, y_pos, flanks, opponentColor, board):
        for dx, dy in [(0, 1), (0, -1)]:
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

        return flanks


    def ResetAvailableMoves(self, board):
        for i in range(board.size):
            for j in range(board.size):
                if board.board[i][j] == SlotStates.AvailableMove.value:
                    board.UpdateBoard(i, j, 0)

            
    def NotifyPlayers(self):
        self.Player1Strategy.UpdateBoardState(self.boardState)
        self.Player2Strategy.UpdateBoardState(self.boardState)

    def ChangeTurn(self):
        self.boardState = BoardStates.WHITE_TURN if self.boardState == BoardStates.BLACK_TURN else BoardStates.BLACK_TURN

    def CalculateBoardState(self):
        if not self.CalculateAvailableMoves():
            self.ChangeTurn()
            if not self.CalculateAvailableMoves():
                self.boardState = BoardStates.GAME_OVER
                self.CurrentPlayer.Run_Game(self.screen, self.board)
                print("Game Over")
                return
        else:
            return
    