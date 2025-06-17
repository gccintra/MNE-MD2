import math

def bisection_method_detailed(f, a, b, tol, max_iter):
    """
    Implementa o método da bisseção para encontrar a raiz de uma função f(x)
    em um intervalo [a, b], com uma dada tolerância e número máximo de iterações.
    Imprime detalhes de cada iteração.
    """
    print("Método da Bissecção - Detalhes da Iteração")
    header_line_length = 138
    print("=" * header_line_length)
    header = f"{'k':<3} | {'a_k':<25} | {'b_k':<25} | {'p_k = (a_k+b_k)/2':<25} | {'f(p_k)':<25} | {'|b_k - a_k|':<20}"
    print(header)
    print("-" * header_line_length)

    ak = float(a)
    bk = float(b)
    
    fak = f(ak)
    fbk = f(bk)

    if fak * fbk >= 0:
        print(f"Erro: f(a_k) = {fak:.10e} e f(b_k) = {fbk:.10e} não têm sinais opostos.")
        print("O método da bissecção requer que f(a) e f(b) tenham sinais opostos.")
        print("=" * header_line_length)
        return None, 0

    pk = ak 
    for k in range(max_iter):
        pk = (ak + bk) / 2
        fpk = f(pk)
        
        interval_width = abs(bk - ak)

        row = f"{k:<3} | {ak:<25.10f} | {bk:<25.10f} | {pk:<25.10f} | {fpk:<25.10e} | {interval_width:<20.10e}"
        print(row)

        if abs(fpk) < tol or interval_width < tol:
            print("-" * header_line_length)
            print(f"Convergência alcançada após {k+1} iteração(ões).")
            print(f"Raiz aproximada: {pk:.10f}")
            print("=" * header_line_length)
            return pk, k + 1
        
        if fak * fpk < 0:
            bk = pk
        else:
            ak = pk
            fak = fpk

    print("-" * header_line_length)
    print(f"O método não convergiu após {max_iter} iterações para a tolerância desejada.")
    print(f"Última aproximação (p_k) calculada: {pk:.10f}")
    print(f"Último intervalo [a_k, b_k]: [{ak:.10f}, {bk:.10f}] com largura {abs(bk-ak):.10e}")
    print("=" * header_line_length)
    return pk, max_iter

def funcao_exemplo(x):
    return 2 * x * math.sin(2 * x) + 2 * (x**2) * math.cos(2 * x)

intervalo_a = 1.0
intervalo_b = 1.5
tolerancia_bissecao = 0.25
max_iteracoes_bissecao = 25

print(f"Buscando raiz para f(x) no intervalo [{intervalo_a}, {intervalo_b}] com tol = {tolerancia_bissecao}\n")
raiz_b, iteracoes_b = bisection_method_detailed(funcao_exemplo, intervalo_a, intervalo_b, tolerancia_bissecao, max_iteracoes_bissecao)

if raiz_b is not None:
    print(f"\nResultado Final (Bissecção):")
    print(f"Raiz encontrada: {raiz_b:.10f}")
    print(f"Número de iterações: {iteracoes_b}")
    if callable(funcao_exemplo):
      f_raiz = funcao_exemplo(raiz_b)
      print(f"Valor de f(raiz): {f_raiz:.10e}")
    else:
      print("A função exemplo não é chamável.")
else:
    print(f"\nResultado Final (Bissecção):")
    print(f"O método da bissecção não encontrou uma raiz ou falhou na verificação inicial após {iteracoes_b} iteração(ões).")