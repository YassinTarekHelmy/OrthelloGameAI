class InputManager:
    _input = (0, 0)

    @staticmethod
    def get_input():
        return InputManager._input

    @staticmethod
    def update_input(input_value):
        InputManager._input = input_value

    @staticmethod
    def update_hovered_index(mouse_pos, board):
        x = mouse_pos[0] - board.padding
        y = mouse_pos[1] - board.top_padding

        col_index = x // board.column_size
        row_index = y // board.row_size

        if 0 <= col_index < board.size and 0 <= row_index < board.size:
            InputManager._input = (row_index, col_index)
