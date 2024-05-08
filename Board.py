
import pygame
import enum
import InputManager

class SlotStates(enum.Enum):
    AvailableMove = -2
    WHITE = -1
    BLACK = 1
    

class Board:
    def __init__(self,screen,size):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.board[size//2][size//2] = SlotStates.BLACK.value
        self.board[size//2-1][size//2-1] = SlotStates.BLACK.value
        self.board[size//2][size//2-1] = SlotStates.WHITE.value
        self.board[size//2-1][size//2] = SlotStates.WHITE.value

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
        self.hover_color = (255, 255, 255, 50)
    def draw(self, screen):

       
        pygame.draw.rect(screen, self.background_color, pygame.Rect(0,0,screen.get_width(), screen.get_height()))  # Draw background
        # Draw border around the board
        pygame.draw.rect(screen, self.border_color, pygame.Rect(self.padding, self.top_padding, self.board_width, self.board_height), self.border_thickness)

        for i in range(self.size + 1):
            x = self.padding + i * self.column_size
            pygame.draw.line(screen, self.border_color, (x, self.top_padding), (x, self.top_padding + self.board_height), 2)

        for i in range(self.size + 1):
            y = self.top_padding + i * self.row_size
            pygame.draw.line(screen, self.border_color, (self.padding, y), (self.padding + self.board_width, y), 2)

         
        (x_pos,y_pos) = InputManager.InputManager.get_input()
        
        x_Rect = x_pos * self.column_size + self.column_size // 2 + self.padding - self.row_size // 2
        y_Rect = y_pos * self.row_size + self.row_size // 2 + self.top_padding - self.column_size // 2
        pygame.draw.rect(screen, self.hover_color, pygame.Rect(y_Rect, x_Rect, self.column_size, self.row_size))


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
                    color = (0, 0, 0)
                    pygame.draw.circle(screen, self.border_around_tokens, (circle_x, circle_y), 20, self.circle_border_thickness)
                    pygame.draw.circle(screen, self.available_move_color, (circle_x, circle_y), 20, 0)
                if (is_token):
                    pygame.draw.circle(screen, self.border_around_tokens, (circle_x, circle_y), 20, self.circle_border_thickness)
                    pygame.draw.circle(screen, color, (circle_x, circle_y), 20, 0)
    def get_board(self):
        return self.board
    
    def UpdateBoard(self ,row, col, slotStates):
        if (slotStates == SlotStates.BLACK.value):
            self.board[row][col] = SlotStates.BLACK.value
        elif (slotStates == SlotStates.WHITE.value):
            self.board[row][col] = SlotStates.WHITE.value
        elif (slotStates == SlotStates.AvailableMove.value):
            self.board[row][col] = SlotStates.AvailableMove.value
        
        
        

                    
               
