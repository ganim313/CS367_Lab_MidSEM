import heapq
import re

# Function to preprocess text (convert to lowercase, remove punctuation, split into sentences)
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text) 
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return sentences

# Function to process two documents
def process_documents(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f1:
        doc1 = f1.read()
    with open(file2, 'r', encoding='utf-8') as f2:
        doc2 = f2.read()
    
    preprocessed_doc1 = preprocess_text(doc1)
    preprocessed_doc2 = preprocess_text(doc2)
    
    return preprocessed_doc1, preprocessed_doc2

# Node class to represent a state in the search space
class Node:
    def __init__(self, state, parent=None):
        self.state = state  # The current sentence alignment (index in doc1, index in doc2)
        self.parent = parent  # Parent node (for tracing the path)
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost (Levenshtein distance)
        self.f = 0  # Total cost (g + h)
    
    def __lt__(self, other):
        return self.f < other.f

# Levenshtein distance (edit distance) calculation
def levenshtein_distance(str1, str2):
    n, m = len(str1), len(str2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0:
                dp[i][j] = j  # Cost of all insertions
            elif j == 0:
                dp[i][j] = i  # Cost of all deletions
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No cost if characters match
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],    # Deletion
                                   dp[i][j - 1],    # Insertion
                                   dp[i - 1][j - 1])  # Substitution

    return dp[n][m]

# Heuristic function using Levenshtein distance
def heuristic(node, goal_state):
    return levenshtein_distance(node.state, goal_state)

# Generate successors (possible next alignments) for the A* search
def get_successors(node, doc1, doc2):
    successors = []
    doc1_len, doc2_len = len(doc1), len(doc2)

    current_index_doc1 = node.state[0]
    current_index_doc2 = node.state[1]

    # Move forward in doc1 (align with next sentence in doc2)
    if current_index_doc1 < doc1_len:
        next_state = (current_index_doc1 + 1, current_index_doc2)
        successors.append(Node(next_state, node))

    # Move forward in doc2 (align with next sentence in doc1)
    if current_index_doc2 < doc2_len:
        next_state = (current_index_doc1, current_index_doc2 + 1)
        successors.append(Node(next_state, node))

    # Move forward in both doc1 and doc2
    if current_index_doc1 < doc1_len and current_index_doc2 < doc2_len:
        next_state = (current_index_doc1 + 1, current_index_doc2 + 1)
        successors.append(Node(next_state, node))

    return successors

# A* search algorithm for text alignment and plagiarism detection
def a_star(doc1, doc2, plagiarism_threshold):
    start_state = (0, 0)  # Initial state (start of both documents)
    goal_state = (len(doc1), len(doc2))  # Goal state (end of both documents)

    start_node = Node(start_state)
    goal_node = Node(goal_state)

    open_list = []
    heapq.heappush(open_list, (start_node.f, start_node))
    visited = set()
    nodes_explored = 0

    alignments = []  # List to hold all aligned sentence pairs

    while open_list:
        _, node = heapq.heappop(open_list)
        if tuple(node.state) in visited:
            continue
        visited.add(tuple(node.state))
        nodes_explored += 1

        # Check if goal is reached
        if node.state == goal_node.state:
            path = []
            while node:
                path.append(node.state)
                node = node.parent
            print('Total nodes explored', nodes_explored)
            return path[::-1], alignments

        # Generate successors and push them to the open list
        for successor in get_successors(node, doc1, doc2):
            successor.g = node.g + 1
            sentence1 = doc1[successor.state[0] - 1] if successor.state[0] > 0 else ""
            sentence2 = doc2[successor.state[1] - 1] if successor.state[1] > 0 else ""
            successor.h = levenshtein_distance(sentence1, sentence2)
            successor.f = successor.g + successor.h
            heapq.heappush(open_list, (successor.f, successor))

            # Check if sentences are similar enough to consider them as plagiarism
            if successor.h <= plagiarism_threshold:
                alignments.append((sentence1, sentence2, successor.h))

    print('Total nodes explored', nodes_explored)
    return None, alignments

# Input file paths for two documents
file1 = r"C:\Users\manim\OneDrive\Desktop\ai\introduction.txt"
file2 = r"C:\Users\manim\OneDrive\Desktop\ai\introduction.txt"
#"C:\Users\manim\OneDrive\Desktop\ai\INTORT.txt"

# Process the documents
preprocessed_doc1, preprocessed_doc2 = process_documents(file1, file2)

# Output the preprocessed documents
print("Preprocessed Document 1:", preprocessed_doc1)
print("Preprocessed Document 2:", preprocessed_doc2)

# Define plagiarism detection threshold (Levenshtein distance <= threshold)
plagiarism_threshold = 5  # You can adjust this threshold based on the level of similarity you want to detect

# Run A* search for sentence alignment and plagiarism detection
alignment_path, potential_plagiarism = a_star(preprocessed_doc1, preprocessed_doc2, plagiarism_threshold)

# Output the alignment path
print("Alignment Path:", alignment_path)

# Output the potential plagiarism pairs
print("Potential Plagiarism (Sentence Pairs with Low Edit Distance):")
for sentence1, sentence2, edit_distance in potential_plagiarism:
    print(f"Sentence 1: {sentence1}")
    print(f"Sentence 2: {sentence2}")
    print(f"Levenshtein Distance: {edit_distance}")
    print("---")
