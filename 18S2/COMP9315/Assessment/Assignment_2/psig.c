// psig.c ... functions on page signatures (psig's)
// part of SIMC signature files
// Written by John Shepherd, September 2018


#include "defs.h"
#include "reln.h"
#include "query.h"
#include "psig.h"
#include "tsig.h"

Bits makePageSig(Reln r, Tuple t)
{
	assert(r != NULL && t != NULL);
	Bits psig = newBits(psigBits(r));
	assert(psig != NULL);
	char ** vals = tupleVals(r, t);
	int i;

	// Foreach attributes make codeword
	for (i = 0; i < nAttrs(r); i++) {
		if (strcmp(vals[i], "?") == 0) {} // For query
		else {
			Bits cw = codeword(vals[i], psigBits(r), codeBits(r)); 
			orBits(psig, cw); // Or to make page sig
			freeBits(cw);
		}
	}
	return psig;
}


void findPagesUsingPageSigs(Query q)
{
	assert(q != NULL);
	Reln r = q->rel;
	Bits qsig = makePageSig(r, q->qstring);
	q->curpage = 0;

	// Locate to page
	while (q->curpage < nPsigPages(r)) {
		
		Page p = getPage(psigFile(r), q->curpage);
		q->curtup = 0;
		
		// Locate to the page sig in page
		while (q->curtup < pageNitems(p)) {

			Bits psig = newBits(psigBits(r));
			getBits(p, q->curtup, psig);

			// Set bit if is subset
			if (isSubset(qsig, psig)) {
				int indexPage = (q->curpage)*maxPsigsPP(r) + (q->curtup);
				setBit(q->pages, indexPage);
			}

			freeBits(psig);
			q->nsigs++;
			q->curtup++;
		}

		q->nsigpages++;
		q->curpage++;
	}
	
	freeBits(qsig);
	// Remove it before submitting this function
	// printf("Matched Pages:"); showBits(q->pages); putchar('\n');
}
