#include <iostream>
using namespace std;


class Mammal {
public:
    void birth() {
        cout << "give birth." << endl;
    }
};

class NocturnalAnimal {
public:
    void see() {
        cout << "Nocturnal animal can see at night." << endl;
    }
};


class Bat : public Mammal, public NocturnalAnimal {
public:
    void fly() {
        cout << "Bat can fly." << endl;
    }
};

int main() {
    Bat b;

    b.birth();    
    b.see();   
    b.fly();          

    return 0;
}
