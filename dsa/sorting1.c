#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// #define N 1000000   

// int arr[N];         

// void unique_numbers() {
//     int i;
//     for ( i = 0; i < N; i++){
//         arr[i] = i + 1;  }
//     for ( i = N - 1; i > 0; i--) {
//         int j = rand() % (i + 1);
//         int temp = arr[i];
//         arr[i] = arr[j];
//         arr[j] = temp;
//     }
// }

int arr[10]={2,56,78,566,789,34,23,24,56,78};         



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


void insertion_sort(int arr[],int len){
    int i,j,temp;
    for(i=1;i<len;i++){
        int temp =arr[i];
        int j=i-1;
        while( j>=0 && arr[j]>temp){
            arr[j+1]=arr[j];
            j=j-1;
        }
        arr[j+1]=temp;
    }
}

void selection_sort(int arr[],int len){
    int i,j,min;
    for(i=0;i<len;i++){
        min=i;        
        for(j=i+1;j<len;j++){
            
            if(arr[j]<arr[min]){
                min=j;
            } }
        
        if(min!=i){
           
                int temp;
                temp=arr[i];
                arr[i]=arr[min];  //swap i and min
                arr[min]=temp;
            }
        }
        }
  
 


void merge(int arr[],int left,int mid,int right){
    int i,j,k;
    i=left;
    j=mid+1;
    k=left;
    
    static int b[N];

    while(i<=mid && j<=right){
        if(arr[i]<=arr[j]){
            b[k]=arr[i];
            i++;
            k++;
            
        }
        else{
            b[k]=arr[j];
            k++;
            j++;
        }
    }
    if(i>mid){
        while(j<=right){
            b[k]=arr[j];
            j++;
            k++;
            
        }
    }
    else{
        while(i<=mid){
            b[k]=arr[i];
            i++;
            k++;
        }
    }
    for(k=left;k<=right;k++){
        arr[k]=b[k];
        
    }
}

void merge_sort(int arr[],int left,int right) {
    if (left<right) {
        int mid=(left+right)/2;

        merge_sort(arr, left, mid);      
        merge_sort(arr,mid + 1,right); 

        merge(arr,left,mid,right);   
    }
}


int partition(int arr[],int left,int right){
    int start,end,pivot;
    pivot=arr[left];
    start=left;
    end=right;
    while(start<end){
        while(start <= right && arr[start]<=pivot){
            start++;
        }
        while(end >= left && arr[end] > pivot){
            end--;
        }
        if(start<end){
            int temp;
            temp=arr[start];
            arr[start]=arr[end];
            arr[end]=temp;
        }
    }
    
    int temp;
    temp=arr[left];
    arr[left]=arr[end];
    arr[end]=temp;
    return end;
 }

void quick_sort(int arr[],int left,int right){
    if(left<right){
        int lock;
        lock=partition( arr,left,right);
        quick_sort(arr, left, lock-1);
        quick_sort( arr, lock+1, right);
    }
}


int main() {
    int choice ;
    srand(time(NULL));
    unique_numbers();
    
    
while(1){
    printf("---SORTING MENU---\n");
    printf("1.Bubble sort\n");
    printf("2.Insertion sort\n");
    printf("3.Selection sort\n");
    printf("4.Merge sort\n");
    printf("5.Quick sort\n");
    printf("6.Exit\n");
    printf("Enter your choice : ");
    scanf("%d",&choice);
    
    switch(choice){
        case 1:
            printf("Start\n");
            bubble_sort(arr,N);
            printf("Sorting completed!\n");
            break;
        case 2:
            printf("Start\n");
            insertion_sort(arr,N);
            printf("Sorting completed!\n");
            break;
        case 3:
            printf("Start \n");
            selection_sort(arr,N);
            printf("Sorting completed!\n");
            break;
        case 4:
            printf("Start \n");
            merge_sort(arr,0,N-1);
            printf("Sorting completed!\n");
            break;
        case 5:
            printf("Start\n");
            quick_sort(arr,0,N-1);
            printf("Sorting completed!\n");
            break;
        case 6:
            return 0;
        default:
            printf("Invalid choice\n");
    }
}
}