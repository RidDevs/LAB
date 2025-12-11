#include <iostream>
using namespace std;

class Student;   
class Teacher{
    public:
    void showMarks(Student &s);
};

class Student {
    int marks;   

public:
    Student() {
        marks = 90;
    }

    friend class Teacher;
};

void Teacher::showMarks(Student &s) {
    cout << "Marks: " << s.marks << endl;
}

int main() {
    Student s1;
    Teacher t1;
    t1.showMarks(s1);
    return 0;
}
