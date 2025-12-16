#include <iostream>
using namespace std;

template <class T>

class Stack{

    T arr[100];
    int top;

    public:
    Stack(){top=-1;}

    void push(T a)
    {if (top==99)
        {cout<<"stack full"<<endl;
        return ;}
    arr[++top]= a;
    cout<<"pushed "<< arr[top]<<endl;
    }

    void pop()
    {if (top==-1)
        {cout<<"stack empty"<<endl;

        return ;}
    cout<<"popped " <<arr[top]<<endl;
    top--;}
    
    void peek()
    {if (top==-1)
        {cout<<"stack empty"<<endl;
        return;}
    cout<<"top is " <<arr[top]<<endl;
    top--;

    }

    

};


int main(){

    Stack<int> s;

    s.push(10);
    s.push(20);
     s.peek();
    s.push(30);

    s.peek();

    s.pop();
    s.peek();
    s.pop();
    s.peek();
    s.pop();
    s.pop(); 
    return 0;

}