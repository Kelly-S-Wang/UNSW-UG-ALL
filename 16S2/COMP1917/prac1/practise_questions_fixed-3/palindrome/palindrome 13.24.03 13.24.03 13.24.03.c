#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "palindrome.h"

#define FIRST_ARG 1

int main (int argc, char * argv[]) {
    assert(argc > 1);
    int i;
    for (i = 1; i < argc; i++) {
        if (isPalindrome(argv[i])) {
            printf("palindrome\n");
        } else {
            printf("not palindrome\n");
        }
    }
    return EXIT_SUCCESS;
}
