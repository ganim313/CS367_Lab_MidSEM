import numpy as np
import matplotlib.pyplot as plt
import random
random.seed(1)
def split_matrix(matrix):
    return [matrix[i:i+128, j:j+128] for i in range(0, 512, 128) for j in range(0, 512, 128)]
def reassemble_matrix(pieces, state):
    new_matrix = np.zeros((512, 512))
    index = 0
    for i in range(0, 512, 128):
        for j in range(0, 512, 128):
            new_matrix[i:i+128, j:j+128] = pieces[state[index]]
            index += 1
    return new_matrix
def calculate_cost(matrix, state, pieces):
    cost = 0
    for i in range(3):
        for j in range(3):
            right_diff = np.sum(np.abs(pieces[state[i*4+j]][:, -1] - pieces[state[i*4+j+1]][:, 0]))
            bottom_diff = np.sum(np.abs(pieces[state[i*4+j]][-1, :] - pieces[state[(i+1)*4+j]][0, :]))
            cost += right_diff + bottom_diff
    return cost
def get_neighbor(state):
    new_state = state.copy()
    i, j = random.sample(range(16), 2)
    new_state[i], new_state[j] = new_state[j], new_state[i]
    return new_state
def simulated_annealing(pieces,final_temp =1, max_iter=10000, initial_temp=1000, alpha=0.99):
    state = list(range(16)) 
    current_cost = calculate_cost(None, state, pieces)
    temp = initial_temp
    for i in range(max_iter):
        new_state = get_neighbor(state)
        new_cost = calculate_cost(None, new_state, pieces)
        delta_cost = new_cost - current_cost
        
        if delta_cost < 0 or random.uniform(0, 1) < np.exp(-delta_cost / temp):
            state = new_state
            current_cost = new_cost
        
        temp *= alpha
        
        if i % 1000 == 0:
            print(f"Iteration {i}, Current Cost: {current_cost}, Temperature: {temp}")
    
    return state

with open('scrambled_lena.mat', 'r') as file:
    lines = file.readlines()

arr = []
for line in lines:
    arr.extend(map(float, line.split()))

no_arr = np.array(arr)
if len(no_arr) == 512 * 512:
    matrix = no_arr.reshape(512, 512)
else:
    raise ValueError("Error!")

# Split the scrambled image into 16 submatrices
pieces = split_matrix(matrix)

# Run simulated annealing
final_state = simulated_annealing(pieces)

# Reassemble and display the final matrix
final_matrix = reassemble_matrix(pieces, final_state)
plt.imshow(final_matrix, cmap='gray')
plt.colorbar()
plt.show()
