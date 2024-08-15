from src.word import Word, WordList
from src.trie import TrieNode
from src.board import Board
from src.cell import Cell
from string import ascii_lowercase

import time

class WordSearch:
    def __init__(self) -> None:
        """
        Initialize the WordSearch object.
        
        Loads words from a file and builds a Trie for efficient word lookup.
        """
        self.words: set = set()  # Set to store the valid words
        # Load words from the file into the set
        with open("data/words.txt", "r") as file:
            for line in file.readlines():
                self.words.add(line.strip())
        
        self.trie: TrieNode = self._build_trie()
        self.modified_tree: TrieNode = self._build_trie(True)
    
    def _build_trie(self, modified = False) -> TrieNode:
        """
        Build a Trie from the set of words.

        Returns:
        - TrieNode: The root node of the constructed Trie.
        """
        root = TrieNode()
        for word in self.words:
            if modified and len(word) < 6:
                continue

            node = root
            for letter in word:
                if letter not in node.children:
                    node.children[letter] = TrieNode()
                node = node.children[letter]
            node.is_end_of_word = True
        return root

    def find_all_words(self, board: Board, swaps_left: int) -> WordList:
        """
        Find all valid words in the board using Depth-First Search (DFS).

        Args:
        - board (Board): The board to search for words.

        Returns:
        - WordList: A list of found words along with their paths.
        """

        found_words: WordList = WordList()
        trie = self.modified_tree if swaps_left >= 3 else self.trie

        # Start DFS from each cell in the board
        for y in range(Board.ROWS):
            for x in range(Board.COLS):
                cell: Cell = board.get_cell(x, y)
                board.set_cell(x, y, None)

                self._dfs(board, [(x, y, cell.value, False)], trie.children[cell.value], found_words, swaps_left)

                # Perform DFS starting from the current cell
                if swaps_left > 0:
                    for char in ascii_lowercase:
                        if char != cell.value:
                            self._dfs(board, [(x, y, char, True)], trie.children[char], found_words, swaps_left - 1)
                
                board.set_cell(x, y, cell)

        if swaps_left >= 3 and len(found_words.paths) == 0:
            return self.find_all_words(board, 2)

        return found_words
    
    def _dfs(self, board: Board, current_path: list[tuple[int, int, str, bool]], node: TrieNode, found_words: WordList, swaps_left: int) -> None:
        """
        Perform Depth-First Search (DFS) to find words starting from a given cell.

        Args:
        - board (Board): The board to search on.
        - x (int): The x-coordinate of the starting cell.
        - y (int): The y-coordinate of the starting cell.
        - current_word (Word): The current word being formed.
        - node (TrieNode): The current node in the Trie.
        - found_words (WordList): The list of found words to be updated.
        """

        directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        x, y, _, _ = current_path[-1]

        # w = "".join([tup[2] for tup in current_path])

        # Add the current word to the found words if it's valid
        if node.is_end_of_word:
            found_words._add(tuple(current_path))

        temp_cell: Cell = board.get_cell(x, y)
        board.set_cell(x, y, None)  # Mark the current cell as visited

        # Explore all 8 possible directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < Board.ROWS and 0 <= ny < Board.COLS:
                next_cell: Cell = board.get_cell(nx, ny)
                if next_cell is not None:

                    # No swap
                    if next_cell.value in node.children:
                        current_path.append((nx, ny, next_cell.value, False))
                        self._dfs(board, current_path, node.children[next_cell.value], found_words, swaps_left)
                        current_path.pop()  # Backtrack
                
                    # Swap
                    if swaps_left > 0:
                        for char in ascii_lowercase:
                            if not char == next_cell.value and char in node.children:

                                current_path.append((nx, ny, char, True))
                                self._dfs(board, current_path, node.children[char], found_words, swaps_left - 1)
                                current_path.pop()  # Backtrack

        # Restore the original cell value after backtracking
        board.set_cell(x, y, temp_cell)

    def benchmark(self, swaps: int) -> None:
        """
        Benchmark the performance of the word search algorithm.

        Measures the average points and time taken for a number of games.
        """
        average_points: float = 0
        average_time: float = 0
        start: float = time.perf_counter()  # Record the start time

        games: int = 100  # Number of games to benchmark

        for i in range(games):
            board: Board = Board(False)  # Create a new board
            board.print()
            algorithm_start: float = time.perf_counter()  # Record the time before finding words
            word_list: WordList = self.find_all_words(board, swaps)  # Find all words in the board

            # Sort words by points and update the average points
            sorted_list = word_list.get_sorted(board)
            if sorted_list:
                average_points += sorted_list[0].get_points() / games
            
            # Update the average time
            average_time += (time.perf_counter() - algorithm_start) / games

            sorted_list[0].print()

        # Print the benchmark results
        print("Average points:", average_points)
        print("Average time:", str(average_time * 1000) + "ms")
        print("Total time:", str((time.perf_counter() - start)) + "s")
