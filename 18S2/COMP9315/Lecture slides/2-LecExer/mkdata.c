// make some data for getBytes.c to read

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
	char data[20];
	int  i,j;
	FILE *outf;

	if ((outf = fopen("data","w")) == NULL) exit(1);

	for (i = 1; i < 100000; i++) {
		for (j = 0; j < 20; j++) {
			data[j] = 'a' + (rand()%12);
		}
		fprintf(outf,"Tuple %06d %19.19s",i,data);
	}
	fclose(outf);
	exit(0);
}
