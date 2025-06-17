import math

def secant_method_detailed(f, x0, x1, tol, max_iter):
    print("Método das Secantes - Detalhes da Iteração")
    table_width = 95 
    print("=" * table_width)
    # Header: Iter k | x_k      | f(x_k)     | x_(k+1)    | |x_k+1 - x_k|
    header = f"{'Iter k':<7} | {'x_k':<18} | {'f(x_k)':<20} | {'x_(k+1)':<18} | {'|x_k+1 - x_k|':<20}"
    print(header)
    print("-" * table_width)

    # Iteração k=0: Mostra x0 como x_k, e x1 como x_(k+1) para esta linha.
    # f(x_k) é f(x0). |x_k+1 - x_k| é |x1 - x0|.
    f_x0 = f(x0)
    error_initial = abs(x1 - x0) 
    row_0 = f"{0:<7} | {x0:<18.10f} | {f_x0:<20.10f} | {x1:<18.10f} | {error_initial:<20.10e}"
    print(row_0)

    # Verifica convergência com base em f(x0) ou se x0 é suficientemente próximo de x1 (se tol for muito grande)
    if abs(f_x0) < tol:
        print("-" * table_width)
        print(f"Convergência: f(x_k) para k=0 (f(x0)) está dentro da tolerância.")
        print(f"Raiz aproximada: {x0:.10f}")
        print("=" * table_width)
        return x0, 0 # 0 cálculos de secante realizados

    # Prepara para o loop das iterações de cálculo (k=1 em diante)
    # Para a primeira iteração do loop (k=1):
    # x_k_minus_1 (o x_{k-1} da fórmula) será x0
    # x_k (o x_k da fórmula) será x1
    x_k_minus_1 = x0
    x_k = x1
    
    # Loop para k = 1, 2, ..., max_iter
    # max_iter é o número máximo de aplicações da fórmula das secantes.
    for k_iter_num in range(1, max_iter + 1):
        f_k_minus_1 = f(x_k_minus_1) # Este é f(x_{k-1})
        f_k = f(x_k)                 # Este é f(x_k)

        # Verifica convergência com base em f(x_k) antes de calcular x_{k+1}
        # Para k_iter_num=1, x_k é x1. Se f(x1) já for pequeno, x1 é a raiz.
        if abs(f_k) < tol:
            print("-" * table_width)
            print(f"Convergência: f(x_k) para k={k_iter_num} está dentro da tolerância antes de calcular x_(k+1).")
            print(f"Raiz aproximada: {x_k:.10f}")
            print("=" * table_width)
            return x_k, k_iter_num 

        denominator = f_k - f_k_minus_1
        if abs(denominator) < 1e-12:
            # Mensagem de erro na tabela para a iteração k atual
            print(f"Iter k={k_iter_num}: Denominador |f(x_k) - f(x_k-1)| = {abs(denominator):.2e} é muito próximo de zero.")
            print("O método pode divergir ou falhou.")
            print("=" * table_width)
            return None, k_iter_num # Retorna o k da iteração que falhou

        # Fórmula das Secantes para calcular x_{k+1}
        if abs(x_k - x_k_minus_1) < 1e-12 : # Evita divisão por zero se x_k e x_{k-1} são idênticos
             x_k_plus_1 = x_k 
        else:
             x_k_plus_1 = (x_k_minus_1 * f_k - x_k * f_k_minus_1) / denominator

        error = abs(x_k_plus_1 - x_k) # Este é |x_{k+1} - x_k|
        
        # Na linha da tabela para Iter k:
        # x_k é o valor atual de x_k (que foi x1 na primeira iteração do loop)
        # f(x_k) é f_k
        # x_(k+1) é o x_k_plus_1 recém-calculado
        # O erro é |x_k_plus_1 - x_k|
        row_k = f"{k_iter_num:<7} | {x_k:<18.10f} | {f_k:<20.10f} | {x_k_plus_1:<18.10f} | {error:<20.10e}"
        print(row_k)

        # Critério de parada baseado no erro ou no valor da função em x_{k+1}
        if error < tol or abs(f(x_k_plus_1)) < tol:
            print("-" * table_width)
            print(f"Convergência alcançada na Iteração k={k_iter_num} (após cálculo de x_{k_iter_num+1}).")
            print(f"Raiz aproximada: {x_k_plus_1:.10f}")
            print("=" * table_width)
            return x_k_plus_1, k_iter_num # Retorna o k da iteração que convergiu
        
        # Atualiza para a próxima iteração
        x_k_minus_1 = x_k
        x_k = x_k_plus_1

    print("-" * table_width)
    print(f"O método não convergiu após {max_iter} iterações para a tolerância desejada.")
    print(f"Última aproximação calculada (x_{max_iter+1}): {x_k:.10f}") # x_k aqui é o último x_k_plus_1
    print("=" * table_width)
    return x_k, max_iter

def minha_funcao(x):
    return 2*x*math.sin(2*x) + 2*(x**2) * math.cos(2*x)


estimativa_inicial_0 = 3.5
estimativa_inicial_1 = 4.5
tolerancia = 0.25
maximo_iteracoes = 10 # Número de cálculos da secante (k=1 até max_iter)


print(f"Buscando raiz para f(x) com chutes iniciais x0 = {estimativa_inicial_0}, x1 = {estimativa_inicial_1}\n")
raiz, iteracoes_k = secant_method_detailed(minha_funcao, estimativa_inicial_0, estimativa_inicial_1, tolerancia, maximo_iteracoes)
if raiz is not None:
    print(f"\nResultado Final:")
    print(f"Raiz encontrada: {raiz:.10f}")
    # 'iteracoes_k' é o valor de k onde a convergência ocorreu ou max_iter.
    # Se k=0, significa que x0 foi a raiz.
    # Se k > 0, significa que k aplicações da fórmula da secante foram feitas.
    if iteracoes_k == 0:
        print(f"Número de iterações de cálculo (k): 0 (x0 já era a raiz ou próximo dela)")
    else:
        print(f"Número de iterações de cálculo (k): {iteracoes_k}")
    print(f"Valor de f(raiz): {minha_funcao(raiz):.10e}")
else:
    print(f"\nResultado Final:")
    print(f"O método não encontrou uma raiz sob as condições dadas após {iteracoes_k} iteração(ões) de cálculo (k).")