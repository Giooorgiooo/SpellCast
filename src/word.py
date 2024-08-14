from src.cell import Cell
from src.board import Board

class Word:
    def __init__(self, board: Board, path: list[tuple[int, int, str, bool]]) -> None:
        """
        Initialize a new word based on a path of cells on the board.

        :param board: The game board containing the cells.
        :param path: A list of tuples representing the coordinates and character
                     of each cell in the word path.
        """
        self.word: str = ""
        self.path = path

        self.points = 0
        self.gems = 0

        # Dictionary to store the points associated with each letter.
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

        # Iterate through each cell in the path to build the word, calculate points, and count gems.
        for x, y, char, _ in self.path:
            self.word += char

            # Calculate score for the current letter.
            letter_score = letter_scores[char]
            cell: Cell = board.get_cell(x, y)

            # Check for special flags on the cell that modify the score or multiplier.
            if cell.flag == "2":
                letter_score *= 2
            elif cell.flag == "3":
                letter_score *= 3
            elif cell.flag == "$":
                multiplier = 2

            self.points += letter_score

            # Increment the gem counter if the cell allows swapping.
            if cell.can_swap:
                self.gems += 1

        # Apply the multiplier to the total points.
        self.points *= multiplier

        # Bonus points for words with 6 or more characters.
        if len(self.word) >= 6:
            self.points += 10

    def get_points(self) -> int:
        """
        Get the total points for the word.

        :return: The total points calculated for the word.
        """
        return self.points
    
    def has_swap(self) -> bool:
        """
        Check if any cell in the word's path allows swapping.

        :return: True if there is at least one swappable cell, otherwise False.
        """
        for path in self.path:
            if path[3]:
                return True
        return False
    
    def print(self) -> None:
        """
        Print the details of the word, including points, starting position,
        and any swap details if available.
        """
        print(f"Word: {self.word}")
        print(f"Start at: x: {self.path[0][0] + 1} | y: {self.path[0][1] + 1}")
        print(f"Points: {self.points}")
        print(f"Gems: {self.gems}")

        if self.has_swap():
            for pos in self.path:
                if pos[3]:
                    print("Swap to:", pos[2], "at", pos[0] + 1, pos[1] + 1)

class WordList:
    def __init__(self) -> None:
        """
        Initialize the WordList with an empty list of word paths.
        """
        # List to store word paths; each path is a list of tuples.
        self.paths: list[list[tuple[int, int, str, bool]]] = []

    def get_sorted(self, board: Board) -> list[Word]:
        """
        Get a sorted list of Word objects based on their points, 
        considering any bonus points or gems, and remove duplicates.

        :param board: The game board used to construct Word objects.
        :return: A list of unique Word objects sorted by their points in descending order.
        """
        words: list[Word] = self.get_words(board)
        words.sort(key=lambda word: word.get_points() + word.gems, reverse=True)

        return words

    def _add(self, path: list[tuple[int, int, str, bool]]) -> None:
        """
        Add a word path to the list of paths.

        :param word: A tuple containing the word and its corresponding path.
        """
        self.paths.append(path)

    def get_words(self, board: Board) -> list[Word]:
        """
        Convert stored word paths into Word objects.

        :param board: The game board used to get cell values.
        :return: A list of Word objects created from the stored paths.
        """
        words: list[Word] = []
        for path in self.paths:
            word: Word = Word(board, path)
            words.append(word)

        return words
