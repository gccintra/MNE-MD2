import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def load_data(filename):
    x_points = []  
    y_steps = []   
    points = 0  

    with open(filename, "r") as file:
        for line in file:
            parts = line.split("|")
            if len(parts) < 3:
                continue  

            try:
                steps_value = int(parts[2].split("=")[-1].strip())  
                points += 1  
                x_points.append(points)
                y_steps.append(steps_value)
            except ValueError:
                continue

    return x_points, y_steps

def plot_graph(x_points, y_steps):
    plt.figure(figsize=(8, 5))
    plt.plot(x_points, y_steps, color='blue', marker='o', markersize=2, linestyle='-')
    plt.xlabel("Quantidade de pontos marcados")
    plt.ylabel("Passos até ponto válido")
    plt.title("Relação entre Pontos Marcados e Passos Necessários")
    plt.grid(True)

    plt.gca().xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))
    plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))


    plt.show()

if __name__ == "__main__":
    x_points, y_steps = load_data("output.dat")
    plot_graph(x_points, y_steps)
