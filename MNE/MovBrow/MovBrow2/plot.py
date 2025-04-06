import numpy as np
import matplotlib.pyplot as plt

def load_data(filename):
    grid = np.zeros((250, 250))
    with open(filename, "r") as file:
        for line in file:
            parts = line.split()  
            x, y = int(parts[0]), int(parts[1])  
            grid[y, x] = 1  
    return grid

def plot_grid(grid):
    plt.figure(figsize=(10, 10), )
    plt.imshow(grid, cmap="Greens", interpolation="nearest") 
    plt.title("MovBrow", color="black")
    plt.xlabel("X", color="black")
    plt.ylabel("Y", color="black")
    plt.xticks(color="black")
    plt.yticks(color="black")
    plt.gca().invert_yaxis()
    plt.grid(False)  
    plt.show()


if __name__ == "__main__":
    grid = load_data("output.dat")
    plot_grid(grid)