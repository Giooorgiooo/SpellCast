class TrieNode:
    def __init__(self):
        """
        Initialize a TrieNode.

        This node is part of a trie (prefix tree) data structure used for storing strings (words). Each node
        represents a single character in the trie.

        Attributes:
        - children (dict): A dictionary mapping characters to their corresponding child TrieNodes.
        - is_end_of_word (bool): A flag indicating whether this node marks the end of a valid word.
        """
        self.children = {}  # A dictionary where keys are characters and values are TrieNodes representing subsequent characters.
        self.is_end_of_word = False  # A flag indicating if this node completes a valid word.