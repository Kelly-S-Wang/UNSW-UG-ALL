// bsig.c ... functions on Tuple Signatures (bsig's)
// part of SIMC signature files
// Written by John Shepherd, September 2018

#include "defs.h"
#include "reln.h"
#include "query.h"
#include "bsig.h"
#include "tsig.h"
#include "psig.h"

void findPagesUsingBitSlices(Query q)
{
	assert(q != NULL);
	Reln r = q->rel;

	int checker[nPages(r)], i, counter = 0;
	for (i = 0; i < nPages(r); i++) checker[i] = 0;

	Bits qsig = makePageSig(r, q->qstring);

	// q->curpage = 0;
	// while(q->curpage < nBsigPages(r)) {
	// 	Page bp = getPage(bsigFile(r), q->curpage);

	// 	printf("%d\n", pageNitems(bp));
	// 	q->curtup = 0;
	// 	while (q->curtup < pageNitems(bp)) {
	// 		if (bitIsSet(qsig, (q->curpage)*maxBsigsPP(r)+(q->curtup))) {
	// 			counter++;
	// 			Bits bslice = newBits(bsigBits(r));
	// 			getBits(bp, q->curtup, bslice);
	// 			for (i = 0; i < nPsigs(r); i++)
	// 				if (bitIsSet(bslice, i))
	// 					checker[i]++;
	// 			freeBits(bslice);
	// 		}
	// 		q->curtup++;
	// 		q->nsigs++;
	// 	}
	// 	q->curpage++;
	// 	q->nsigpages++;
	// }

	for (int b = 0; b < psigBits(r); b++){ // For all bits in qsig
		if (bitIsSet(qsig, b)) {

			counter++;
			q->nsigs++;
			Page bp = getPage(bsigFile(r), b/maxBsigsPP(r));
			Bits bitslice = newBits(bsigBits(r));
			getBits(bp, b % maxBsigsPP(r), bitslice);

			// Horizontal check
			for (i = 0; i < nPsigs(r); i++)
				if (bitIsSet(bitslice, i))
					checker[i]++;
			freeBits(bitslice);

		}
		if (b%maxBsigsPP(r) == 0) q->nsigpages++;
	}

	// Vertical chcek
	for (i = 0; i < nPages(r); i++)
		if (checker[i] == counter)
			setBit(q->pages, i);

	// printf("Matched Pages:"); showBits(q->pages); putchar('\n');
}
