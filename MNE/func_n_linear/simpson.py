import math

def f(x):
  return x**2 * math.sin(2 * x)

def simpson_3_8(func, a, b):
  if a == b:
    return 0.0

  h = (b - a) / 3.0

  x0 = a
  x1 = a + h
  x2 = a + 2 * h
  x3 = b 

  integral = (3.0 * h / 8.0) * (func(x0) + 3 * func(x1) + 3 * func(x2) + func(x3))
  return integral

x_g = 3.141
x_h = 4.71   


area = simpson_3_8(f, x_g, x_h)
print(f"A função a ser integrada é: F(x) = x^2 * sin(2x)")
print(f"O limite inferior de integração (x de G) é: {x_g}")
print(f"O limite superior de integration (x de H) é: {x_h}")
print(f"A área calculada usando o método de Simpson 3/8 (não composto) é: {area:.6f}")
