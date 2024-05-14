
import pygame
import enum
import InputManager
import copy

class SlotStates(enum.Enum):
    AvailableMove = -2
    WHITE = -1
    BLACK = 1



class Board:
    def __init__(self,screen,size,player1Data,player2Data):
        self.Player1Score = 0
        self.Player2Score = 0
        self.player1Data = player1Data
        self.player2Data = player2Data
        self.playerDataRecord  = {player1Data.playerColor:player1Data,player2Data.playerColor:player2Data}
        self.screen = screen
        self.size = size
        
        #initializing the board.
        self.board = [[0 for _ in range(size)] for _ in range(size)]

        #adding the base of the board.
        self.board[size//2][size//2] = SlotStates.BLACK.value
        self.board[size//2-1][size//2-1] = SlotStates.BLACK.value
        self.board[size//2][size//2-1] = SlotStates.WHITE.value
        self.board[size//2-1][size//2] = SlotStates.WHITE.value

        #refining the look of the board.
        self.border_thickness = 5
        self.circle_border_thickness = 2
        self.padding = 35  # padding from screen edges
        self.top_padding = screen.get_height() // 7
        self.board_width = screen.get_width() - 2 * self.padding
        self.board_height = screen.get_height() - (self.padding + self.top_padding)
        self.column_size = self.board_width // self.size
        self.row_size = self.board_height // self.size

        self.background_color = (4, 175, 112)
        self.border_color = (30, 105, 50)
        self.border_around_tokens = (172, 225, 175)
        self.available_move_color = (5, 237, 152)
        self.hover_color = (5, 237, 152)

    #this function handles the entire drawing of the board and is being called each frame from the game loop
    #to keep up with every thing that is changed in the board.
    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, pygame.Rect(0,0,screen.get_width(), screen.get_height()))  # Draw background
        # Draw border around the board
        pygame.draw.rect(screen, self.border_color, pygame.Rect(self.padding, self.top_padding, self.board_width, self.board_height), self.border_thickness)
        
        self.DrawScore(screen)
        self.DrawMouseHover(screen)
        self.DrawGrid(screen)
        self.SetTokens(screen)


    def get_board(self):
        return self.board
    
    def SetScore(self, player1Score, player2Score):
        self.Player1Score = player1Score
        self.Player2Score = player2Score

    def UpdateBoard(self ,row, col, slotStates):
            self.board[row][col] = slotStates
        

    def DrawGrid(self, screen):
        #starting from the side padding and drawing the horizontal lines.
        for i in range(self.size + 1):
            x = self.padding + i * self.column_size
            pygame.draw.line(screen, self.border_color, (x, self.top_padding), (x, self.top_padding + self.board_height), 2)

        #starting from the top padding and drawing the vertical lines.
        for i in range(self.size + 1):
            y = self.top_padding + i * self.row_size
            pygame.draw.line(screen, self.border_color, (self.padding, y), (self.padding + self.board_width, y), 2)

    def DeclareWinner(self, screen):
        if (self.Player1Score > self.Player2Score):
            self.DrawWinner(screen, "Player 1", (0,0,0))
        elif (self.Player1Score == self.Player2Score):
            self.DrawWinner(screen, "It's a Tie", (127,127,127))
        else:
            self.DrawWinner(screen, "Player 2", (255,255,255))

    def DrawWinner(self,screen,winner, color):
        font = pygame.font.Font(None, 36)
        text = font.render(winner + " wins!", True, color)
        screen.blit(text, (self.padding + 300, 30))
        pygame.display.flip()

    def SetTokens(self, screen):
        for row in range(self.size):
            for col in range(self.size):
                circle_x = col * self.column_size + self.column_size // 2 + self.padding
                circle_y = row * self.row_size + self.row_size // 2 + self.top_padding
                is_token = False

                if self.board[row][col] == SlotStates.BLACK.value:
                    color = (0, 0, 0)
                    is_token = True
                elif self.board[row][col] == SlotStates.WHITE.value:
                    color = (255, 255, 255)
                    is_token = True
                elif self.board[row][col] == SlotStates.AvailableMove.value:
                    color = (55, 251, 179)
                    pygame.draw.circle(screen, self.border_around_tokens, (circle_x, circle_y), 20, self.circle_border_thickness)
                    pygame.draw.circle(screen, self.available_move_color, (circle_x, circle_y), 20, 0)
                
                if (is_token):
                    pygame.draw.circle(screen, self.border_around_tokens, (circle_x, circle_y), 20, self.circle_border_thickness)
                    pygame.draw.circle(screen, color, (circle_x, circle_y), 20, 0)

    # drawing the Mouse hover on the screen by getting the position of the mouse and calculating the position.
    def DrawMouseHover(self, screen):
        (x_pos,y_pos) = InputManager.InputManager.get_input()
        x_Rect = x_pos * self.column_size + self.padding
        y_Rect = y_pos * self.row_size + self.top_padding

        pygame.draw.rect(screen, self.hover_color, pygame.Rect(x_Rect, y_Rect, self.column_size, self.row_size))

    def DrawScore(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render("Player 1: " + str(self.Player1Score), True, (0, 0, 0))
        screen.blit(text, (self.padding, 10))

        text = font.render("Player 2: " + str(self.Player2Score), True, (0, 0, 0))
        screen.blit(text, (self.padding, 40))
    
    def PrintBoard(self):
        for row in self.board:
            for col in row:
                if col == SlotStates.AvailableMove.value:
                    print("A", end=" ")
                elif col == SlotStates.BLACK.value:
                    print("B", end=" ")
                elif col == SlotStates.WHITE.value:
                    print("W", end=" ")
                else:
                    print("0", end=" ")
            print("\n")
        
    def CopyBoard(self):
        copied_board = copy.deepcopy(self)
        return copied_board

    def ReduceTokens(self,playerColor):
        self.playerDataRecord[playerColor].playerTokens -= 1
                    
               
