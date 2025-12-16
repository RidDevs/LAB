#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

struct Node* front = NULL;
struct Node* rear = NULL;

void enqueue(int value) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    
    if (newNode == NULL) {
        printf("MemoryERROR!\n");
        return;
    }
    newNode->data = value;
    newNode->next = NULL;

    if (rear == NULL) {
        front = rear = newNode;
    } else {
        rear->next = newNode;
        rear = newNode;
    }
    printf("%d queued\n", value);
}

void dequeue() {
    if (front == NULL) {
        printf("Queue ERROR\n");
    } else {
        printf("%d dequeued\n", front->data);
        struct Node* temp = front;
        front = front->next;
        if (front == NULL) {
            rear = NULL;
        }
        free(temp);
    }
}

void display() {
    if (front == NULL) {
        printf("Queue is Empty\n");
    } else {
        struct Node* temp = front;
        printf("Queue elements: ");
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
        printf("\n-QueueLinked List\n");
        printf("1. queue\n");
        printf("2. Dequeue\n");
        printf("3. Display\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter value to enqueue: ");
                scanf("%d", &value);
                enqueue(value);
                break;
            case 2:
                dequeue();
                break;
            case 3:
                display();
                break;
            case 4:
               
                exit(0);
            default:
                printf("Invalid!!!!\n");
        }
    }

    return 0;
}
