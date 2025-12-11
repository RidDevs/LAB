#include <iostream>
using namespace std;

class Student 
{
int mark;  

public:
    void setMark(int m) 
    { mark = m;}
    friend void showResult(Student s);
};

void showResult(Student s) 
{cout << "Student Marks: " << s.mark << endl;}

int main() {
    Student s1;
    s1.setMark(75);

    showResult(s1);   

    return 0;
}
