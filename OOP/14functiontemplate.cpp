#include <iostream>
using namespace std;

template <class A>
A add(A a, A b) {
    return a + b;
}

int main() {
    cout << add(56,78) << endl;
    cout << add(2.89,9.8);
    return 0;
}
