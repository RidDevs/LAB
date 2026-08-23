#include <stdio.h>
#include <unistd.h>
int main(){

    int p, i, ar[2];

    i=pipe(ar)
    p=fork();
    
    if(p<0)
        {printf("pipe creation failed");}
    if(p==0)
        {printf("\n child process \n");}
    else
        {printf("\n parent process \n");}

    return 0;
}
