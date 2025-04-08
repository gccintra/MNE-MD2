#include "unbounded_integer.h"
#include <stdarg.h> 
#include <stdio.h>
#include <string.h>
#include <inttypes.h> // Para usar PRIX64 com uint64_t

struct UnboundedInteger unbounded_integer_constructor(short sign, int size, ...) {
    struct UnboundedInteger result;
    result.sign = sign;
    result.size = size;

    // Aloca memória para os inteiros
    result.integer = malloc(sizeof(uint64_t) * size);

    // Aloca memória para a string hexadecimal (cada uint64_t pode ter até 16 caracteres + 1)
    result.hex = malloc((size * 16 + 1)); 
    result.hex[0] = '\0'; // Inicializa a string como vazia

    // Pega os argumentos variáveis
    va_list args;
    va_start(args, size);
    for (int i = 0; i < size; i++) {
        result.integer[i] = va_arg(args, uint64_t);

        // Converte cada inteiro para hexadecimal e concatena
        char x[17]; // até 16 dígitos + '\0'
        sprintf(x, "%" PRIX64, result.integer[i]);
        strcat(result.hex, x);
    }
    va_end(args);

    return result;
}

void unbounded_integer_desctructor(struct UnboundedInteger *bignum) {
    free(bignum->integer);
    free(bignum->hex);
}
