#include <iostream>
using namespace std;

template <class T>

class Box {
public:
    T value;

    void set(T v) 
    {   value = v;}
    void show() 
    {   cout << value << endl;}
};

int main() {
    Box<int> b1;        
    Box<float> b2;      

    b1.set(10);
    b2.set(2.5);

    b1.show();
    b2.show();

    return 0;
}
