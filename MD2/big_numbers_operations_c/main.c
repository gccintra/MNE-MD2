#include <stdio.h>
#include <inttypes.h>
#include <string.h>
#include "unbounded_integer.h"


int main() {
    struct UnboundedInteger x = unbounded_integer_constructor(1, 2, 
        0x783913FACBE92313, 
        0xFFFFFFFFFFA8319F
    );

    struct UnboundedInteger y = unbounded_integer_constructor(1, 2, 
        0x9999913FACBE931E, 
        0xFFF222FFFFA8319F
    );

    struct UnboundedInteger sum = unbounded_integer_add(x, y);
    struct UnboundedInteger diff = unbounded_integer_sub(x, y);
    printf("sum hex: %s\n", sum.hex);
    printf("diff hex: %s\n", diff.hex);

    
    unbounded_integer_desctructor(&x);
    unbounded_integer_desctructor(&y);
    unbounded_integer_desctructor(&sum);
    unbounded_integer_desctructor(&diff);
    return 0;
}
