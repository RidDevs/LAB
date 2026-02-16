#include <iostream>
using namespace std;

class Employee {
public:
    virtual void work() {
        cout << "employee work in office." << endl;
    }
};

class Manager : public Employee {
public:
    void work() {
        cout << "manager manage team." << endl;
    }
};

int main() {
    Employee *e;     
    Manager m;

    e = &m;          
    e->work();       

    return 0;
}
