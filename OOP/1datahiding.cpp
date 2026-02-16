#include<iostream>
using namespace std;

class game {
    private:
        int score;   // here, data hiding is used
    public:
        void setScore(int s) {
            score = s;
        }
        void showScore() {
            cout <<"Score = "<< score;
        }
};

int main() {
    game g;
    g.setScore(85);
    g.showScore();
    return 0;
}