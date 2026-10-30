#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>

int main(){

    char *tmp="/tmp/abc", a[10];
    int p,i;

    mkfifo (tmp, 0666);

    p=open(tmp, O_RDONLY);

    if (p>=0)
    {
        int n= read(p,a,sizeof(a)-1);
        if (n>=0)
        {
        printf("\nrecieved- %s \n",a);
        }
    }
    else
        printf("\n error");

return 0;}
