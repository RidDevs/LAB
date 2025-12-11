#include <iostream>
using namespace std;

class base {
public:
    base() {
        cout << "Constructor" << endl;
    }
    ~base() {
        cout << "Destructor" << endl;
    }
};

int main() {
    base b;
    return 0;
}
