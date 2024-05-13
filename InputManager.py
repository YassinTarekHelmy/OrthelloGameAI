class InputManager:
    _input = (0, 0)

    @staticmethod
    def get_input():
        return InputManager._input

    @staticmethod
    def update_input(input_value):
        InputManager._input = input_value

    @staticmethod

    #getting the exact coordinate on board that the mouse is on.
    def update_hovered_index(mouse_pos, board):
        #subtracting the padding to get the exact position on the board.
        x = mouse_pos[0] - board.padding
        y = mouse_pos[1] - board.top_padding

        #dividing the x and y by the size of the column and row to get the exact index.
        col_index = x // board.column_size
        row_index = y // board.row_size

        #as long as the index is within the board size then update the input.
        if 0 <= col_index < board.size and 0 <= row_index < board.size:
            InputManager._input = (col_index, row_index)
