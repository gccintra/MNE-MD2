import math

# Define the function
def f_new(x):
    return (x**2) * math.sin(2 * x)

x_val = 1.125
result = f_new(x_val)

print(f"Para x = {x_val}, f(x) = {result}")