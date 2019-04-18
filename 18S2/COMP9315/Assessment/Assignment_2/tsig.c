// tsig.c ... functions on Tuple Signatures (tsig's)
// part of SIMC signature files
// Written by John Shepherd, September 2018

#include <unistd.h>
#include <string.h>
#include "defs.h"
#include "tsig.h"
#include "reln.h"
#include "hash.h"
#include "bits.h"

// Generate codeword

Bits codeword(char *attr_value, int m, int k)
{
   int nbits = 0; // count of set bits
   Bits cword = newBits(m); // assuming m <= 32 bits
   srandom(hash_any(attr_value, strlen(attr_value)));
   while (nbits < k) {
      int i = random() % m;
      if (!bitIsSet(cword, i)) {
      	setBit(cword, i);
      	nbits++;
      }
   }
   return cword; // m-bits with k 1-bits and m-k 0-bits
}


Bits makeTupleSig(Reln r, Tuple t)
{
	assert(r != NULL && t != NULL);
	Bits tsig = newBits(tsigBits(r));
	assert(tsig != NULL);
	char **vals = tupleVals(r, t); // Change to attributes list
	int i;

	// Foreach attributes make codeword
	for (i = 0; i < nAttrs(r); i++) {
		if (strcmp(vals[i], "?") == 0) {} // For query
		else {
			Bits cw = codeword(vals[i], tsigBits(r), codeBits(r)); 
			orBits(tsig, cw); // Or to make page sig
			freeBits(cw);
		}
	}
	return tsig;
}


void findPagesUsingTupSigs(Query q)
{
	assert(q != NULL);
	Reln r = q->rel;
	Bits qsig = makeTupleSig(r, q->qstring);
	q->curpage = 0;
	int prev_tpp = 0;

	// Locate to page
	while (q->curpage < nTsigPages(r)) {
		
		Page p = getPage(tsigFile(r), q->curpage);
		q->curtup = 0;

		// Locate to tuple sig in page
		while (q->curtup < pageNitems(p)) {

			Bits tsig = newBits(tsigBits(r));
			getBits(p, q->curtup, tsig);

			// Set bit if is subset
			if (isSubset(qsig, tsig)) {
				int indexTup = (q->curpage)*prev_tpp + (q->curtup);
				int indexPage = indexTup/maxTupsPP(r);
				setBit(q->pages, indexPage);
			}

			freeBits(tsig);
			q->nsigs++;
			q->curtup++;
		}

		q->nsigpages++;
		q->curpage++;
		prev_tpp = pageNitems(p);
	}

	freeBits(qsig);
	// Remove it before submitting this function
	// printf("Matched Pages:"); showBits(q->pages); putchar('\n');
}
