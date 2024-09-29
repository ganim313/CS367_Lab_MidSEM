import random

class Puzzle8:
    def __init__(self):
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  # Goal state with 0 representing the empty space
        self.state = self.generate_random_state()

    def generate_random_state(self):
        """Generate a random state for the Puzzle-8."""
        numbers = list(range(9))  # Numbers 0 to 8
        random.shuffle(numbers)
        return [numbers[i:i + 3] for i in range(0, 9, 3)]  # Create 3x3 board

    def display_board(self):
        """Display the current state of the puzzle."""
        for row in self.state:
            print(" ".join(str(num) if num != 0 else " " for num in row))
        print()

    def is_goal_state(self):
        """Check if the current state is the goal state."""
        return self.state == self.goal_state

    def find_zero(self):
        """Find the position of the empty space (0)."""
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return (i, j)
        return None

    def generate_possible_moves(self):
        """Generate possible moves from the current state."""
        zero_row, zero_col = self.find_zero()
        moves = []

        # Possible directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = zero_row + dr, zero_col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                moves.append((new_row, new_col))

        return moves

    def make_move(self, new_zero_position):
        """Make a move by sliding a tile into the empty space."""
        zero_row, zero_col = self.find_zero()
        new_row, new_col = new_zero_position

        # Swap the empty space with the target tile
        self.state[zero_row][zero_col], self.state[new_row][new_col] = self.state[new_row][new_col], self.state[zero_row][zero_col]

# Example usage
puzzle = Puzzle8()
puzzle.display_board()

if not puzzle.is_goal_state():
    possible_moves = puzzle.generate_possible_moves()
    print("Possible moves:", possible_moves)
