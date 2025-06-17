import math

def newton_method_detailed(f, df, x0, tol, max_iter):
    print("Método de Newton - Detalhes da Iteração")
    print("=" * 110)
    header = f"{'k':<3} | {'x_k':<20} | {'f(x_k)':<20} | {'df(x_k)':<20} | {'x_k+1':<20} | {'|x_k+1 - x_k|/|x_k+1|':<20}"
    print(header)
    print("-" * 110)

    xk = x0
    for k in range(max_iter):
        fxk = f(xk)
        dfxk = df(xk)

        if abs(dfxk) < 1e-12:
            print(f"Derivada df(x_k) = {dfxk:.10e} é muito próxima de zero em x_k = {xk:.10f}.")
            print("O método pode divergir ou falhou.")
            print("=" * 110)
            return None, k

        xk_plus_1 = xk - fxk / dfxk
        
        error = abs(xk_plus_1 - xk)

        row = f"{k:<3} | {xk:<20.10f} | {fxk:<20.10f} | {dfxk:<20.10f} | {xk_plus_1:<20.10f} | {error:<20.10e}"
        print(row)

        if abs(fxk) < tol or error < tol:
            print("-" * 110)
            print(f"Convergência alcançada após {k+1} iteração(ões).")
            print(f"Raiz aproximada: {xk_plus_1:.10f}")
            print("=" * 110)
            return xk_plus_1, k + 1
        
        xk = xk_plus_1

    print("-" * 110)
    print(f"O método não convergiu após {max_iter} iterações para a tolerância desejada.")
    print(f"Última aproximação calculada: {xk:.10f}")
    print("=" * 110)
    return xk, max_iter

def minha_funcao(x):
    return  2*x*math.sin(2*x) + 2*(x**2) * math.cos(2*x)

def derivada_minha_funcao(x):
    return -4*(x**2) * math.sin(2*x) + 8*x*math.cos(2*x) + 2*math.sin(2*x)

estimativa_inicial = 2.356
tolerancia = 0.25
maximo_iteracoes = 20

print(f"Buscando raiz para f(x) com chute inicial x0 = {estimativa_inicial}\n")
raiz, iteracoes = newton_method_detailed(minha_funcao, derivada_minha_funcao, estimativa_inicial, tolerancia, maximo_iteracoes)
if raiz is not None:
    print(f"\nResultado Final:")
    print(f"Raiz encontrada: {raiz:.10f}")
    print(f"Número de iterações: {iteracoes}")
    print(f"Valor de f(raiz): {minha_funcao(raiz):.10e}")
else:
    print(f"\nResultado Final:")
    print(f"O método não encontrou uma raiz sob as condições dadas após {iteracoes} iteração(ões).")