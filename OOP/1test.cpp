#include<iostream>
using namespace std;

class exam{
private: int data;
public:  
    void setdata(int m){
        data=m;
    }
    void getdata(){
        cout<<"marks id"<<data;
    }
};

int main() {
    
    exam e;
    e.setdata(100);
    e.getdata();
    return 0;
}
