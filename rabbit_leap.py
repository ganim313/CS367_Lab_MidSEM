from collections import deque


def is_valid_move(state, empty_index, target_index):
    
    if empty_index < target_index:  
        if state[target_index] == 'W':  
            return True
    elif empty_index > target_index:  
        if state[target_index] == 'E':  
            return True
    return False


def get_successors(state):
    successors = []
    state_list = list(state)  
    empty_index = state_list.index('X')  
    
   
    possible_moves = []
    
    # One-step move
    if empty_index - 1 >= 0 and is_valid_move(state_list, empty_index, empty_index - 1):
        possible_moves.append((empty_index - 1, empty_index))
    if empty_index + 1 < len(state_list) and is_valid_move(state_list, empty_index, empty_index + 1):
        possible_moves.append((empty_index + 1, empty_index))
    
    # Jump over one rabbit
    if empty_index - 2 >= 0 and is_valid_move(state_list, empty_index, empty_index - 2):
        possible_moves.append((empty_index - 2, empty_index))
    if empty_index + 2 < len(state_list) and is_valid_move(state_list, empty_index, empty_index + 2):
        possible_moves.append((empty_index + 2, empty_index))
    
    # Apply moves and create new states
    for move in possible_moves:
        new_state = state_list[:]
        new_state[empty_index], new_state[move[0]] = new_state[move[0]], new_state[empty_index]
        successors.append(tuple(new_state))  
    
    return successors


def bfs(start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set()
    
    while queue:
        (state, path) = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        path = path + [state]
        if state == goal_state:
            return path
        for successor in get_successors(state):
            queue.append((successor, path))
    return None


def dfs(start_state, goal_state):
    stack = [(start_state, [start_state])]
    visited = set()
    
    while stack:
        (state, path) = stack.pop()
        if state == goal_state:
            return path
        if state in visited:
            continue
        visited.add(state)
        for successor in get_successors(state):
            stack.append((successor, path + [successor]))
    return None


start_state = ('E', 'E', 'E', 'X', 'W', 'W', 'W')
goal_state = ('W', 'W', 'W', 'X', 'E', 'E', 'E')


solution = bfs(start_state, goal_state)
if solution:
    print("BFS Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found with BFS.")


solution = dfs(start_state, goal_state)
if solution:
    print("DFS Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found with DFS.")
