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
    cout << s.add(10, 20) << endl;
    cout << s.add(2.5f, 4.5f);
    return 0;
}
