#include <stdio.h>


#define MAX_SIZE 123
int i,j;
void insert(int arr[], int *n, int value, int pos) {
    if (*n >= MAX_SIZE || pos < 0 || pos > *n) {
        printf("Insertion not possible.\n");
        return;
    }

    for ( i = *n; i > pos; i--)
        arr[i] = arr[i - 1];
    arr[pos] = value;
    (*n)++;
}

void delete(int arr[], int *n, int pos) {
    if (*n <= 0 || pos < 0 || pos >= *n) {
        printf("Deletion not possible.\n");
        return;
    }   for (i = pos; i < *n - 1; i++)
        arr[i] = arr[i + 1];
    (*n)--;
}

int search(int arr[], int n, int value) {
    for (i = 0; i < n; i++)
        if (arr[i] == value)
            return i;
    return -1;
}

void sort(int arr[], int n) {
    for (i = 0; i < n - 1; i++)
        for (j = 0; j < n - i - 1; j++)
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
}

void display(int arr[], int n) {
    if (n == 0) {
        printf("Array is empty.\n");
        return;
    }
    printf("Array elements: ");
    for (i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

int main() {
    int arr[MAX_SIZE];
    int n = 0, choice, value, pos;

    while (1) {
        printf("\nMenu:\n");
        printf("1. Insert\n2. Delete\n3. Search\n4. Sort\n5. Display\n6. Exit\n");
        printf("Enter selection no.: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter value to insert: ");
                scanf("%d", &value);
                printf("Enter position (0 to %d): ", n);
                scanf("%d", &pos);
                insert(arr, &n, value, pos);
                break;
            case 2:
                printf("Enter position to delete (0 to %d): ", n - 1);
                scanf("%d", &pos);
                delete(arr, &n, pos);
                break;
            case 3:
                printf("Enter value to search: ");
                scanf("%d", &value);
                pos = search(arr, n, value);
                if (pos != -1)
                    printf("Value found at position %d.\n", pos);
                else
                    printf("Value not found.\n");
                break;
            case 4:
                printf("Unorted Array.\n");
                display(arr, n);
                sort(arr, n);
                printf("Sorted Array.\n");
                display(arr, n);
                break;
            case 5:
                display(arr, n);
                break;
            case 6:
                printf("exit success\n");
                return 0;
            default:
                printf("Invalid choice.\n");
        }
    }
}

