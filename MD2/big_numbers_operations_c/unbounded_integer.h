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

#endif