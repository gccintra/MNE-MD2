import math

def f(x):
    return x**3 - math.cos(x)

def regula_falsi(a, b, tol, max_iter):
    if f(a) * f(b) >= 0:
        print("Erro: f(a) e f(b) devem ter sinais opostos.")
        return None, 0

    x_p_anterior = a 
    if abs(f(a)) < tol: # Verifica se 'a' já é a raiz
        print(f"Iteração 0: x_p = {a:.10f}, f(x_p) = {f(a):.10e}, Erro N/A (ponto inicial)")
        return a, 0
    if abs(f(b)) < tol: # Verifica se 'b' já é a raiz
        print(f"Iteração 0: x_p = {b:.10f}, f(x_p) = {f(b):.10e}, Erro N/A (ponto inicial)")
        return b, 0
        
    table_width = 138
    print(f"{'Iter':<4} | {'a':<18} | {'b':<18} | {'f(a)':<20} | {'f(b)':<20} | {'x_p':<18} | {'f(x_p)':<20} | {'|x_p - x_p_ant|':<20}")
    print("-" * table_width)

    for i in range(max_iter):
        f_a = f(a)
        f_b = f(b)
        
        if abs(f_b - f_a) < 1e-12:
            print(f"Iter {i:<4}: Denominador f(b)-f(a) muito pequeno. Interrompendo.")
            return None, i

        x_p = (a * f_b - b * f_a) / (f_b - f_a)
        f_x_p = f(x_p)
        erro = abs(x_p - x_p_anterior)

        print(f"{i:<4} | {a:<18.10f} | {b:<18.10f} | {f_a:<20.10f} | {f_b:<20.10f} | {x_p:<18.10f} | {f_x_p:<20.10e} | {erro:<20.10e}")

        if erro < tol or abs(f_x_p) < 1e-12 : # Adiciona verificação de f_x_p próximo de zero
            print(f"Convergência alcançada após {i+1} iterações.")
            return x_p, i + 1

        if f_a * f_x_p < 0:
            b = x_p
        else:
            a = x_p
        
        x_p_anterior = x_p

    print(f"O método não convergiu após {max_iter} iterações.")
    return x_p, max_iter

a_inicial = 0.0
b_inicial = 1.0
tolerancia = 0.05 
max_iteracoes = 100

print(f"Método Regula Falsi para f(x) = x^3 - cos(x)")
print(f"Intervalo inicial: [{a_inicial}, {b_inicial}], Tolerância para |x_p - x_p_ant|: {tolerancia}\n")

raiz_aprox, num_iters = regula_falsi(a_inicial, b_inicial, tolerancia, max_iteracoes)

if raiz_aprox is not None:
    print(f"\nRaiz aproximada encontrada: {raiz_aprox:.10f}")
    print(f"Número de iterações: {num_iters}")
    print(f"f(raiz_aprox) = {f(raiz_aprox):.10e}")