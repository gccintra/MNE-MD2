#include "unbounded_integer.h"
#include <stdarg.h> 
#include <stdio.h>
#include <string.h>
#include <inttypes.h> 

struct UnboundedInteger unbounded_integer_constructor(short sign, int size, ...) {
    struct UnboundedInteger result;
    result.sign = sign;
    result.size = size;

    result.integer = malloc(sizeof(uint64_t) * size);
    if (!result.integer) {
        fprintf(stderr, "Erro: Falha ao alocar memória para os blocos.\n");
        exit(EXIT_FAILURE);
    }
    

    result.hex = malloc((size * 16 + 1)); 
    result.hex[0] = '\0'; 

    va_list args;
    va_start(args, size);
    for (int i = 0; i < size; i++) {
        result.integer[i] = va_arg(args, uint64_t);
    }
    va_end(args);

    normalize(&result);
    generate_hex_string(&result);

    return result;
}

void unbounded_integer_desctructor(struct UnboundedInteger *bignum) {
    free(bignum->integer);
    free(bignum->hex);

}

struct UnboundedInteger unbounded_integer_add(struct UnboundedInteger a, struct UnboundedInteger b) {
    int max_size = (a.size > b.size) ? a.size : b.size;
    uint64_t *sum = calloc(max_size + 1, sizeof(uint64_t));

    uint64_t carry = 0;
    for (int i = 0; i < max_size; i++) {
        uint64_t a_val = (i < a.size) ? a.integer[i] : 0;
        uint64_t b_val = (i < b.size) ? b.integer[i] : 0;

        __uint128_t temp = (__uint128_t)a_val + (__uint128_t)b_val + carry;
        sum[i] = (uint64_t)temp;
        carry = (uint64_t)(temp >> 64);
    }

    int result_size = max_size;
    if (carry) {
        sum[max_size] = carry;
        result_size++;
    }

    struct UnboundedInteger result;
    result.integer = sum;
    result.size = result_size;
    result.sign = a.sign;
    result.hex = NULL;

    normalize(&result);
    generate_hex_string(&result);

    return result;
}

struct UnboundedInteger unbounded_integer_sub(struct UnboundedInteger a, struct UnboundedInteger b) {
    struct UnboundedInteger result;
    memset(&result, 0, sizeof(result));

    int cmp = compare_abs(&a, &b);
    if (cmp == 0) {
        result.size = 1;
        result.integer = calloc(1, sizeof(uint64_t));
        result.integer[0] = 0;
        result.sign = 1;
        generate_hex_string(&result);
        return result;
    }

    const struct UnboundedInteger *maior, *menor;
    if (cmp > 0) {
        maior = &a;
        menor = &b;
        result.sign = a.sign;
    } else {
        maior = &b;
        menor = &a;
        result.sign = -a.sign;
    }

    result.integer = calloc(maior->size, sizeof(uint64_t));
    result.size = maior->size;

    uint64_t borrow = 0;
    for (int i = 0; i < result.size; i++) {
        uint64_t maior_val = (i < maior->size) ? maior->integer[i] : 0;
        uint64_t menor_val = (i < menor->size) ? menor->integer[i] : 0;

        __uint128_t tmp = (__uint128_t)maior_val - menor_val - borrow;
        result.integer[i] = (uint64_t)tmp;
        borrow = (tmp >> 127) & 1;
    }

    normalize(&result);
    generate_hex_string(&result);

    return result;
}

static int compare_abs(const struct UnboundedInteger *a, const struct UnboundedInteger *b) {
    if (a->size > b->size) return 1;
    if (a->size < b->size) return -1;

    for (int i = a->size - 1; i >= 0; i--) {
        if (a->integer[i] > b->integer[i]) return 1;
        if (a->integer[i] < b->integer[i]) return -1;
    }
    return 0;
}


static void generate_hex_string(struct UnboundedInteger *num) {
    free(num->hex);
    num->hex = calloc(num->size * 17 + 2, sizeof(char));
    int pos = 0;
    if (num->sign < 0) {
        num->hex[pos++] = '-';
    }
    int start_block = num->size - 1;
    int leading_done = 0;

    for (int i = start_block; i >= 0; i--) {
        char buffer[17];
        if (!leading_done) {
            if (num->integer[i] == 0 && i == start_block) {
                sprintf(buffer, "0");
                leading_done = 1;
            } else {
                sprintf(buffer, "%llX", (unsigned long long)num->integer[i]);
                leading_done = 1;
            }
        } else {
            sprintf(buffer, "%016llX", (unsigned long long)num->integer[i]);
        }
        strcat(num->hex + pos, buffer);
        pos = strlen(num->hex);
    }

    if (strcmp(num->hex + (num->sign < 0 ? 1 : 0), "") == 0) {
        strcat(num->hex, "0");
    }
}

static void normalize(struct UnboundedInteger *num) {
    while (num->size > 1 && num->integer[num->size - 1] == 0) {
        num->size--;
    }
}


