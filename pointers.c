#include <stdio.h>

int main() {
    int a = 10, i = 0, ar[5] = {1, 2, 3, 4, 5};
    int *p = &a;

    for (i = 0; i < 5; i++) {
        printf("%d\n", *p);
    }
    
    return 0;
}

