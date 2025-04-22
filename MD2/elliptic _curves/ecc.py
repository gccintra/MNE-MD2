O = None

def print_point(p):
    if p is O:
        print("O (Ponto no Infinito)", end="")
    else:
        print(f"({p[0]}, {p[1]})", end="")

def mod_mul(a, b, p):
    return (a * b) % p

def mod_add(a, b, p):
    return (a + b) % p  

def mod_sub(a, b, p):
    return (a - b) % p

# Pequeno Teorema de Fermat
def mod_inverse(a, p):
    a = mod_add(a, 0, p)
    return pow(a, p - 2, p)

# Adição de pontos P + Q na curva y^2 = x^3 + ax + b (mod p)
def point_add(P, Q, a, p):
    if P is O:
        return Q
    if Q is O:
        return P

    if P[0] == Q[0]:
        if P[1] == Q[1]: # se P == Q
            return point_double(P, a, p)
        else: # Se P != Q mas x_p == x_q, então P = -Q
            return O

    # P != Q e P.x != Q.x
    # s = (yQ - yP) / (xQ - xP) mod p
    num = mod_sub(Q[1], P[1], p)
    den = mod_sub(Q[0], P[0], p)

    if den == 0: # ja fiz essa tratativa ali em cima, mas é bom pra robustez
        return O

    s = mod_mul(num, mod_inverse(den, p), p)

    # xR = (s^2 - xP - xQ) mod p
    xR = mod_sub(mod_sub(mod_mul(s, s, p), P[0], p), Q[0], p)

    # yR = (s * (xP - xR) - yP) mod p
    yR = mod_sub(mod_mul(s, mod_sub(P[0], xR, p), p), P[1], p)

    return (xR, yR)

# Duplicação de ponto P + P = 2P na curva y^2 = x^3 + ax + b (mod p)
def point_double(P, a, p):
    if P is O:
        return O 
    if P[1] == 0: # y=0, tangente vertical
        return O 

    # s = (3*xP^2 + a) / (2*yP) mod p
    num = mod_add(mod_mul(3, mod_mul(P[0], P[0], p), p), a, p)
    den = mod_mul(2, P[1], p)

    if den == 0:
        return O

    s = mod_mul(num, mod_inverse(den, p), p)

    # xR = (s^2 - 2*xP) mod p
    xR = mod_sub(mod_mul(s, s, p), mod_mul(2, P[0], p), p)

    # yR = (s * (xP - xR) - yP) mod p
    yR = mod_sub(mod_mul(s, mod_sub(P[0], xR, p), p), P[1], p)

    return (xR, yR)

def scalar_multiply(k, P, a, p):
    result = O         
    current = P         

    if k == 0:
        return O

    while k > 0:
        if k % 2 == 1:
            result = point_add(result, current, a, p)
        current = point_double(current, a, p)
        k = k // 2

    return result

p = 17
a = 2
b = 2
G = (5, 1) 

print(f"Curva Elíptica: y^2 = x^3 + {a}x + {b} (mod {p})")
print(f"Ponto Gerador (G): ", end="")
print_point(G)
print()

while True:
    try:
        k = int(input("\nDigite o valor de k para calcular kG: "))
        break
    except ValueError:
        print("Entrada inválida. Por favor, digite um número inteiro.")

result_kG = scalar_multiply(k, G, a, p)

print(f"\nO resultado de {k}G é: ", end="")
print_point(result_kG)
print()