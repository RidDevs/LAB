#include <stdio.h>
#include <unistd.h>
int main(){

    int p, i, ar[2];

    i=pipe(ar);

    if(i==0){
            p=fork();
            
            if(p<0)
                {printf("pipe creation failed");}
            if(p==0)
                {   char a[]="hello";
                    printf("\n child process \n");
                    printf("writing data in pipe \n");
                    write(ar[1],a,5);
                }

            else
                {   char b[10];
                    read(ar[0],b,5);
                    printf("\n parent process \n");
                    printf("\n %s \n",b);
                }
        }
    else
        {printf("pipe failed");}
    return 0;
}
