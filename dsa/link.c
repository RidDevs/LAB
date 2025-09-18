#include <stdio.h>
#include <stdlib.h>

struct node {
        int data;
        struct node * link;
};

int main(){
        struct node *new, *start;
        start = NULL;
        int a;
        printf("insert data\n");
        scanf("%d",&a);

        new=malloc(sizeof(struct node));

        new->data=a;
        new->link=NULL;

        if(start==NULL)
        {
        start=new;
        }

        printf("\n %d \n",start->data);
return 0;

}
