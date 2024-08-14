from src.cell import Cell
from random import choice, random
from string import ascii_lowercase

class Board:
    ROWS = 5  # Number of rows in the board
    COLS = 5  # Number of columns in the board

    def __init__(self, from_input: bool = True) -> None:
        """
        Initialize the Board.

        Args:
        - from_input (bool): Determines whether to initialize the board from user input or randomly.
        """
        # Initialize the board with an empty list for each row
        self.cells: list[list[Cell]] = [[] for _ in range(Board.ROWS)]
        
        # Setup the board based on the provided flag
        if from_input:
            self._setup_from_input()
        else:
            self._setup_random()

    def _setup_random(self) -> None:
        """
        Initialize the board with random cells.

        Each cell is assigned a random lowercase letter and a random flag indicating special conditions.
        """
        for y in range(Board.ROWS):
            for x in range(Board.COLS):
                # Randomly choose a letter and a flag indicating whether the cell can be swapped
                letter = choice(ascii_lowercase)
                can_swap = random() < 0.3
                self.cells[y].append(Cell(letter, x, y, "", can_swap))

        # Randomly set special flags for some cells
        choice(choice(self.cells)).flag = "2"  # Double letter score
        choice(choice(self.cells)).flag = "D" if random() > 0.5 else "T"  # Double or triple word score

    def _setup_from_input(self) -> None:
        """
        Initialize the board based on user input.

        The input string specifies cell values and flags. 
        Special flags like "!" indicate that the cell can be swapped.
        """
        board_string: str = input().strip()  # Read the input string

        i: int = 0  # Index for traversing the input string
        char_counter: int = 0  # Counter to keep track of the position in the board
        flag: str = " "  # Current flag to be applied to cells
        can_swap: bool = False  # Flag indicating if the cell can be swapped

        while i < len(board_string):
            token: str = board_string[i]  # Get the current character from the input string
            if token.isnumeric() or token in ["!", "$"]:
                if token == "!":
                    can_swap = True  # Set the swap flag if "!" is encountered
                else:
                    flag = token  # Set the special flag (e.g., "2", "D", "T")
            else:
                # Create a new Cell and add it to the board
                self.cells[char_counter // Board.COLS].append(Cell(token.lower(), char_counter % Board.COLS, char_counter // Board.COLS, flag, can_swap))
                char_counter += 1  # Move to the next cell
                flag = " "  # Reset the flag for the next cell
                can_swap = False  # Reset the swap flag

            i += 1  # Move to the next character in the input string

    def get_cell(self, x: int, y: int) -> Cell:
        """
        Get the cell at the specified coordinates.

        Args:
        - x (int): The x-coordinate of the cell.
        - y (int): The y-coordinate of the cell.

        Returns:
        - Cell: The cell at the given coordinates.
        """
        return self.cells[y][x]

    def set_cell(self, x: int, y: int, cell: Cell | None) -> Cell:
        """
        Set the cell at the specified coordinates.

        Args:
        - x (int): The x-coordinate of the cell.
        - y (int): The y-coordinate of the cell.
        - cell (Cell | None): The cell to set at the given coordinates. If None, clears the cell.

        Returns:
        - Cell: The cell that was set at the given coordinates.
        """
        self.cells[y][x] = cell
        return cell

    def print(self) -> None:
        """
        Print the board to the console.

        Displays the value of each cell in a grid format.
        """
        for row in self.cells:
            for cell in row:
                print(cell.value + "/" + cell.flag + "|", end="")  # Print the cell value followed by a space
            print()  # Move to the next line after printing a row
