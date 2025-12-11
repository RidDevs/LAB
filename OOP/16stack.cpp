#include <iostream>
using namespace std;

template <class T>
class Stack 
{
    T arr[100];
    int top;
public:
    Stack() 
    {   top = -1;}

    void push(T x) 
    {   arr[++top] = x;}

    void pop() 
    {   cout << arr[top--] << "popped" << endl;}
};

int main() {
    Stack<int> s;
    s.push(1);
    s.push(2);
    s.pop();
    return 0;
}
