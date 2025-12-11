#include <iostream>
using namespace std;

class Animal 
{
public:
    void eat() {
        cout << "I can Eat" << endl;
    }
    void sleep() {
        cout << "I can Sleep" << endl;
    }
};

class Dog : public Animal 
{
public:
    void bark() {
        cout << "I can Bark" << endl;
    }
};

int main() {
    Dog d;
    d.eat();
    d.sleep();
    d.bark();
    return 0;
}
