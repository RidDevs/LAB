#include <stdio.h>
#define SIZE 5

int queue[SIZE];
int front = -1, rear = -1;

void enqueue(int value) {
    if (rear == SIZE - 1) {
        printf("Queue ERR\n");
    } else {
        if (front == -1) front = 0;
        queue[++rear] = value;
        printf("%d queued\n", value);
    }
}

void dequeue() {
    if (front == -1 || front > rear) {
        printf("Queue ERROR\n");
    } else {
        printf("%d dequeued\n", queue[front++]);
    }
}

void display() {
    if (front == -1 || front > rear) {
        printf("Queue is Empty\n");
    } else {
        printf("Queue elements: ");
        for (int i = front; i <= rear; i++) {
            printf("%d ", queue[i]);
        }
        printf("\n");
    }
}

int main() {
    int choice, value;

    while (1) {
        printf("\n QueueArray \n");
        printf("1. queue\n");
        printf("2. Dequeue\n");
        printf("3. Display\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter value to queue: ");
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
                
                return 0;
            default:
                printf("Invalid choice! Try again.\n");
        }
    }

    return 0;
}
