
import enum
import Board
from InputManager import InputManager

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
        self.playerColor = Board.SlotStates.BLACK.value
    def CalculateFlanks(self, x_pos, y_pos):
        flanks = []
        opponentColor = Board.SlotStates.WHITE.value if self.playerColor == Board.SlotStates.BLACK.value else Board.SlotStates.BLACK.value
        
        flanks = self.CalculateHorizontalFlanks(x_pos, y_pos, flanks, opponentColor)
        flanks = self.CalculateVerticalFlanks(x_pos, y_pos, flanks, opponentColor)

        return flanks


    def CalculateAvailableMoves(self):
        self.ResetAvailableMoves()
        found_flank = False
        for i in range(self.board.size):
            for j in range(self.board.size):
                    if self.board.board[i][j] == 0:
                        flanks = self.CalculateFlanks(i, j)
                        if len(flanks) > 0:
                            self.board.UpdateBoard(i, j, Board.SlotStates.AvailableMove.value)
                            found_flank = True

        return found_flank

    def OnCellClicked(self):
        print(self.boardState)

        (x_pos, y_pos) = InputManager.get_input()

        if (self.board.board[y_pos][x_pos] != Board.SlotStates.AvailableMove.value):
            return
        
        self
        flanks = self.CalculateFlanks(y_pos, x_pos)
        
        for (x, y) in flanks:
            self.board.UpdateBoard(x, y, self.playerColor)

        self.board.UpdateBoard(y_pos, x_pos, self.playerColor)
        self.ChangeTurn()
        self.CalculateAvailableMoves()

    def CheckClosedTurn(self):
        pass
        
    def ChangeTurn(self):
        self.boardState = BoardStates.WHITE_TURN if self.boardState == BoardStates.BLACK_TURN else BoardStates.BLACK_TURN
        self.playerColor = Board.SlotStates.BLACK.value if self.playerColor == Board.SlotStates.WHITE.value else Board.SlotStates.WHITE.value

    def CalculateHorizontalFlanks(self, x_pos, y_pos, flanks, opponentColor):
        for i in range(x_pos + 1, self.board.size):
            if i >= self.board.size or self.board.board[i][y_pos] != opponentColor:
                break
            if self.board.board[i][y_pos] == self.playerColor:
                flanks.append((i, y_pos))
                break
            flanks.append((i, y_pos))

        for i in range(x_pos - 1, -1, -1):
            if i < 0 or self.board.board[i][y_pos] != opponentColor:
                break
            if self.board.board[i][y_pos] == self.playerColor:
                flanks.append((i, y_pos))
                break
            flanks.append((i, y_pos))
        
        return flanks
    
    def CalculateVerticalFlanks(self, x_pos, y_pos, flanks, opponentColor):
        for i in range(y_pos + 1, self.board.size):
            if i >= self.board.size or self.board.board[x_pos][i] != opponentColor:
                break
            if self.board.board[x_pos][i] == self.playerColor:
                flanks.append((x_pos, i))
                break
            flanks.append((x_pos, i))

        for i in range(y_pos - 1, -1, -1):
            if i < 0 or self.board.board[x_pos][i] != opponentColor:
                break
            if self.board.board[x_pos][i] == self.playerColor:
                flanks.append((x_pos, i))
                break
            flanks.append((x_pos, i))
        
        return flanks

    def ResetAvailableMoves(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i][j] == Board.SlotStates.AvailableMove.value:
                    self.board.UpdateBoard(i, j, 0)