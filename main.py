from src.search import WordSearch
from src.board import Board

# Init search and random board
searcher = WordSearch()
board = Board(False)
board.print()

# Start search
words = searcher.find_all_words(board, int(input("Swaps: "))).get_sorted(board)

# Print 3 best words (can be the same with different paths)
for i in range(3):
    print("------------")
    word = words[i]
    word.print()
