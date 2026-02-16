#include <iostream>
using namespace std;

class Student {
    int marks;        // private data

public:
    Student() {
        marks = 85;
    }
    friend class Teacher;   // Teacher is a friend
};

class Teacher {
public:
    void showMarks(Student s) {
        cout << "Marks = " << s.marks << endl;
    }
};

int main() {
    Student s1;
    Teacher t;
    t.showMarks(s1);
    return 0;
}
