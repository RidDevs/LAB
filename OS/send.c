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
    printf("\n enter the string \n");
    scanf("%s",a);

    p=open(tmp, O_WRONLY);

    if (p>=0)
    {
        write(p,a,strlen(a));
    }
    else
        printf("\n error");

return 0;}
