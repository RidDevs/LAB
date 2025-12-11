#include <iostream>
using namespace std;


class Grandfather {
public:
    void land() {
        cout << "land." << endl;
    }
};


class Father : public Grandfather {
public:
    void house() {
        cout << "a house." << endl;
    }
};


class Son : public Father {
public:
    Son(){cout << "Son owns" << endl;}
    void bike() {
        cout << " a bike." << endl;
    }
};

int main() {
    Son s;

    s.land();   
    s.house();  
    s.bike();   

    return 0;
}
