#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 250
#define DIRECTIONS 4

int grid[N][N] = {0};
int Np = 0;
int attempts = 0;

int center = (N % 2 == 0) ? (N / 2) - 1 : (N / 2);

// {Norte, Sul, Oeste, Leste}
int move_i[] = {-1, 1, 0, 0};
int move_j[] = {0, 0, -1, 1};

void get_random_empty_cell(int *i, int *j) {
    do {
        *i = rand() % N;
        *j = rand() % N;
    } while (grid[*i][*j] == 1);
}

void verify_point(int i, int j, FILE *file) {
    int total_steps = 1;
    int fist_i = i;
    int first_j = j;

    while (1) { 
        int direction = rand() % DIRECTIONS;
        int ni = (i + move_i[direction] + N) % N;
        int nj = (j + move_j[direction] + N) % N;

        if (grid[ni][nj] == 1) {
            grid[i][j] = 1;
            fprintf(file, "%d %d | First point = %d %d | Total Steps until valid point = %d\n", i, j, fist_i, first_j, total_steps);
            Np++;
            return;
        } else {
            i = ni;
            j = nj;
            total_steps++;
        }
        attempts++;
    }
}

int main() {
    srand(time(NULL));

    FILE *file = fopen("output.dat", "w");
    if (file == NULL) {
        printf("Erro ao criar arquivo de saída.\n");
        return 1;
    }   

    grid[center][center] = 1;
    fprintf(file, "%d %d | First point = %d %d | Total Steps until valid point = %d\n", center, center, center, center, 1);

    Np++;

    while (Np < (int)((N * N) * 0.1)) {
        int i, j;
        get_random_empty_cell(&i, &j);
        verify_point(i, j, file);
    }

    fclose(file);
    return 0;
}
