from src.cell import Cell
from src.board import Board

class Word:
    def __init__(self, first_cell: Cell) -> None:
        """
        Initialize a new word with the first cell.

        :param first_cell: The starting cell for the word.
        """
        self.cells = [first_cell]
    
    def add(self, cell: Cell):
        """
        Add a cell to the current word.

        :param cell: The cell to be added to the word.
        """
        self.cells.append(cell)

    def pop(self):
        """
        Remove the last cell from the current word.
        """
        self.cells.pop()

    def _get_path(self) -> list[tuple[int, int]]:
        """
        Get the path of the word as a list of (x, y) coordinates.

        :return: A list of tuples representing the coordinates of the cells in the word.
        """
        return [(cell.x, cell.y) for cell in self.cells]
    
    def __str__(self) -> str:
        """
        Convert the word to a string.

        :return: The word formed by concatenating the values of its cells.
        """
        return ''.join(cell.value for cell in self.cells)
    
    def count_points(self) -> int:
        """
        Calculate the points for the word based on letter scores and multipliers.

        :return: The total points for the word.
        """
        letter_scores = {
            'a': 1, 'e': 1, 'i': 1, 'o': 1,
            'n': 2, 'r': 2, 's': 2, 't': 2,
            'd': 3, 'g': 3, 'l': 3,
            'b': 4, 'h': 4, 'p': 4, 'm': 4, 'u': 4, 'y': 4,
            'c': 5, 'f': 5, 'v': 5, 'w': 5,
            'k': 6,
            'j': 7, 'x': 7,
            'q': 8, 'z': 8
        }

        multiplier = 1
        points = 0

        for cell in self.cells:
            letter_score = letter_scores[cell.value]
            match cell.flag:
                case "2": letter_score *= 2  # Double letter score
                case "3": letter_score *= 3  # Triple letter score
                case "$": multiplier = 2    # Double word score
            points += letter_score

        # Apply word multiplier and bonus points
        points = points * multiplier + (10 if len(self.cells) >= 6 else 0)

        # Add points for each cell that can be swapped
        for cell in self.cells:
            if cell.can_swap:
                points += 1

        return points
    
class WordList:
    def __init__(self) -> None:
        """
        Initialize the WordList with an empty list of words.
        """
        # List of tuples where each tuple contains a word and its path
        self.objects: list[tuple[str, list[tuple[int, int]]]] = []

    def get_sorted(self, board: Board) -> list[Word]:
        """
        Get a sorted list of words based on their points and remove duplicates.

        :param board: The game board used to construct words.
        :return: A list of unique words sorted by their points in descending order.
        """
        words = self.get_words(board)
        words.sort(key=lambda word: word.count_points(), reverse=True)

        return words

    def _add(self, word: tuple[str, list]):
        """
        Add a word and its path to the list.

        :param word: A tuple containing the word and its path.
        """
        self.objects.append(word)

    def get_words(self, board: Board) -> list:
        """
        Convert stored word and path tuples to Word objects.

        :param board: The game board used to get cell values.
        :return: A list of Word objects.
        """
        words: list[Word] = []
        for obj in self.objects:
            first_position: tuple[int, int] = obj[1][0]
            word: Word = Word(board.get_cell(first_position[0], first_position[1]))

            # Add cells to the word based on the stored path
            for i in range(1, len(obj[1])):
                position = obj[1][i]
                word.add(board.get_cell(position[0], position[1]))

            words.append(word)

        return words
