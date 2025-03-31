#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 11
#define DIRECTIONS 4

int grid[N][N] = {0};
int Np = 0;
int attempts = 0;

int center = (N % 2 == 0) ? (N / 2) - 1 : (N / 2);

// {Norte, Sul, Oeste, Leste}
int move_i[] = {-1, 1, 0, 0};
int move_j[] = {0, 0, -1, 1};

void print_grid() {
    printf("Número de Pontos Salvos: %d\n\n", Np);
    printf("   ");
    for (int i = 0; i < N; i++) {
        printf("%2d ", i + 1);
    }
    printf("\n");

    for (int i = 0; i < N; i++) {
        printf("%2d ", i + 1);

        for (int j = 0; j < N; j++) {
            if (i == center && j == center) {
                printf("@  ");
            } else {
                printf("%c  ", grid[i][j] ? '#' : '.');
            }
        }
        printf("\n");
    }
    printf("\n");
}

void get_random_empty_cell(int *i, int *j) {
    do {
        *i = rand() % N;
        *j = rand() % N;
    } while (grid[*i][*j] == 1);
}

void verify_point(int i, int j) {
    int direction = rand() % DIRECTIONS;
    int ni, nj;

    if (i == 0 && direction == 0) { 
        ni = N - 1; 
        nj = j;
    } else if (j == 0 && direction == 2) { 
        ni = i;
        nj = N - 1; 
    } else if (i == N - 1 && direction == 1) { 
        ni = 0; 
        nj = j;
    } else if (j == N - 1 && direction == 3) { 
        ni = i;
        nj = 0;
    } else {
        ni = i + move_i[direction];
        nj = j + move_j[direction];
    }

    if (grid[ni][nj] == 1) {
        grid[i][j] = 1;
        Np++;
    }

    // Debug (remover para numeros muito grandes)
    printf("\n\nEscolha Aleatória: i = %d j = %d \n", i + 1, j + 1);
    printf("Direção: %s\n", (direction == 0) ? "Norte" : (direction == 1) ? "Sul" : (direction == 2) ? "Oeste" : "Leste");
    printf("Posição Vizinha: ni = %d nj = %d, Valor = %d \n", ni + 1, nj + 1, grid[ni][nj]);
    printf("Resultado: grid[%d][%d] = %d \n", i + 1, j + 1, grid[ni][nj] == 1 ? 1 : 0);
    print_grid();

    attempts++;
}

int main() {
    srand(time(NULL));

    grid[center][center] = 1;
    Np++;

    printf("\nPonto central definido: grid[%d][%d]\n", center + 1, center + 1);
    print_grid();

    while (Np < (int)((N * N) * 0.1)) {
        int i, j;
        get_random_empty_cell(&i, &j);
        verify_point(i, j);
    }

    printf("Resultado Final: \n\n");
    printf("Número de Tentativas: %d\n", attempts);
    print_grid();

    return 0;
}
