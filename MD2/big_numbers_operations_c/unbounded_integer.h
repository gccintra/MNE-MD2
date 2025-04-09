#ifndef UNBOUNDED_INTEGER_H
#define UNBOUNDED_INTEGER_H

#include <stdlib.h>
#include <stdint.h>

struct UnboundedInteger
{
    uint64_t *integer;
    short sign;
    int size;
    char *hex;
};
struct UnboundedInteger unbounded_integer_constructor(short sign, int size, ...);
void unbounded_integer_desctructor(struct UnboundedInteger *bignum);
static void generate_hex_string(struct UnboundedInteger *num);
static void normalize(struct UnboundedInteger *num);
struct UnboundedInteger unbounded_integer_add(struct UnboundedInteger a, struct UnboundedInteger b);
struct UnboundedInteger unbounded_integer_sub(struct UnboundedInteger a, struct UnboundedInteger b);
static int compare_abs(const struct UnboundedInteger *a, const struct UnboundedInteger *b);

#endif