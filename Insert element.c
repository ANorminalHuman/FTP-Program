#include <stdio.h>

int main() {
    int arr[6] = {10, 20, 30, 40, 50};  // array of size 6, but 5 elements are filled

    int element = 25, pos = 2;
    for(int i = 5; i >= pos; i--) {
        arr[i] = arr[i-1]; // Shift elements to the right
    }
    arr[pos] = element; // Insert the new element

    // Print the new array
    for(int i = 0; i < 6; i++) {
        printf("%d ", arr[i]);
    }

    return 0;
}
