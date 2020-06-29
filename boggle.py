from string import ascii_uppercase
from random import choice

def make_grid(width, height):
    """
    # make an empty boggle grid
    return{}
    """

    # creates a grid that will hold all of the tiles for the boggle game
    return {(row, col): choice(ascii_uppercase)
        for row in range(height)
        for col in range(width)
    }

def neighbors_of_position(coords):
    # get neighbors of a given position
    row = coords[0]
    col = coords[1]

    # assigning each  of the neighbors
    # TOP-LEFT to TOP-RIGHT
    top_left = (row - 1, col - 1)
    top_center = (row - 1, col)
    top_right = (row - 1, col + 1)

    # LEFT to RIGHT
    left = (row, col - 1)
    # (row, col) are the default / centers
    right = (row, col + 1)

    # BOTTOM-LEFT to BOTTOM-RIGHT
    bottom_left = (row + 1, col - 1)
    bottom_center = (row + 1, col)
    bottom_right = (row + 1, col + 1)

    return [top_left, top_center, top_right,
            left, right,
            bottom_left, bottom_center, bottom_right]

def all_grid_neighbors(grid):
    # get all of the possible neighbors for each position in the grid
    neighbors = {}
    for position in grid:
        position_neighbors = neighbors_of_position(position)
        neighbors[position] = [p for p in position_neighbors if p in grid]
    return neighbors

def path_to_word(grid, path):
    # add all of the letters on the path to a string
    return ''.join([grid[p] for p in path])

"""
def word_in_dictionary(word, dict):
    return word in dict
"""

def search(grid, dictionary):
    # search through the paths to locate words by matching strings to words in a dictionary
    neighbors = all_grid_neighbors(grid)
    paths = []
    full_words, stems = dictionary

    def do_search(path):
        word = path_to_word(grid, path)
        #if word_in_dictionary(word, dictionary):
        if word in full_words:
            paths.append(path)
        if word not in stems:
            return # nothing
        for next_pos in neighbors[path[-1]]:
            if next_pos not in path:
                do_search(path + [next_pos])
    
    for position in grid:
        do_search([position])
    
    words = []
    for path in paths:
        words.append(path_to_word(grid, path))
    return set(words)

def get_dictionary(dictionary_file):
    # load dictionary file
    full_words, stems = set(), set()

    with open(dictionary_file) as f:
        for word in f:
            word = word.strip().upper()
            full_words.add(word)

            for i in range(1, len(word)):
                stems.add(word[:i])

        #return [w.strip().upper() for w in f] # square brackets = list O(n) notation
        #return {w.strip().upper() for w in f} # curly brackets = set O(1) notation
    return full_words, stems

def display_words(words):
    #for word in words:
        #print(word)
    # instead of iterating through each word as its found, sort alphabetically and split to \n new lines
    print("\n".join(sorted(words)))
    print("Found %s words" % len(words))
    """
    # instead of printing to the terminal, create a new file with the foundWords
    with open('foundWords.txt', 'w') as f:
        f = open('foundWords.txt', 'w')
        f.write("\n".join(sorted(words)))
        f.write("\nFound %s words" % len(words))
    """

def main():
    # this is the function that will run the whole project
    grid = make_grid(4, 4)
    dictionary = get_dictionary('words.txt')
    words = search(grid, dictionary)
    display_words(words)

if __name__ == "__main__":
    main()
