// bufpool.c ... buffer pool implementation

// TODO: to complete this you will need to:
// - manipulate usedList[] in the appropriate places
// - implement the getNextSlot() function

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include "bufpool.h"

#define PID_LEN 8

// one buffer
struct buffer {
	char  id[PID_LEN];
	int   pin;
	int   dirty;
	char  *data;
};

// collection of buffers + stats
struct bufPool {
	int   nbufs;         // how many buffers
	char  strategy;      // LRU, MRU, Queue
	int   nrequests;     // stats counters
	int   nreleases;
	int   nreads;
	int   nwrites;
	int   *freeList;     // list of completely unused bufs
	int   nfree;
	int   *usedList;     // implements replacement strategy
	int   nused;
	struct buffer *bufs;
};

static int clock = 0;

// helper functions

char *pageInBuf(BufPool pool, int slot)
{
	char *pname;
	pname = pool->bufs[slot].id;
	if (pname[0] == '\0')
		return "_";
	else
		return pname;
}

int pageInPool(BufPool pool, char rel, int page)
{
	int i, found = 0;
	char pname[PID_LEN];

	sprintf(pname, "%c%d", rel,page);
	for (i = 0; i < pool->nbufs; i++) {
		if (strcmp(pname, pool->bufs[i].id) == 0) {
			found = 1;
			break;
		}
	}
	return (!found) ? -1 : i;
}

int removeFirstFree(BufPool pool)
{
	int v, i;
	v = pool->freeList[0];
	for (i = 0; i < pool->nfree-1; i++)
		pool->freeList[i] = pool->freeList[i+1];
	pool->nfree--;
	return v;
}

// select first unpinned slot, favouring non-dirty
int grabNextSlot(BufPool pool)
{
	// TODO: complete this to utilise replacement strategy
	// TODO: manipulate usedList[] appropriately
}


// interface functions

BufPool initBufPool(int nbufs, char strategy)
{
	BufPool newPool;
	struct buffer *bufs;

	newPool = malloc(sizeof(struct bufPool));
	assert(newPool != NULL);
	newPool->nbufs = nbufs;
	newPool->strategy = strategy;
	newPool->nrequests = 0;
	newPool->nreleases = 0;
	newPool->nreads = 0;
	newPool->nwrites = 0;
	newPool->nfree = nbufs;
	newPool->nused = 0;
	newPool->freeList = malloc(nbufs * sizeof(int));
	assert(newPool->freeList != NULL);
	newPool->usedList = malloc(nbufs * sizeof(int));
	assert(newPool->usedList != NULL);
	newPool->bufs = malloc(nbufs * sizeof(struct buffer));
	assert(newPool->bufs != NULL);

	int i;
	for (i = 0; i < nbufs; i++) {
		newPool->bufs[i].id[0] = '\0';
		newPool->bufs[i].pin = 0;
		newPool->bufs[i].dirty = 0;
		newPool->freeList[i] = i;
		newPool->usedList[i] = -1;
	}
	return newPool;
}

int request_page(BufPool pool, char rel, int page)
{
	int slot;
	printf("Request %c%d\n", rel, page);
	pool->nrequests++;
	slot = pageInPool(pool,rel,page);
	if (slot < 0) {
			if (pool->nfree > 0) {
				slot = removeFirstFree(pool);
			}
			else {
				slot = grabNextSlot(pool);
			}
			assert(slot >= 0);
			pool->nreads++;
			sprintf(pool->bufs[slot].id,"%c%d",rel,page);
			pool->bufs[slot].pin = 0;
			pool->bufs[slot].dirty = 0;
	}
	// have a slot
	pool->bufs[slot].pin++;
	showPoolState(pool);
	return slot;
}

void release_page(BufPool pool, char rel, int page)
{
	printf("Release %c%d\n", rel, page);
	pool->nreleases++;
	char id[10];
	sprintf(id,"%c%d",rel,page);
	int i;
	for (i = 0; i < pool->nbufs; i++) {
		if (strcmp(id,pool->bufs[i].id) == 0)
			break;
	}
	if (i < pool->nbufs) {
		pool->bufs[i].pin--;
	}
//	showPoolState(pool);
}

void showPoolUsage(BufPool pool)
{
	assert(pool != NULL);
	printf("#requests: %d\n",pool->nrequests);
	printf("#releases: %d\n",pool->nreleases);
	printf("#reads   : %d\n",pool->nreads);
	printf("#writes  : %d\n",pool->nwrites);
}

void showPoolState(BufPool pool)
{
	int i, j; char *p; struct buffer b;

	printf("%4s %6s %6s %6s\n","Slot","Page","Pin","Dirty");
	for (i = 0; i < pool->nbufs; i++) {
		b = pool->bufs[i];
		p = pageInBuf(pool,i);
		printf("[%02d] %6s %6d %6d\n", i, p, b.pin, b.dirty);
	}
	printf("FreeList:");
	for (i = 0; i < pool->nfree; i++) {
		j = pool->freeList[i];
		printf(" [%02d]%s", j, pageInBuf(pool,j));
	}
	printf("\n");
	printf("UsedList:");
	for (i = 0; i < pool->nused; i++) {
		j = pool->usedList[i];
		printf(" [%02d]%s", j, pageInBuf(pool,j));
	}
	printf("\n");
}
