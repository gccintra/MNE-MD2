#include <stdio.h>
#include "unbounded_integer.h"

int main() {
    struct UnboundedInteger x = unbounded_integer_constructor(1, 2, 
        1234567890123456789ULL, 
        9876543210987654321ULL   
    );

    printf("Hex: %s\n", x.hex);

    unbounded_integer_desctructor(&x);
    return 0;
}
