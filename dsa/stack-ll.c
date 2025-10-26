#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

struct Node* top = NULL;

void push(int value) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    if (newNode == NULL) {
        printf("Memory issue!\n");
        return;
    }
    newNode->data = value;
    newNode->next = top;
    top = newNode;
    printf("%d pushed\n", value);
}

void pop() {
    if (top == NULL) {
        printf("Stack error!!!!\n");
    } else {
        printf("%d popped\n", top->data);
        struct Node* temp = top;
        top = top->next;
        free(temp);
    }
}

void display() {
    if (top == NULL) {
        printf("Stack is Empty\n");
    } else {
        struct Node* temp = top;
        printf("Stack elements: ");
        while (temp != NULL) {
            printf("%d ", temp->data);
            temp = temp->next;
        }
        printf("\n");
    }
}

int main() {
    int choice, value;

    while (1) {
        printf("\n-StackLinkedlist-\n");
        printf("1. Push\n");
        printf("2. Pop\n");
        printf("3. Display\n");
        printf("4. Exit\n");
        printf("Enter choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter value: ");
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
               
                exit(0);
            default:
                printf("Invalid!!\n");
        
    }

    return 0;
}
