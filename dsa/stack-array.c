#include <stdio.h>
#define SIZE 100

int stack[SIZE];
int top = -1;

void push(int value) {
    if (top == SIZE - 1) {
        printf("Stack full!!!! \n");
    } else {
        stack[++top] = value;
        printf("%d pushed\n", value);
    }
}

void pop() {
    if (top == -1) {
        printf("Stack empty!!!! \n");
    } else {
        printf("%d popped\n", stack[top--]);
    }
}

void display() {
    if (top == -1) {
        printf("Stack is Empty\n");
    } else {
        printf("Stack elements: ");
        for (int i = top; i >= 0; i--) {
            printf("%d ", stack[i]);
        }
        printf("\n");
    }
}

int main() {
    int choice, value;

    while (1) {
        printf("\n -StackArray \n");
        printf("1. Push\n");
        printf("2. Pop\n");
        printf("3. Display\n");
        printf("4. Exit\n");
        printf("Enter your choice: \n ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter value to push: ");
                scanf("%d", &value);
                push(value);
                break;
            case 2:
                pop();
                break;
            case 3:
                display();
                break;
            case 4:
                return 0;
            default:
                printf("Invalid!!! \n");
        }
    }
}
