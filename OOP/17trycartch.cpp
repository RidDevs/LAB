#include <iostream>
using namespace std;

int main() {
    int a = 1, b = 0;
    try {
        if(b == 0)
            throw b;
        cout << a / b;
    }
    catch(int x) {
        cout << "Error";
    }
    return 0;
}
