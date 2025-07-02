import numpy as np
import matplotlib.pyplot as plt

def resolver_sistema_min_quad(X, y):
    """
    Resolve o sistema de equações normais (X.T @ X) @ a = X.T @ y para o vetor de coeficientes 'a'.
    Args:
        X (np.array): A matriz do modelo (design matrix).
        y (np.array): O vetor de observações.
    Returns:
        np.array: O vetor de coeficientes 'a' que minimiza o erro quadrático.
    """
    # (X^T * X) * a = X^T * y
    XTX = X.T @ X
    XTy = X.T @ y
    # Resolve o sistema linear para 'a'
    coeficientes = np.linalg.solve(XTX, XTy)
    return coeficientes

def ajustar_e_plotar(x, y, modelo, grau_poly=None):
    """
    Ajusta os dados a um modelo especificado, imprime os coeficientes e plota o resultado.
    
    Args:
        x (np.array): Dados do eixo x.
        y (np.array): Dados do eixo y.
        modelo (str): O tipo de modelo a ser ajustado ('potencia', 'exponencial', 'polinomial').
        grau_poly (int, optional): O grau do polinômio, necessário se modelo='polinomial'.
    """
    
    print("-" * 60)
    
    if modelo == 'potencia':
        # Linearização: log(y) = log(a) + b*log(x) -> Y = c0 + c1*X' onde X' = log(x)
        log_x = np.log(x)
        log_y = np.log(y)
        # Monta a matriz X para o modelo linearizado Y = c0 + c1*X'
        X_lin = np.vstack([np.ones(len(log_x)), log_x]).T
        # Resolve o sistema. O resultado será [c0, c1] = [log(a), b]
        coeffs_lin = resolver_sistema_min_quad(X_lin, log_y)
        a = np.exp(coeffs_lin[0])
        b = coeffs_lin[1]
        
        titulo = f"Ajuste de Potência: y = a * x^b"
        print(titulo)
        print(f"Coeficientes encontrados: a = {a:.4f}, b = {b:.4f}")
        
        # Gera a curva ajustada
        x_fit = np.linspace(min(x), max(x), 200)
        y_fit = a * (x_fit ** b)
        
    elif modelo == 'exponencial':
        # Linearização: log(y) = log(a) + b*x -> Y = c0 + c1*x
        log_y = np.log(y)
        # Monta a matriz X para o modelo linearizado Y = c0 + c1*x
        X_lin = np.vstack([np.ones(len(x)), x]).T
        # Resolve o sistema. O resultado será [c0, c1] = [log(a), b]
        coeffs_lin = resolver_sistema_min_quad(X_lin, log_y)
        a = np.exp(coeffs_lin[0])
        b = coeffs_lin[1]
        
        titulo = f"Ajuste Exponencial: y = a * exp(b*x)"
        print(titulo)
        print(f"Coeficientes encontrados: a = {a:.4f}, b = {b:.4f}")
        
        # Gera a curva ajustada
        x_fit = np.linspace(min(x), max(x), 200)
        y_fit = a * np.exp(b * x_fit)

    elif modelo == 'polinomial':
        if grau_poly is None:
            raise ValueError("O grau do polinômio (grau_poly) deve ser fornecido para o modelo polinomial.")
            
        # CORREÇÃO: Montar a matriz X de forma explícita para evitar erros de ordenamento.
        # Para um polinômio y = c_n*x^n + ... + c_1*x + c_0,
        # queremos que o vetor de coeficientes seja [c_n, ..., c_1, c_0].
        # Portanto, as colunas da matriz X devem ser [x^n, ..., x^1, x^0].
        
        # Cria uma matriz de zeros com o formato correto (n_pontos, grau + 1)
        X_poly = np.zeros((len(x), grau_poly + 1))
        # Preenche cada coluna com a potência correspondente de x, em ordem decrescente
        for i in range(grau_poly + 1):
            potencia = grau_poly - i
            X_poly[:, i] = x**potencia
            
        # Resolve o sistema. O resultado já estará na ordem correta (potências decrescentes)
        # Ex: para cúbico, coeffs = [a, b, c, d]
        coeffs = resolver_sistema_min_quad(X_poly, y)
        
        # Constrói a string da equação e o título
        graus_str = {1: "Linear", 2: "Quadrático", 3: "Cúbico"}
        termos = []
        letras = ['a', 'b', 'c', 'd', 'e']
        for i, coef in enumerate(coeffs):
            potencia = grau_poly - i
            letra = letras[i]
            print(f"  {letra} = {coef:.4f}")
            if potencia > 1:
                termos.append(f"{coef:.2f}x^{potencia}")
            elif potencia == 1:
                termos.append(f"{coef:.2f}x")
            else:
                termos.append(f"{coef:.2f}")
        
        equacao = "y = " + " + ".join(termos).replace('+ -', '- ')
        titulo = f"Ajuste Polinomial ({graus_str.get(grau_poly, f'Grau {grau_poly}')})"
        
        print(f"\n{titulo}")
        print(f"Equação ajustada: {equacao}")
        
        # Gera a curva ajustada
        p = np.poly1d(coeffs)
        x_fit = np.linspace(min(x), max(x), 200)
        y_fit = p(x_fit)
        
    else:
        print(f"Modelo '{modelo}' não reconhecido.")
        return

    # Plotagem
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, label='Dados Originais', color='blue', zorder=5)
    plt.plot(x_fit, y_fit, label='Função Ajustada', color='red', linewidth=2)
    plt.title(titulo)
    plt.xlabel('x (Coluna 1)')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()
    print("-" * 60 + "\n")


def main():
    # Carregar os dados do arquivo
    try:
        dados = np.loadtxt('data.dat')
    except FileNotFoundError:
        print("Erro: O arquivo 'data.dat' não foi encontrado no mesmo diretório.")
        return
    except ValueError:
        print("Erro: O arquivo 'data.dat' contém dados mal formatados.")
        return

    x = dados[:, 0]

    # Mapeamento das colunas para os modelos
    ajustes = {
        1: {'modelo': 'potencia', 'descricao': 'y = ax^b'},
        2: {'modelo': 'exponencial', 'descricao': 'y = a*exp(b*x)'},
        3: {'modelo': 'polinomial', 'grau': 2, 'descricao': 'y = ax^2+bx+c'},
        4: {'modelo': 'polinomial', 'grau': 1, 'descricao': 'y = ax+b'},
        5: {'modelo': 'polinomial', 'grau': 3, 'descricao': 'y = ax^3+bx^2+cx+d'}
    }

    # Executar os ajustes para as colunas de 2 a 6 (índices 1 a 5)
    for i in range(1, 6):
        print(f"===== Processando Ajuste para (Coluna 1, Coluna {i+1}) =====")
        y = dados[:, i]
        config = ajustes[i]
        ajustar_e_plotar(x, y, config['modelo'], grau_poly=config.get('grau'))

if __name__ == "__main__":
    main()