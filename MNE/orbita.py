import math
import os
import time

# --- Configurações da Tela ASCII ---
LARGURA_TELA = 70
ALTURA_TELA = 20
CHAR_PONTO_USUARIO = 'O'
CHAR_CAMINHO_SUAVE = '*'
CHAR_VAZIO = ' '

# --- Funções de Interpolação (Spline Catmull-Rom) ---
def catmull_rom_point(P0, P1, P2, P3, t):
    """Calcula um ponto em um segmento de spline Catmull-Rom para um dado t (0 a 1)."""
    t2 = t * t
    t3 = t2 * t
    
    # Coeficientes da matriz Catmull-Rom (para tau=0.5 implícito na fórmula abaixo)
    # q(t) = 0.5 * ( (2 * P1) +
    #                (-P0 + P2) * t +
    #                (2 * P0 - 5 * P1 + 4 * P2 - P3) * t^2 +
    #                (-P0 + 3 * P1 - 3 * P2 + P3) * t^3 )

    out_x = 0.5 * ( (2 * P1[0]) +
                    (-P0[0] + P2[0]) * t +
                    (2 * P0[0] - 5 * P1[0] + 4 * P2[0] - P3[0]) * t2 +
                    (-P0[0] + 3 * P1[0] - 3 * P2[0] + P3[0]) * t3 )

    out_y = 0.5 * ( (2 * P1[1]) +
                    (-P0[1] + P2[1]) * t +
                    (2 * P0[1] - 5 * P1[1] + 4 * P2[1] - P3[1]) * t2 +
                    (-P0[1] + 3 * P1[1] - 3 * P2[1] + P3[1]) * t3 )
    return (out_x, out_y)

def get_catmull_rom_segment_coeffs(P0, P1, P2, P3):
    """
    Calcula os coeficientes dos polinômios cúbicos x(t) e y(t) para um segmento
    de spline Catmull-Rom entre P1 e P2, com t variando de 0 a 1.
    x(t) = Ax*t^3 + Bx*t^2 + Cx*t + Dx
    y(t) = Ay*t^3 + By*t^2 + Cy*t + Dy
    """
    coeffs_x = {
        'A': 0.5 * (-P0[0] + 3*P1[0] - 3*P2[0] + P3[0]),
        'B': 0.5 * (2*P0[0] - 5*P1[0] + 4*P2[0] - P3[0]),
        'C': 0.5 * (-P0[0] + P2[0]),
        'D': P1[0] # que é 0.5 * (2*P1[0])
    }
    coeffs_y = {
        'A': 0.5 * (-P0[1] + 3*P1[1] - 3*P2[1] + P3[1]),
        'B': 0.5 * (2*P0[1] - 5*P1[1] + 4*P2[1] - P3[1]),
        'C': 0.5 * (-P0[1] + P2[1]),
        'D': P1[1] # que é 0.5 * (2*P1[1])
    }
    return {'x': coeffs_x, 'y': coeffs_y}

def gerar_caminho_e_polinomios(pontos_usuario, pontos_por_segmento=10):
    """
    Gera um caminho suave e os polinômios de cada segmento.
    """
    if not pontos_usuario or len(pontos_usuario) < 2:
        return [], []

    caminho_interpolado = []
    polinomios_segmentos = []

    if len(pontos_usuario) == 2: # Interpolação linear
        P1, P2 = pontos_usuario[0], pontos_usuario[1]
        for i in range(pontos_por_segmento + 1):
            t = i / float(pontos_por_segmento)
            x = P1[0] * (1 - t) + P2[0] * t
            y = P1[1] * (1 - t) + P2[1] * t
            caminho_interpolado.append((x, y))
        
        # Polinômio linear: P(t) = (P2-P1)t + P1 = Ct + D
        coeffs_x = {'A': 0, 'B': 0, 'C': P2[0] - P1[0], 'D': P1[0]}
        coeffs_y = {'A': 0, 'B': 0, 'C': P2[1] - P1[1], 'D': P1[1]}
        polinomios_segmentos.append({
            'P1': P1, 'P2': P2,
            'coeffs_x': coeffs_x, 'coeffs_y': coeffs_y
        })
        return caminho_interpolado, polinomios_segmentos

    caminho_interpolado.append(pontos_usuario[0])

    for i in range(len(pontos_usuario) - 1):
        P1 = pontos_usuario[i]
        P2 = pontos_usuario[i+1]

        P0 = pontos_usuario[i-1] if i > 0 else P1
        P3 = pontos_usuario[i+2] if i < len(pontos_usuario) - 2 else P2
        
        coeffs = get_catmull_rom_segment_coeffs(P0, P1, P2, P3)
        polinomios_segmentos.append({
            'P1': P1, 'P2': P2, # Pontos que este segmento conecta
            'P0': P0, 'P3': P3, # Pontos de controle usados
            'coeffs_x': coeffs['x'], 'coeffs_y': coeffs['y']
        })

        for j in range(1, pontos_por_segmento + 1): # Ponto P1 (t=0) já foi adicionado ou é o primeiro ponto global
            t = j / float(pontos_por_segmento)
            ponto_spline = catmull_rom_point(P0, P1, P2, P3, t)
            caminho_interpolado.append(ponto_spline)
            
    return caminho_interpolado, polinomios_segmentos


# --- Funções de Tela ASCII --- (mantidas do código anterior)
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def criar_canvas_vazio(largura, altura):
    return [[CHAR_VAZIO for _ in range(largura)] for _ in range(altura)]

def desenhar_ponto_no_canvas(canvas, x, y, char, min_coord_x, max_coord_x, min_coord_y, max_coord_y):
    largura_mundo = max_coord_x - min_coord_x
    altura_mundo = max_coord_y - min_coord_y
    if largura_mundo <= 1e-6: largura_mundo = 1.0 
    if altura_mundo <= 1e-6: altura_mundo = 1.0
    col_tela = int(((x - min_coord_x) / largura_mundo) * (LARGURA_TELA - 1))
    lin_tela = int(((max_coord_y - y) / altura_mundo) * (ALTURA_TELA - 1))
    if 0 <= lin_tela < ALTURA_TELA and 0 <= col_tela < LARGURA_TELA:
        canvas[lin_tela][col_tela] = char

def imprimir_canvas(canvas, titulo_extra=""):
    limpar_tela()
    print(f"Seu Caminho Suavizado (O: Pontos Originais, *: Caminho Suave) {titulo_extra}")
    print("+" + "-" * LARGURA_TELA + "+")
    for linha in canvas:
        print("|" + "".join(linha) + "|")
    print("+" + "-" * LARGURA_TELA + "+")

# --- Loop Principal ---
def main():
    pontos_usuario = []
    print("Digite as coordenadas (x y) do caminho")
    print("valores de X entre ~0-150 e Y entre ~0-50")

    while True:
        entrada = input(f"Ponto {len(pontos_usuario) + 1} (x y) ou 'fim': ").strip()
        if entrada.lower() == 'fim':
            if len(pontos_usuario) < 2:
                print("Você precisa de pelo menos 2 pontos para criar um caminho.")
                if input("Tentar novamente? (s/n): ").lower() != 's':
                    return
                else:
                    continue
            break
        try:
            partes = entrada.split()
            if len(partes) != 2:
                raise ValueError("Por favor, insira dois números separados por espaço.")
            x, y = float(partes[0]), float(partes[1])
            pontos_usuario.append((x, y))
        except ValueError as e:
            print(f"Entrada inválida: {e}. Use o formato 'x y' (ex: '10 20') ou digite 'fim'.")

    if not pontos_usuario:
        print("Nenhum ponto inserido. Saindo.")
        return

    caminho_suave, polinomios_segmentos = gerar_caminho_e_polinomios(pontos_usuario, pontos_por_segmento=15)

    todos_os_pontos_para_escala = pontos_usuario + caminho_suave
    if not todos_os_pontos_para_escala:
        print("Nenhum ponto para desenhar. Saindo.")
        return

    min_x = min(p[0] for p in todos_os_pontos_para_escala)
    max_x = max(p[0] for p in todos_os_pontos_para_escala)
    min_y = min(p[1] for p in todos_os_pontos_para_escala)
    max_y = max(p[1] for p in todos_os_pontos_para_escala)
    margem_x = (max_x - min_x) * 0.10 if (max_x - min_x) > 1e-6 else 1.0
    margem_y = (max_y - min_y) * 0.10 if (max_y - min_y) > 1e-6 else 1.0
    final_min_x, final_max_x = min_x - margem_x, max_x + margem_x
    final_min_y, final_max_y = min_y - margem_y, max_y + margem_y
    if final_max_x <= final_min_x: final_max_x = final_min_x + 1.0
    if final_max_y <= final_min_y: final_max_y = final_min_y + 1.0

    for i, ponto_anim in enumerate(caminho_suave):
        canvas = criar_canvas_vazio(LARGURA_TELA, ALTURA_TELA)
        for ponto in caminho_suave:
            desenhar_ponto_no_canvas(canvas, ponto[0], ponto[1], CHAR_CAMINHO_SUAVE,
                                     final_min_x, final_max_x, final_min_y, final_max_y)
        for ponto_u in pontos_usuario:
            desenhar_ponto_no_canvas(canvas, ponto_u[0], ponto_u[1], CHAR_PONTO_USUARIO,
                                     final_min_x, final_max_x, final_min_y, final_max_y)
        desenhar_ponto_no_canvas(canvas, ponto_anim[0], ponto_anim[1], '@',
                                 final_min_x, final_max_x, final_min_y, final_max_y)
        imprimir_canvas(canvas, f"| Passo: {i+1}/{len(caminho_suave)}")
        # print(f"Coordenadas atuais: ({ponto_anim[0]:.1f}, {ponto_anim[1]:.1f})") # Removido para não poluir a animação
        time.sleep(0.05)

   # print("\n--- Polinômios dos Segmentos (para t de 0 a 1 em cada segmento) ---")
    for i, seg_info in enumerate(polinomios_segmentos):
        p1 = seg_info['P1']
        p2 = seg_info['P2']
        cx = seg_info['coeffs_x']
        cy = seg_info['coeffs_y']
        
        print(f"\nSegmento {i+1}: De ({p1[0]:.1f}, {p1[1]:.1f}) a ({p2[0]:.1f}, {p2[1]:.1f})")
        if len(pontos_usuario) > 2 : # Somente para Catmull-Rom, não para linear de 2 pontos.
             p0_disp = seg_info.get('P0', p1) # Usa P1 se P0 não existir (caso de 2 pontos, embora já tratado)
             p3_disp = seg_info.get('P3', p2) # Usa P2 se P3 não existir
             print(f"  Usando controles P0:({p0_disp[0]:.1f},{p0_disp[1]:.1f}), P1:({p1[0]:.1f},{p1[1]:.1f}), P2:({p2[0]:.1f},{p2[1]:.1f}), P3:({p3_disp[0]:.1f},{p3_disp[1]:.1f})")

        print(f"  x(t) = {cx['A']:.2f}*t^3 + {cx['B']:.2f}*t^2 + {cx['C']:.2f}*t + {cx['D']:.2f}")
        print(f"  y(t) = {cy['A']:.2f}*t^3 + {cy['B']:.2f}*t^2 + {cy['C']:.2f}*t + {cy['D']:.2f}")

    print("\nfinalizado.")

if __name__ == "__main__":
    main()