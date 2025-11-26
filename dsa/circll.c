#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

struct Node* head = NULL;


struct Node* createNewNode(int value) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = value;
    newNode->next = NULL;
    return newNode;
}


void insertBegin(int value) {
    struct Node* newNode = createNewNode(value);
    if (head == NULL) {
        head = newNode;
        head->next = head; 
    } else {
        struct Node* temp = head;
        while (temp->next != head)
            temp = temp->next;
        newNode->next = head;
        temp->next = newNode;
        head = newNode;
    }
    printf("%d inserted at begin\n", value);
}


void insertEnd(int value) {
    struct Node* newNode = createNewNode(value);
    if (head == NULL) {
        head = newNode;
        head->next = head;
    } else {
        struct Node* temp = head;
        while (temp->next != head)
            temp = temp->next;
        temp->next = newNode;
        newNode->next = head;
    }
    printf("%d inserted at end.\n", value);
}

void insertPos(int value, int pos) {
    int i;
    struct Node* newNode = createNewNode(value);
    if (head == NULL || pos == 1) {
        insertBegin(value);
        return;
    }

    struct Node* temp = head;
    for (i = 1; i < pos - 1 && temp->next != head; i++)
        temp = temp->next;

    newNode->next = temp->next;
    temp->next = newNode;
    printf("%d inserted at pos %d.\n", value, pos);
}


void deleteBegin() {
    if (head == NULL) {
        printf("List is empty.\n");
        return;
    }

    struct Node* temp = head;
    if (head->next == head) {
        free(head);
        head = NULL;
    } else {
        struct Node* last = head;
        while (last->next != head)
            last = last->next;
        head = head->next;
        last->next = head;
        free(temp);
    }
    printf("Node deleted from beginning.\n");
}


void deleteEnd() {
    if (head == NULL) {
        printf("List is empty.\n");
        return;
    }

    struct Node* temp = head;
    if (head->next == head) {
        free(head);
        head = NULL;
    } else {
        struct Node* prev = NULL;
        while (temp->next != head) {
            prev = temp;
            temp = temp->next;
        }
        prev->next = head;
        free(temp);
    }
    printf("Node deleted from end.\n");
}

void deletePos(int pos) {

    int i;
    if (head == NULL) {
        printf("List is empty.\n");
        return;
    }

    if (pos == 1) {
        deleteBegin();
        return;
    }

    struct Node* temp = head;
    struct Node* prev = NULL;
    for (i = 1; i < pos && temp->next != head; i++) {
        prev = temp;
        temp = temp->next;
    }

    if (temp == head) {
        printf("Invalid position!\n");
        return;
    }

    prev->next = temp->next;
    free(temp);
    printf("Node deleted from position %d.\n", pos);
}

void display() {
    if (head == NULL) {
        printf("List is empty.\n");
        return;
    }
    struct Node* temp = head;
    printf("Circular Linked List: ");
    do {
        printf("%d ", temp->data);
        temp = temp->next;
    } while (temp != head);
    printf("\n");
}

void search(int val) {
    if (head == NULL) {
        printf("!!!!!List empty.\n");
        return;
    }

    struct Node* temp = head;
    int pos = 1;
    int found = 0;

    do {
        if (temp->data == val) {
            printf("Element %d found at position %d.\n", val, pos);
            found = 1;
            break;
        }
        temp = temp->next;
        pos++;
    } while (temp != head);

    if (!found)
        printf("Element %d not found in the list.\n", val);
}


int main() {
    int choice, value, pos, val;

    while (1) {
        printf("\n circular linkedlist\n");

        printf(" INSERT \n");
        printf("1. at Beginning\n");
        printf("2. at End\n");
        printf("3. at Position\n");

        printf(" DELETE \n");
        printf("4. from Beginning\n");
        printf("5. from End\n");
        printf("6. from Position\n \n");

        printf("7. Search\n");
        printf("8. Display\n");

        printf("9. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter value: ");
                scanf("%d", &value);
                insertBegin(value);
                break;
            case 2:
                printf("Enter value: ");
                scanf("%d", &value);
                insertEnd(value);
                break;
            case 3:
                printf("Enter value and position: ");
                scanf("%d %d", &value, &pos);
                insertPos(value, pos);
                break;
            case 4:
                deleteBegin();
                break;
            case 5:
                deleteEnd();
                break;
            case 6:
                printf("Enter position to delete: ");
                scanf("%d", &pos);
                deletePos(pos);
                break;
            
             case 7:     
             printf("Enter value to find: ");
                scanf("%d", &val);
                search(val); 
                break;
            
                case 8:
                display();
                break;
                
           
            case 9:
                exit(0);
            default:
                printf("error\n");
        }
    }

    return 0;
}
