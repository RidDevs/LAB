#include <stdio.h>

void selectionsort(int arr[],int N)
{
    int i,j,min,temp;

    for(i=0;i<N;i++)
    {min=i;
        for(j=i+1;j<N;j++)
        {if(arr[j]<arr[min])
        {min=j;}
    }

    if (min!=i){
        temp=arr[i];
        arr[i]=arr[min];
        arr[min]=temp;
    }
}
}

int main()
{int l;
    int arr[10]={2,56,78,566,789,34,23,24,56,78};    

    selectionsort(arr,10);

    for(l=0;l<10;l++)
    {printf("%d ",arr[l]);}

return 0;}