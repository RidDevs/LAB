#include <stdio.h>
#include <unistd.h>

void bubble_sort(int arr[],int len){
    int i,j,temp;
    for(i=0;i<len-1;i++){
        for(j=0;j<len-i-1;j++){
            if(arr[j]>arr[j+1]){
                temp=arr[j];
                arr[j]=arr[j+1];
                arr[j+1]=temp;
            }
        }
    }
}

int main(){

    int p, i1, i2, ar1[2],ar2[2];

    i1=pipe(ar1);
    i2=pipe(ar2);

    if(i1==0 ||i2==0){
            p=fork();
            
            if(p<0)
                {printf("fork creation failed");}
            if(p==0)
                {   int a[]={11,14,16,9,4,1};
                    printf("\n child process \n");
                    printf("writing data in pipe \n");
                    write(ar1[1],a,24);

                    int maxin;
                    read(ar2[0],&maxin,4);
                    printf("\n parent- max val= %d \n",maxin);
                }

            else
                {   int b[6];
                    read(ar1[0],b,24);
                    printf("\n parent process \n");
                    printf("data recieving \n");
                  
                    bubble_sort(b,6);
                    int x;
                    for(x=0;x<6;x++)
                    {printf("%d,",b[x]);}
                    
                    int max=b[5];

                    write(ar2[1],&max,4);
                    
                }
        }
    else
        {printf("pipe failed");}
    return 0;
}
