from src.search import WordSearch
from src.board import Board

# Init search
searcher = WordSearch()

board = Board(True)
words = searcher.find_all_words(board, int(input("Swaps: "))).get_sorted(board)

for i in range(2):
    words[i].print()