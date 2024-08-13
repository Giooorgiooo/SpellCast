class Cell:
    def __init__(self, value: str, x: int, y: int, flag: str, can_swap: bool) -> None:
        """
        Initialize a cell on the board.

        :param value: The character value of the cell (e.g., 'a', 'b', 'c', etc.).
        :param x: The x-coordinate (column index) of the cell on the board.
        :param y: The y-coordinate (row index) of the cell on the board.
        :param flag: A special flag associated with the cell, used for scoring or other purposes.
        :param can_swap: A boolean indicating whether the cell's value can be swapped.
        """
        self.value: str = value       # The character value of the cell
        self.flag: str = flag         # A flag associated with the cell (e.g., for multipliers in scoring)
        self.x: int = x               # The x-coordinate of the cell on the board
        self.y: int = y               # The y-coordinate of the cell on the board
        self.can_swap = can_swap      # Boolean flag indicating if the cell's value can be swapped
