#include <iostream>
using namespace std;

class Add {
public:
    Add(int a, int b) {
        cout << a + b << endl;
    }
    Add(int a, int b, int c) {
        cout << a + b + c << endl;
    }
};

int main() {
    Add (9,90);
    Add (19,92,73);
    return 0;
}
