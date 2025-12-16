#include <iostream>
using namespace std;

class employee{
    public: virtual void work()
        {cout << "emp" << endl;}
};

class manager : public employee{
    public: void work(){
        cout<< "manager"<< endl;
    }
};

int main(){
    employee *e;
    manager m;
    e= &m;
     
    e->work();
    return 0;
}