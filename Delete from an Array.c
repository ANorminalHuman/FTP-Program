#include <stdio.h>

int main() {
    int arr[5] = {10, 20, 30, 40, 50};
    int pos = 2;

    for(int i = pos; i < 4; i++) {
        arr[i] = arr[i+1]; // Shift elements to the left
    }

    // Print the updated array
    for(int i = 0; i < 4; i++) {
        printf("%d ", arr[i]);
    }

    return 0;
}