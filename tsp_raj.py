import random
import math
import matplotlib.pyplot as plt

def haversine(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371.0
    distance = r * c
    return distance
cities = [
    "Jaipur", "Udaipur", "Jodhpur", "Jaisalmer", "Ajmer", "Pushkar",
    "Bikaner", "Chittorgarh", "Mount Abu", "Sawai Madhopur", "Alwar",
    "Ranthambore", "Tonk", "Neemrana", "Kota", "Barmer", "Bundi",
    "Mandawa", "Shekhawati", "Ganganagar"
]

city_coords = [
    (26.9124, 75.7873),  # Jaipur
    (24.5854, 73.7125),  # Udaipur
    (26.2389, 73.0243),  # Jodhpur
    (26.9157, 70.9083),  # Jaisalmer
    (26.4499, 74.6399),  # Ajmer
    (26.4898, 74.5511),  # Pushkar
    (28.0229, 73.3119),  # Bikaner
    (24.8887, 74.6269),  # Chittorgarh
    (24.5926, 72.7156),  # Mount Abu
    (25.9920, 76.3665),  # Sawai Madhopur
    (27.5520, 76.6346),  # Alwar
    (26.0173, 76.5026),  # Ranthambore
    (26.1664, 75.7885),  # Tonk
    (27.9882, 76.3844),  # Neemrana
    (25.2138, 75.8648),  # Kota
    (25.7457, 71.3943),  # Barmer
    (25.4305, 75.6499),  # Bundi
    (28.0559, 75.1416),  # Mandawa
    (27.3214, 75.7491),  # Shekhawati
    (29.9038, 73.8772)   # Ganganagar
]
def generate_distance_matrix(coords):
    n = len(coords)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = haversine(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
    return matrix
distance_matrix = generate_distance_matrix(city_coords)
def total_distance(route):
    total = 0
    for i in range(len(route) - 1):
        total += distance_matrix[route[i]][route[i + 1]]
    total += distance_matrix[route[-1]][route[0]] 
    return total
def plot_route(route, title, min_distance=None):
    plt.figure(figsize=(10, 6))
    x = [city_coords[i][0] for i in route] + [city_coords[route[0]][0]]  
    y = [city_coords[i][1] for i in route] + [city_coords[route[0]][1]]  
    plt.plot(x, y, marker='o', linestyle='-', color='b')
    plt.title(title)
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.xticks(rotation=45)
    plt.grid()
    for i, city in enumerate(route):
        plt.annotate(cities[city], (city_coords[city][0], city_coords[city][1]), textcoords="offset points", xytext=(0, 5), ha='center')
    if min_distance is not None:
        plt.text(0.5, 0.1, f'Minimum Distance: {min_distance:.2f} km', fontsize=12, ha='center', transform=plt.gca().transAxes)

    plt.show()

def simulated_annealing(initial_temp=10000, final_temp=1, alpha=0.99, num_iterations=1000):
    current_solution = list(range(len(distance_matrix)))
    random.shuffle(current_solution) 
    initial_distance = total_distance(current_solution)
    best_solution = current_solution[:]
    best_distance = initial_distance
    temperature = initial_temp
    plot_route(current_solution, "Initial Path")
    while temperature > final_temp:
        for _ in range(num_iterations):
            new_solution = current_solution[:]
            i, j = random.sample(range(len(new_solution)), 2)
            new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
            new_distance = total_distance(new_solution)
            cost_diff = new_distance - total_distance(current_solution)
            if cost_diff < 0 or random.random() < math.exp(-cost_diff / temperature):
                current_solution = new_solution
                if new_distance < best_distance:
                    best_solution = current_solution[:]
                    best_distance = new_distance
        
        temperature *= alpha
    
    
    return best_solution, best_distance
best_tour, min_distance = simulated_annealing()
best_tour_cities = [cities[i] for i in best_tour]
print("Best order:", " -> ".join(best_tour_cities))
print("Minimum distance:", min_distance)
plot_route(best_tour, "Final Optimized Path", min_distance)
