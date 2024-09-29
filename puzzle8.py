import random

def is_valid_move(x, y):
    return 0 <= x < 3 and 0 <= y < 3

def move(puzzle, zero_pos, direction):
    x, y = zero_pos
    new_puzzle = [row[:] for row in puzzle] 
    moves = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    dx, dy = moves[direction]
    new_x, new_y = x + dx, y + dy

    if is_valid_move(new_x, new_y):
        new_puzzle[x][y], new_puzzle[new_x][new_y] = new_puzzle[new_x][new_y], new_puzzle[x][y]
        return new_puzzle, (new_x, new_y)
    return puzzle, zero_pos

def print_puzzle(puzzle):
    for row in puzzle:
        print(row)
    print()

def generate_puzzle_at_depth(d):
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  
    zero_pos = (2, 2) 

    current_puzzle = goal_state
    current_zero_pos = zero_pos
    moves = ['up', 'down', 'left', 'right']

    reverse_move = {
        'up': 'down',
        'down': 'up',
        'left': 'right',
        'right': 'left'
    }
    
    last_move = None

    print("Initial State:")
    print_puzzle(current_puzzle)

    for step in range(1, d + 1):
        valid_moves = moves[:]
        
        if last_move:
            valid_moves.remove(reverse_move[last_move])

        while True:
            move_direction = random.choice(valid_moves)
            new_puzzle, new_zero_pos = move(current_puzzle, current_zero_pos, move_direction)
            
            if new_puzzle != current_puzzle:  
                current_puzzle, current_zero_pos = new_puzzle, new_zero_pos
                last_move = move_direction
                break  

        print("Instance",step,":")
        print_puzzle(current_puzzle)

    return current_puzzle

depth = 5
puzzle_at_depth = generate_puzzle_at_depth(depth)

print(f"Final Puzzle at depth {depth}:")
for row in puzzle_at_depth:
    print(row)
