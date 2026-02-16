#include <iostream>
using namespace std;
class Customer{
    int age;
    string name;
    static int count;
    public:
    Customer(string n,int a){
        name=n;
        age=a;
        count++;
    }
    static void access(){
        cout<<count<<endl;
    }
    void display(){
        cout<<name<<" "<<age<<endl;
    }
};
int Customer :: count=0;
int main() {
    Customer A1("Raag",20);
    Customer A2("Nibir",34);
    Customer A3("Nibir",34);
    Customer A4("Nibir",34);
    A2.access();
    return 0;
}