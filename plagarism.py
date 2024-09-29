import heapq
import re
import nltk
def preprocess_text(text):
    # Tokenize into sentences
    sentences = nltk.sent_tokenize(text)
    # Normalize by converting to lowercase and removing punctuation
    normalized_sentences = [re.sub(r'[^\w\s]', '', sentence.lower()) for sentence in sentences]
    return normalized_sentences

def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j] + 1,  # Deletion
                               dp[i][j - 1] + 1,  # Insertion
                               dp[i - 1][j - 1] + 1)  # Substitution
    return dp[m][n]

# A* search function
def a_star_search(doc1, doc2):
    # Initial state
    start = (0, 0, 0)  # (index_doc1, index_doc2, cost_so_far)
    goal = (len(doc1), len(doc2))

    # Priority queue
    frontier = []
    heapq.heappush(frontier, (0, start))
    explored = {}

    while frontier:
        current_f, (i, j, cost_so_far) = heapq.heappop(frontier)

        # Check if we've reached the goal
        if (i, j) == goal:
            return cost_so_far

        # Expand possible transitions
        if i < len(doc1) and j < len(doc2):  # Align sentences
            new_cost = cost_so_far + levenshtein_distance(doc1[i], doc2[j])
            new_state = (i + 1, j + 1, new_cost)
            heapq.heappush(frontier, (new_cost + heuristic(i + 1, j + 1, doc1, doc2), new_state))

        if i < len(doc1):  # Skip sentence in doc1
            new_cost = cost_so_far + levenshtein_distance(doc1[i], "")
            new_state = (i + 1, j, new_cost)
            heapq.heappush(frontier, (new_cost + heuristic(i + 1, j, doc1, doc2), new_state))

        if j < len(doc2):  # Skip sentence in doc2
            new_cost = cost_so_far + levenshtein_distance("", doc2[j])
            new_state = (i, j + 1, new_cost)
            heapq.heappush(frontier, (new_cost + heuristic(i, j + 1, doc1, doc2), new_state))

# Heuristic function: Minimum possible edit distance for remaining sentences
def heuristic(i, j, doc1, doc2):
    remaining_cost = 0
    for k in range(i, len(doc1)):
        remaining_cost += levenshtein_distance(doc1[k], "")
    for k in range(j, len(doc2)):
        remaining_cost += levenshtein_distance("", doc2[k])
    return remaining_cost

def align_documents(doc1, doc2):
    preprocessed_doc1 = preprocess_text(doc1)
    preprocessed_doc2 = preprocess_text(doc2)

    # Perform A* search to find the minimum cost alignment
    total_cost = a_star_search(preprocessed_doc1, preprocessed_doc2)
    return total_cost

def detect_plagiarism(doc1, doc2, threshold=5):
    preprocessed_doc1 = preprocess_text(doc1)
    preprocessed_doc2 = preprocess_text(doc2)

    plagiarism_candidates = []
    for i, sentence1 in enumerate(preprocessed_doc1):
        for j, sentence2 in enumerate(preprocessed_doc2):
            distance = levenshtein_distance(sentence1, sentence2)
            if distance <= threshold:
                plagiarism_candidates.append((i, j, distance))

    return plagiarism_candidates

def main():
    # Test Case 1
    doc1 = """The cat sits on the mat.
              The cat sits on the mat."""

    doc2 = """The cat sits on the mat.
              The cat sits on the mat."""

    # Test Case 2
    doc3 = """The cat sits on the mat.
              The dog sits on the rug."""

    doc4 = """The cat is on the mat.
             The dog is on the carpet."""
             
    # Test Case 3
    doc5 = """The sun is bright.
              It is a nice day."""

    doc6 = """The rain is falling.
               It is cold outside."""

    # Test Case 4
    doc7 = """Artificial intelligence is transforming industries.
              Machine learning algorithms are powerful tools.
              Technology is advancing rapidly."""

    doc8 = """Technology is advancing rapidly.
              AI and ML are transforming the world.
              Computers are getting smarter every day."""

    # Align documents and detect plagiarism (TESTCASE1)
    print("TEST CASE 1 : ")
    total_cost = align_documents(doc1, doc2)
    print(f"Total alignment cost: {total_cost}")

    plagiarism_candidates = detect_plagiarism(doc1, doc2)
    if plagiarism_candidates:
        print("plagiarism detected:")
        for i, j, distance in plagiarism_candidates:
            print(f"Sentence {i+1} from Document 1 and Sentence {j+1} from Document 2: Edit Distance = {distance}")
    else:
        print("No plagiarism detected.")
        
    # Align documents and detect plagiarism(TESTCASE2)
    print("TEST CASE 2 : ")
    total_cost = align_documents(doc3, doc4)
    print(f"Total alignment cost: {total_cost}")

    plagiarism_candidates = detect_plagiarism(doc3, doc4)
    if plagiarism_candidates:
        print("plagiarism detected:")
        for i, j, distance in plagiarism_candidates:
            print(f"Sentence {i+1} from Document 1 and Sentence {j+1} from Document 2: Edit Distance = {distance}")
    else:
        print("No plagiarism detected.")
        
    # Align documents and detect plagiarism(TESTCASE3)
    print("TEST CASE 3 : ")
    total_cost = align_documents(doc5, doc6)
    print(f"Total alignment cost: {total_cost}")

    plagiarism_candidates = detect_plagiarism(doc5, doc6)
    if plagiarism_candidates:
        print("plagiarism detected:")
        for i, j, distance in plagiarism_candidates:
            print(f"Sentence {i+1} from Document 1 and Sentence {j+1} from Document 2: Edit Distance = {distance}")
    else:
        print("No plagiarism detected.")
        
    # Align documents and detect plagiarism(TESTCASE4)
    print("TEST CASE 4 : ")
    total_cost = align_documents(doc7, doc8)
    print(f"Total alignment cost: {total_cost}")

    plagiarism_candidates = detect_plagiarism(doc7, doc8)
    if plagiarism_candidates:
        print("plagiarism detected:")
        for i, j, distance in plagiarism_candidates:
            print(f"Sentence {i+1} from Document 1 and Sentence {j+1} from Document 2: Edit Distance = {distance}")
    else:
        print("No plagiarism detected.")

if __name__ == "__main__":
    main()
