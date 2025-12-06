#include <iostream>
using namespace std;

class Student {
    int roll;
public:
    void setRoll(int r) {
        roll = r;
    }
    void display() {
        cout << roll << endl;
    }
};

int main() {
    Student s[3];
    for(int i=0;i<3;i++)
        s[i].setRoll(i+1);

    for(int i=0;i<3;i++)
        s[i].display();

    return 0;
}
