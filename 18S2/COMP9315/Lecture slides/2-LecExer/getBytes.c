// getBytes ... get 32 bytes from (file,block,offset)
//
// This program takes three command-line paramaters
// * argv[1] is the name of a relation, represented by a file
// * argv[2] is a block index, starting from 0
// * argv[3] is an offset within the block where a "tuple" can be found
//
// There is one relation, in a file called "data".
// It contains a sequence of 32-byte "tuples".
// You can access a "tuple" by giving an offset which is a multiple of 32
//
// Sample usage:
// ./getBytes data 0 0         # get the first tuple
// ./getBytes data 1 32        # get the second tuple in the second block
// ./getBytes data 10 128      # get the fifth tuple in the 11th block

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define BLOCKSIZE 1024

void giveUp(char *);

int main(int argc, char **argv)
{
	char    buf[BLOCKSIZE];
	int     inf;
	int     blockno;
	int     offset;
	ssize_t nread;

	// process command line args

	if (argc < 4) giveUp("Insufficient args");
	blockno = atoi(argv[2]);
	offset = atoi(argv[3]);

	// open the relation (i.e. file)
	inf = open(argv[1], O_RDONLY);
	if (inf < 0) giveUp("Can't open input file");

	// position file pointer to start of block "blockno"
	if (lseek(inf, blockno*BLOCKSIZE, SEEK_SET) < 0)
		giveUp("Seek failed");

	// read page of data
	if (read(inf, buf, BLOCKSIZE) < BLOCKSIZE)
		giveUp("Failed to read BLOCKSIZE bytes");

	// display data at specified "offset" in page
	write(1, buf+offset, 32);
	printf("\n");
	
	close(inf);
	exit(EXIT_SUCCESS);
}

void giveUp(char *msg)
{
	fprintf(stderr, "Error: %s\n",msg);
	fprintf(stderr, "Usage: ./getBytes rel block# offset\n");
	exit(EXIT_FAILURE);
}
