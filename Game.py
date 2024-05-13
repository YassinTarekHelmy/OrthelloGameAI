
import time
import Board
import pygame
import InputManager


#we decided that we want to use Strategy for this game, so we created a class called GameStrategy
#this class is the parent class for the HumanStrategy and AIStrategy classes.
#this class has the Run_Game function that is responsible for running the turn and updating the board.
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



#the AIStrategy class is a child class of the GameStrategy class.
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
        #getting the available moves for the player.
        available = self.gameManager.CalculateAvailableMoves(board, self.playerColor)
        if len(available) > 0:
            for (x, y) in available:
                #creating a simulation board to simulate the moves as to pick the best out of them to apply
                #to the main board.

                simulationBoard = board.CopyBoard()

                #getting the flanks for the a single token.
                flanks = self.gameManager.CalculateFlanks(x, y, simulationBoard, self.playerColor)
                self.gameManager.PlotFlank(x, y, flanks ,self.playerColor, simulationBoard)
                simulationBoard.ReduceTokens(self.playerColor)        
                
                #the recursive function to get the value of the play.        
                value = self.AlphaBetaBruining(simulationBoard, opponentColor, depth - 1, bestVal, worstVal)
                
                #If we have a value that is better that what we already discoverd then this is our new best move.
                if value > bestVal:
                    bestVal = value
                    bestMove = (x, y)
        if bestMove is not None:
            #apply the best move to the main board.
            flanks = self.gameManager.CalculateFlanks(bestMove[0], bestMove[1], board, self.playerColor)
            self.gameManager.PlotFlank(bestMove[0], bestMove[1],flanks,self.playerColor, board)
            
            #this is to reduce the time of the Ai Play to know what is he doing.
            time.sleep(1) 

            #reduce the tokens of the current player.
            board.playerDataRecord[self.playerColor].playerTokens -= 1
        return bestMove


    #the recursive function.
    def AlphaBetaBruining(self, board, playerColor, depth, alpha, beta):
        # a simulated game ends if the depth is equal to 0 or if one of the players has no tokens.
        if depth == 0 or board.player1Data.playerTokens == 0 or board.player2Data.playerTokens == 0:
            #score is our utility function there was a way to do it statistically but it was going to be
            #too much work.
            
            self.gameManager.CalculateScore(board)
            return board.Player2Score - board.Player1Score
        
        #if the player is the current player then we want to maximize the value.
        if playerColor == self.playerColor:
            opponentColor = Board.SlotStates.WHITE.value if playerColor == Board.SlotStates.BLACK.value else Board.SlotStates.BLACK.value
            bestValue = -1000

            #same as what we did above.
            available = self.gameManager.CalculateAvailableMoves(board, playerColor)
            if len(available) > 0:
                for (x, y) in available:
                    flanks = self.gameManager.CalculateFlanks(x, y, board, playerColor)
                    simulationBoard = board.CopyBoard()
                    self.gameManager.PlotFlank(x, y,flanks ,playerColor, simulationBoard)
                    simulationBoard.ReduceTokens(playerColor)
                    value = self.AlphaBetaBruining(simulationBoard, opponentColor, depth - 1, alpha, beta)
                    bestValue = max(bestValue, value)
                    alpha = max(alpha, bestValue)
                    if beta <= alpha:   #pruning the tree.
                        break        
            return bestValue
        else:
            # here we want to minimize the opponent.
            opponentColor = Board.SlotStates.WHITE.value if playerColor == Board.SlotStates.BLACK.value else Board.SlotStates.BLACK.value
            bestValue = 1000
            
            #same as what we did above.
            available = self.gameManager.CalculateAvailableMoves(board, playerColor)
            if len(available) > 0:
                for (x, y) in available:
                    flanks = self.gameManager.CalculateFlanks(x, y, board, playerColor)
                    simulationBoard = board.CopyBoard()
                    self.gameManager.PlotFlank(x, y,flanks ,playerColor, simulationBoard)
                    simulationBoard.ReduceTokens(playerColor)
                    value = self.AlphaBetaBruining(simulationBoard, opponentColor, depth - 1, alpha, beta)    
                    bestValue = min(bestValue, value)
                    beta = min(beta, bestValue)
                    if beta <= alpha:
                        break
            return bestValue

        
class HumanStrategy(GameStrategy):
    def Run_Game(self,screen,board):
        isTurnOver = False
        #handling the event of the player.
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #this isthe one that is responsible for the player to click on the board.
                    #and the play to be applied.
                    if self.OnCellClicked(board):

                        #if he plays mark the turn as over.
                        isTurnOver = True

            #update my mouse hovering effect each frame.
            InputManager.InputManager.update_hovered_index(pygame.mouse.get_pos(), board)
            GameStrategy.Run_Game(self, screen, board)
            if isTurnOver:
                #the player played.
                break

    def OnCellClicked(self,board):
        #getting the mouse position in the form of indicies on the board.
        (x_pos, y_pos) = InputManager.InputManager.get_input()

        if (board.board[y_pos][x_pos] != Board.SlotStates.AvailableMove.value):
            return False
        
        
        flanks = self.gameManager.CalculateFlanks(y_pos, x_pos,board, self.playerColor)
        
        #plotting the flanks on board.
        self.gameManager.PlotFlank(y_pos, x_pos, flanks, self.playerColor, board)
        board.playerDataRecord[self.playerColor].playerTokens -= 1
        return True
