#include <iostream>
using namespace std;

class Student {
public:
    string name;
    int marks;
};

int main(){
    Student s[3];

    s[0].name= "helo"; s[0].marks=99;
    s[1].name= "helo"; s[1].marks=99;
    s[2].name= "helo"; s[2].marks=99;

    for(int i=0;i<3;i++){
        cout<< s[i].name<<"scored"<<s[i].marks<<endl;
    }

    return 0;

}