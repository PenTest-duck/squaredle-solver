# Squaredle Solver

board = []

def read_wordlist():
    with open("NWL2020-alphabetical.txt", "r") as f:
        global wordlist
        wordlist = f.read().split()

def setup_board():
    global dimension
    dimension = int(input("Board size: "))
    print("Enter rows of letters, with no spaces, e.g. CLIF")
    for row in range(1, dimension + 1):
        row_input = list(input(f"Row #{row}: ").upper())
        while len(row_input) != dimension:
            row_input = list(input(f"Row #{row}: ").upper())
        board.append(row_input)

def check_fragment(fragment):
    found = False
    low = 0
    high = len(wordlist) - 1
    
    while not found and high >= low:
        middle = (high + low) // 2
        
        if wordlist[middle].startswith(fragment):
            found = True
        elif fragment < wordlist[middle]:
            high = middle - 1
        else:
            low = middle + 1

    return found

def check_word(word):
    found = False
    low = 0
    high = len(wordlist) - 1
    
    while not found and high >= low:
        middle = (high + low) // 2
        
        if wordlist[middle] == word:
            found = True
        elif word < wordlist[middle]:
            high = middle - 1
        else:
            low = middle + 1

    return found

def find_next(path):
    pos = []
    paths = []
    row = path[-1][0]
    col = path[-1][1]

    # Get all positions of surrounding
    if row > 0:
        pos.append([row - 1, col])
        if col > 0:
            pos.append([row - 1, col - 1])
        if col < dimension - 1:
            pos.append([row - 1, col + 1])
    if row < dimension - 1:
        pos.append([row + 1, col])
        if col > 0:
            pos.append([row + 1, col - 1])
        if col < dimension - 1:
            pos.append([row + 1, col + 1])
    if col > 0:
        pos.append([row, col - 1])
    if col < dimension - 1:
        pos.append([row, col + 1])

    # Remove positions already in path
    for p in pos[:]:
        if p in path:
            pos.remove(p)

    # Add valid fragments to paths
    for p in pos:
        fragment = ""
        for coord in path:
            fragment += board[coord[0]][coord[1]]
            
        new_frag = fragment + board[p[0]][p[1]]
        if check_fragment(new_frag):
            new_path = path[:]
            new_path.append([p[0], p[1]])
            paths.append(new_path)

    return paths

def solve_letter(row, col):
    paths = [[[row, col]]]
    words = []
    
    # Find all possible fragments
    for p in paths:
        paths += find_next(p)

    # Filter for valid words
    for p in paths:
        word = ""
        for i in p:
            word += board[i[0]][i[1]]
        words.append(word)
    
    for w in words[:]:
        if len(w) < 4 or not check_word(w):
            words.remove(w)

    return words

def solve_board():
    words = []

    # Find all possible words
    for row in range(dimension):
        for col in range(dimension):
            words += solve_letter(row, col)

    # Filter unique and sort words
    words = sorted(list(set(words)))
    
    for i in range(len(words)):
        print(f"{i + 1}: {words[i]}")

if __name__ == "__main__":
    
    read_wordlist()
    
    setup_board()

    solve_board()
