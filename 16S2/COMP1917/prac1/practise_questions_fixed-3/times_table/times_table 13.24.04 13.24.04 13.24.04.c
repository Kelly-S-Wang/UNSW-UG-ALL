#include <stdio.h>
#include <stdlib.h>
#include "times_table.h"

int main (int argc, char * argv[]) {
    
    int t[SIZE][SIZE];
    
    make_table(t);
    print_table(t);
    
    return EXIT_SUCCESS;
}

void print_table(int table[SIZE][SIZE]) {
    int i,j;
    
    for (i = 0; i < SIZE; i++) {
        for (j = 0; j < SIZE; j++) {
            printf("%3d ",table[i][j]);
        }
        printf("\n");
    }
    
}