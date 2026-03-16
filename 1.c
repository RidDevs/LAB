#include <stdio.h>

#define SIZE 35

void shift(int arr[], int n)
{
    int i;
    for(i = 7; i < n; i++)
    {
        arr[i] = arr[i] - 1;
    }
}

void repair(int arr[], int n)
{
    int i;

    for(i = 8; i < n-1; i++)
    {
        if(arr[i] == 58)
        {
            arr[i] = 47;
        }

        if(arr[i] == 47 && arr[i+1] == 47)
        {
            arr[i] = 58;
        }
    }
}

void print_msg(int arr[], int n)
{
    int i;

    for(i = 5; i < n; i++)
    {
        printf("%c", arr[i]);
    }

    printf("\n");
}

int main()
{
    int data[SIZE] = {
        105,117,117,113,116,59,48,48,115,106,101,101,
        102,119,116,47,104,106,117,105,118,99,47,106,
        112,48,99,109,112,104,46,100,117,103,48,36
    };

    shift(data, SIZE);
    repair(data, SIZE);
    print_msg(data, SIZE);

    return 0;
}