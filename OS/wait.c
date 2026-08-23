#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
int main(){

    int p;
    p=fork();
    if(p<0)
        {printf("pipe creation failed");}
    if(p==0)
        {wait(NULL);
        printf("\n child process \n");}
    else
        {printf("\n parent process \n");}

    return 0;
}
