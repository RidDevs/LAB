#include <stdio.h>
#include <stdlib.h>

// Define structure for a tree node
struct Node {
    int data;
    struct Node* left;
    struct Node* right;
};

// Function to create a new node
struct Node* createNode(int value) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = value;
    newNode->left = NULL;
    newNode->right = NULL;
    return newNode;
}

// Function to insert nodes manually (not BST insertion)
struct Node* insertLeft(struct Node* root, int value) {
    root->left = createNode(value);
    return root->left;
}

struct Node* insertRight(struct Node* root, int value) {
    root->right = createNode(value);
    return root->right;
}

// Traversal functions
void inorder(struct Node* root) {
    if (root == NULL)
        return;
    inorder(root->left);
    printf("%d ", root->data);
    inorder(root->right);
}

void preorder(struct Node* root) {
    if (root == NULL)
        return;
    printf("%d ", root->data);
    preorder(root->left);
    preorder(root->right);
}

void postorder(struct Node* root) {
    if (root == NULL)
        return;
    postorder(root->left);
    postorder(root->right);
    printf("%d ", root->data);
}

int main() {
    // Create root
    struct Node* root = createNode(1);
    // Manually insert other nodes
    struct Node* left = insertLeft(root, 2);
    struct Node* right = insertRight(root, 3);
    insertLeft(left, 4);
    insertRight(left, 5);
    insertLeft(right, 6);
    insertRight(right, 7);

    printf("Inorder traversal: ");
    inorder(root);

    printf("\nPreorder traversal: ");
    preorder(root);

    printf("\nPostorder traversal: ");
    postorder(root);

    return 0;
}
