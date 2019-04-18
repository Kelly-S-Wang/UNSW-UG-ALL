#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

void giveUp(char *);

int main(int argc, char **argv)
{
	char    buf[1024];
	int     inf, outf;  // file descriptors
	ssize_t nread;

	// process command line args

	if (argc < 2) giveUp("Insufficient args");
	inf = open(argv[1], O_RDONLY);
	if (inf < 0) giveUp("Can't open input file");
	outf = open("output.txt", O_CREAT|O_WRONLY, 0644);
	if (outf < 0) giveUp("Can't open output file");

	// read file and write output.txt

	while ((nread = read(inf, buf, 1024)) > 0) {
		if (write(outf, buf, nread) != nread)
			giveUp("Write error");
	}
	close(inf);
	close(outf);

	// read part of output.txt

	inf = open("output.txt", O_RDONLY);
        if (inf < 0) giveUp("Can't open output.txt for reading");
	if (lseek(inf, 2000, SEEK_SET) < 0) giveUp("Seek failed");
	if (read(inf, buf, 10) < 10) giveUp("Failed to read 10 bytes");

	// display results
	write(1, buf, 10);
	printf("\n");
	
	exit(EXIT_SUCCESS);
}

void giveUp(char *msg)
{
	fprintf(stderr, "Error: %s\n",msg);
	fprintf(stderr, "Usage: ./blocks BlockSize InputFile\n");
	exit(EXIT_FAILURE);
}
