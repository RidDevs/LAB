#include <iostream>
using namespace std;

class Demo {
    static bool destroyed;

public:
    Demo() {
        cout << "Constructor is invoked" << endl;
    }

    Demo(int v) {
        cout << "Value is = " << v << endl;
    }

    ~Demo() {
        if (!destroyed) {
            cout << "Destructor is invoked" << endl;
            destroyed = true;
        }
    }
};

bool Demo::destroyed = false;

int main() {
    Demo d1;
    cout << "In the main" << endl;
    Demo d2(10);
    return 0;
}
