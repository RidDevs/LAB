#include <iostream>
using namespace std;

class Sum{
    public:
        int add(int a, int b) 
        {return a + b;}
        float add(float a, float b) 
        {return a + b;}
};

int main() {
    Sum s;
    cout << s.add(100, 21) << endl;
    cout << s.add(7.1f, 9.5f);
    return 0;
}
