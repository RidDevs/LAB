#include <iostream>
using namespace std;

#define SIZE 100

int arr[SIZE];

// Stack variables (0 to 49)
int top = -1;

// Queue variables (50 to 99)
int front = 50;
int rear = 49;

/* -------- STACK FUNCTIONS -------- */
void push(int x) {
    if (top == 49) {
        cout << "Stack Overflow\n";
        return;
    }
    arr[++top] = x;
    cout << x << " pushed to stack\n";
}

void pop() {
    if (top == -1) {
        cout << "Stack Underflow\n";
        return;
    }
    cout << arr[top--] << " popped from stack\n";
}

/* -------- QUEUE FUNCTIONS -------- */
void enqueue(int x) {
    if (rear == 99) {
        cout << "Queue Overflow\n";
        return;
    }
    arr[++rear] = x;
    cout << x << " inserted into queue\n";
}

void dequeue() {
    if (front > rear) {
        cout << "Queue Underflow\n";
        return;
    }
    cout << arr[front++] << " removed from queue\n";
}

/* -------- MAIN -------- */
int main() {
    // Stack operations
    push(10);
    push(20);
    pop();

    cout << endl;

    // Queue operations
    enqueue(30);
    enqueue(40);
    dequeue();

    return 0;
}
