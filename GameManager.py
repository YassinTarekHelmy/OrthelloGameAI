
import enum
import time
import pygame
from Board import Board, SlotStates
import Game

class BoardStates(enum.Enum):
    BLACK_TURN = 1
    WHITE_TURN = -1
    GAME_OVER = 0


# a struct for the player data.
class PlayerData(object):
    def __init__(self, playerColor, playerTokens):
        self.playerColor = playerColor
        self.playerTokens = playerTokens

class GameManager(object):
    def __init__(self, screen, difficulty, isDifficultyDisabled):
        self.screen = screen
        self.boardState = BoardStates.BLACK_TURN

        #Initializing the Players according to the output taken from the start menu screen.
        self.Player1Strategy = Game.HumanStrategy(SlotStates.BLACK.value, self.boardState, self)
        if  isDifficultyDisabled:
            self.Player2Strategy = Game.HumanStrategy(SlotStates.WHITE.value, self.boardState, self)
        else:
            self.Player2Strategy = Game.AIStrategy(SlotStates.WHITE.value, self.boardState,self,difficulty)
        
        #a dictionary to keep track of the players.
        self.players = {BoardStates.BLACK_TURN: self.Player1Strategy, BoardStates.WHITE_TURN: self.Player2Strategy}
        self.board = Board(screen, 8, PlayerData(SlotStates.BLACK.value, 30), PlayerData(SlotStates.WHITE.value, 30))
        self.board.draw(self.screen)
        self.CurrentPlayer = self.players[self.boardState]

    def RunGame(self):
        #main gameplay loop.
        NoValid = 0
        while self.boardState != BoardStates.GAME_OVER:
            self.CurrentPlayer = self.players[self.boardState]
            print(self.board.playerDataRecord[self.CurrentPlayer.playerColor].playerTokens)
            if self.board.playerDataRecord[self.CurrentPlayer.playerColor].playerTokens == 0:
                #if the player has no tokens left then the game is over.
                self.boardState = BoardStates.GAME_OVER
                break
            if len(self.CalculateAvailableMoves(self.board, self.CurrentPlayer.playerColor)) > 0:
                self.CurrentPlayer.Run_Game(self.screen, self.board)
                NoValid = 0
            else:
                #if this turn was skipped.
                NoValid += 1
                if NoValid == 2:
                    #if two turns were skipped then the game is over.
                    self.boardState = BoardStates.GAME_OVER
            self.ChangeTurn()
            self.NotifyPlayers()
            self.CalculateScore(self.board)
            self.board.draw(self.screen)
        self.board.DeclareGameState(self.screen)
        pygame.display.update()
        time.sleep(5)

    
    #calculating out flanks.
    def CalculateFlanks(self, x_pos, y_pos,board, currentColor):
        flanks = []
        opponentColor = SlotStates.WHITE.value if currentColor == SlotStates.BLACK.value else SlotStates.BLACK.value
        
        #horizontal direction.
        self.CalculateFlanksUtil(x_pos, y_pos, flanks,[(1,0),(-1,0)],currentColor,opponentColor,board)
        
        #vertical direction.
        self.CalculateFlanksUtil(x_pos, y_pos, flanks,[(0,1),(0,-1)], currentColor,opponentColor,board)
        
        #diagonal direction.
        #self.CalculateFlanksUtil(x_pos, y_pos, flanks,[(1,1),(-1,-1)], currentColor,opponentColor,board)

        #opposite diagonal direction.
        #self.CalculateFlanksUtil(x_pos, y_pos, flanks,[(1,-1),(-1,1)], currentColor,opponentColor,board)
        return flanks

    #calculating the available moves for the player.
    def CalculateAvailableMoves(self,board, playerColor):
        self.ResetAvailableMoves(board)
        available = []
        #if we found a free slot that if we added our color to it to would  form an out flank then
        #this is an available move, append it to the list and also update the board that this is an
        #available move.
        for i in range(board.size):
            for j in range(board.size):
                    if board.board[i][j] == 0:
                        flanks = self.CalculateFlanks(i, j,board,playerColor)
                        if len(flanks) > 0:
                            available.append((i, j))
                            board.UpdateBoard(i, j, SlotStates.AvailableMove.value)
        return available


    #the Utility function to calculate the flanks.
    def CalculateFlanksUtil(self, x_pos, y_pos, flanks,directions,currentColor,opponentColor, board):
        #it adapts the idea of change in x and y to get the flanks in the horizontal, vertical and diagonal directions.
        for dx, dy in directions:
            i = x_pos + dx
            j = y_pos + dy
            tmpFlanks = []
            #as long as i am on the opponent's color and didn't go outside the board,then i will go on.
            while 0 <= i < board.size and 0 <= j < board.size and board.board[i][j] == opponentColor:
                tmpFlanks.append((i, j))
                i += dx     #changing the x direction.
                j += dy     #changing the y direction.
            
            #if i am on the current player's color then i will add the flanks to the list.
            if 0 <= i < board.size and 0 <= j < board.size and board.board[i][j] == currentColor:
                flanks.extend(tmpFlanks)
            # any other option means that i reached a dead end that is not a flank. so clear the list
            # and start finding another flank.
            else:
                tmpFlanks.clear()



    def ResetAvailableMoves(self,board):
        for i in range(board.size):
            for j in range(self.board.size):
                if board.board[i][j] == SlotStates.AvailableMove.value:
                    board.UpdateBoard(i, j, 0)


    #updating the players with the new game state.
    def NotifyPlayers(self):
        self.Player1Strategy.UpdateBoardState(self.boardState)
        self.Player2Strategy.UpdateBoardState(self.boardState)

    def ChangeTurn(self):
        if (self.boardState != BoardStates.GAME_OVER):
            self.boardState = BoardStates.WHITE_TURN if self.boardState == BoardStates.BLACK_TURN else BoardStates.BLACK_TURN
    
    #calculating the score of the players through counting colors.
    def CalculateScore(self,board):
        board.Player1Score = 0
        board.Player2Score = 0
        for i in range(self.board.size):
            for j in range(self.board.size):
                if board.board[i][j] == SlotStates.BLACK.value:
                    board.Player1Score += 1
                elif board.board[i][j] == SlotStates.WHITE.value:
                    board.Player2Score += 1
    
    # the function responsible for plotting a flank.
    def PlotFlank(self, x , y ,flanks, playerColor, board):
        for (fx, fy) in flanks:
            board.UpdateBoard(fx, fy, playerColor)
        board.UpdateBoard(x, y, playerColor)

    
