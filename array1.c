#include <stdio.h>

int main() {
    int arr[5]; // Declare an array of size 5
    arr[0] = 10; // Assign values to array elements
    arr[1] = 20;
    arr[2] = 30;
    arr[3] = 40;
    arr[4] = 50;

    // Loop to print array elements
    for(int i = 0; i < 5; i++) {
        printf("Element at index %d: %d\n", i, arr[i]);
    }

    return 0;
}