/* Assignment 2  (Indidvidual Submission)
done by Mihir Vipradas (1810110130)

The output is of the format: 1st line ->one sorted half of the array, second line-> second sorted half, third line-> merged and sorted complete array.  Changes to the original array must be done in the c file itself, as global array cannot be of variable size

Please disregard the first attempt.﻿﻿

*/

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>


int arr[]={7,12,19,3,18,4,2,6,15,8,9,10};//unsorted array
int n=sizeof(arr)/sizeof(arr[0]);
int sortedarr[sizeof(arr)/sizeof(arr[0])];//another global array of same size 
typedef struct para{//creating structure for parameters as described in the question
int start;
int end;
} parameters; 

typedef struct arguments//structure to pass arguments (addresses of sorted half-arrays)to third thread
{
int *p;
int *q;
} args;

void* merge(void* a) //merging two sorted arrays
{ 
    args *ar=(args *)a;
    int *x=ar->p;
    int *y=ar->q;
    int n1=(n/2);
    int n2=(n-n1);
    int i = 0, j = 0, k = 0; 
  
   
    while (i<n1 && j <n2) 
    { 
        
        if (*(x+i) < *(y+j)) 
            sortedarr[k++] = *(x+i++); 
        else
            sortedarr[k++] = *(y+j++); 
    } 
    while (i < n1) 
        sortedarr[k++] = *(x+i++); 
   while (j < n2) 
        sortedarr[k++] = *(y+j++); 
return NULL;
} 

void swap(int *x, int*y)
{
int temp= *x;
*x=*y;
*y=temp;
}



void * sort(void *a)          // sorting halves of array using bubble sort                        
{
    
        parameters *pa = (parameters *)a;
        int k=(pa->end)-(pa->start)+1;
        int z=(pa->start);
      
        int *x=(int *)malloc(k* sizeof(int));
        int i, j;  
            for(i=0;i<k;i++)
        {
             *(x+i)=arr[z+i];
             
        }
    for (i = 0; i < k-1; i++) {
    for (j = 0; j < k-i-1; j++) 
       {
      
       if (*(x+j) > *(x+j+1))  
       swap((x+j),(x+j+1));
       }
  }

for(i=0;i<k;i++)
        {
           
             printf("%d ",*(x+i));
        }


printf("\n");
return x;
      
}

void main()
{
    
    
    parameters fa,sa;
    args mergeptr; 
    fa.start=0;   // creating parameters for passing the indices for sorting
    fa.end=(n/2)-1;
    sa.start=(n/2);
    sa.end=n-1;
    
    

    pthread_t thread1,thread2,thread3;                                        
    pthread_create (&thread1, NULL, sort, &fa);//these two threads concurrently sort two halves of the array, thread 1 from [0 to N/2-1] and thread 2 from[n/2 to n-1 ]
    pthread_create (&thread2, NULL, sort, &sa);  
    int *ar1,*ar2;
                    
    pthread_join(thread1, (void*)&ar1); 
    pthread_join(thread2, (void*)&ar2); 
    
   
    mergeptr.p=ar1;
    mergeptr.q=ar2;
    pthread_create (&thread3, NULL, merge, &mergeptr); // third thread to merge.
    pthread_join(thread3, NULL);
    for (int i=0;i<n;i++)
    printf("%d ",sortedarr[i]);
    printf("\n");                             
        
    

}
