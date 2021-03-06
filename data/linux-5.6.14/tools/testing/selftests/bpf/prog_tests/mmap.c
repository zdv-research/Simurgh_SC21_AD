// SPDX-License-Identifier: GPL-2.0
#include <test_progs.h>
#include <sys/mman.h>
#include "test_mmap.skel.h"

struct map_data {
	__u64 val[512 * 4];
};

static size_t roundup_page(size_t sz)
{
	long page_size = sysconf(_SC_PAGE_SIZE);
	return (sz + page_size - 1) / page_size * page_size;
}

void test_mmap(void)
{
	const size_t bss_sz = roundup_page(sizeof(struct test_mmap__bss));
	const size_t map_sz = roundup_page(sizeof(struct map_data));
	const int zero = 0, one = 1, two = 2, far = 1500;
	const long page_size = sysconf(_SC_PAGE_SIZE);
	int err, duration = 0, i, data_map_fd;
	struct bpf_map *data_map, *bss_map;
	void *bss_mmaped = NULL, *map_mmaped = NULL, *tmp1, *tmp2;
	struct test_mmap__bss *bss_data;
	struct map_data *map_data;
	struct test_mmap *skel;
	__u64 val = 0;


	skel = test_mmap__open_and_load();
	if (CHECK(!skel, "skel_open_and_load", "skeleton open/load failed\n"))
		return;

	bss_map = skel->maps.bss;
	data_map = skel->maps.data_map;
	data_map_fd = bpf_map__fd(data_map);

	bss_mmaped = mmap(NULL, bss_sz, PROT_READ | PROT_WRITE, MAP_SHARED,
			  bpf_map__fd(bss_map), 0);
	if (CHECK(bss_mmaped == MAP_FAILED, "bss_mmap",
		  ".bss mmap failed: %d\n", errno)) {
		bss_mmaped = NULL;
		goto cleanup;
	}
	/* map as R/W first */
	map_mmaped = mmap(NULL, map_sz, PROT_READ | PROT_WRITE, MAP_SHARED,
			  data_map_fd, 0);
	if (CHECK(map_mmaped == MAP_FAILED, "data_mmap",
		  "data_map mmap failed: %d\n", errno)) {
		map_mmaped = NULL;
		goto cleanup;
	}

	bss_data = bss_mmaped;
	map_data = map_mmaped;

	CHECK_FAIL(bss_data->in_val);
	CHECK_FAIL(bss_data->out_val);
	CHECK_FAIL(skel->bss->in_val);
	CHECK_FAIL(skel->bss->out_val);
	CHECK_FAIL(map_data->val[0]);
	CHECK_FAIL(map_data->val[1]);
	CHECK_FAIL(map_data->val[2]);
	CHECK_FAIL(map_data->val[far]);

	err = test_mmap__attach(skel);
	if (CHECK(err, "attach_raw_tp", "err %d\n", err))
		goto cleanup;

	bss_data->in_val = 123;
	val = 111;
	CHECK_FAIL(bpf_map_update_elem(data_map_fd, &zero, &val, 0));

	usleep(1);

	CHECK_FAIL(bss_data->in_val != 123);
	CHECK_FAIL(bss_data->out_val != 123);
	CHECK_FAIL(skel->bss->in_val != 123);
	CHECK_FAIL(skel->bss->out_val != 123);
	CHECK_FAIL(map_data->val[0] != 111);
	CHECK_FAIL(map_data->val[1] != 222);
	CHECK_FAIL(map_data->val[2] != 123);
	CHECK_FAIL(map_data->val[far] != 3 * 123);

	CHECK_FAIL(bpf_map_lookup_elem(data_map_fd, &zero, &val));
	CHECK_FAIL(val != 111);
	CHECK_FAIL(bpf_map_lookup_elem(data_map_fd, &one, &val));
	CHECK_FAIL(val != 222);
	CHECK_FAIL(bpf_map_lookup_elem(data_map_fd, &two, &val));
	CHECK_FAIL(val != 123);
	CHECK_FAIL(bpf_map_lookup_elem(data_map_fd, &far, &val));
	CHECK_FAIL(val != 3 * 123);

	/* data_map freeze should fail due to R/W mmap() */
	err = bpf_map_freeze(data_map_fd);
	if (CHECK(!err || errno != EBUSY, "no_freeze",
		  "data_map freeze succeeded: err=%d, errno=%d\n", err, errno))
		goto cleanup;

	/* unmap R/W mapping */
	err = munmap(map_mmaped, map_sz);
	map_mmaped = NULL;
	if (CHECK(err, "data_map_munmap", "data_map munmap failed: %d\n", errno))
		goto cleanup;

	/* re-map as R/O now */
	map_mmaped = mmap(NULL, map_sz, PROT_READ, MAP_SHARED, data_map_fd, 0);
	if (CHECK(map_mmaped == MAP_FAILED, "data_mmap",
		  "data_map R/O mmap failed: %d\n", errno)) {
		map_mmaped = NULL;
		goto cleanup;
	}
	map_data = map_mmaped;

	/* map/unmap in a loop to test ref counting */
	for (i = 0; i < 10; i++) {
		int flags = i % 2 ? PROT_READ : PROT_WRITE;
		void *p;

		p = mmap(NULL, map_sz, flags, MAP_SHARED, data_map_fd, 0);
		if (CHECK_FAIL(p == MAP_FAILED))
			goto cleanup;
		err = munmap(p, map_sz);
		if (CHECK_FAIL(err))
			goto cleanup;
	}

	/* data_map freeze should now succeed due to no R/W mapping */
	err = bpf_map_freeze(data_map_fd);
	if (CHECK(err, "freeze", "data_map freeze failed: err=%d, errno=%d\n",
		  err, errno))
		goto cleanup;

	/* mapping as R/W now should fail */
	tmp1 = mmap(NULL, map_sz, PROT_READ | PROT_WRITE, MAP_SHARED,
		    data_map_fd, 0);
	if (CHECK(tmp1 != MAP_FAILED, "data_mmap", "mmap succeeded\n")) {
		munmap(tmp1, map_sz);
		goto cleanup;
	}

	bss_data->in_val = 321;
	usleep(1);
	CHECK_FAIL(bss_data->in_val != 321);
	CHECK_FAIL(bss_data->out_val != 321);
	CHECK_FAIL(skel->bss->in_val != 321);
	CHECK_FAIL(skel->bss->out_val != 321);
	CHECK_FAIL(map_data->val[0] != 111);
	CHECK_FAIL(map_data->val[1] != 222);
	CHECK_FAIL(map_data->val[2] != 321);
	CHECK_FAIL(map_data->val[far] != 3 * 321);

	/* check some more advanced mmap() manipulations */

	/* map all but last page: pages 1-3 mapped */
	tmp1 = mmap(NULL, 3 * page_size, PROT_READ, MAP_SHARED,
			  data_map_fd, 0);
	if (CHECK(tmp1 == MAP_FAILED, "adv_mmap1", "errno %d\n", errno))
		goto cleanup;

	/* unmap second page: pages 1, 3 mapped */
	err = munmap(tmp1 + page_size, page_size);
	if (CHECK(err, "adv_mmap2", "errno %d\n", errno)) {
		munmap(tmp1, map_sz);
		goto cleanup;
	}

	/* map page 2 back */
	tmp2 = mmap(tmp1 + page_size, page_size, PROT_READ,
		    MAP_SHARED | MAP_FIXED, data_map_fd, 0);
	if (CHECK(tmp2 == MAP_FAILED, "adv_mmap3", "errno %d\n", errno)) {
		munmap(tmp1, page_size);
		munmap(tmp1 + 2*page_size, page_size);
		goto cleanup;
	}
	CHECK(tmp1 + page_size != tmp2, "adv_mmap4",
	      "tmp1: %p, tmp2: %p\n", tmp1, tmp2);

	/* re-map all 4 pages */
	tmp2 = mmap(tmp1, 4 * page_size, PROT_READ, MAP_SHARED | MAP_FIXED,
		    data_map_fd, 0);
	if (CHECK(tmp2 == MAP_FAILED, "adv_mmap5", "errno %d\n", errno)) {
		munmap(tmp1, 3 * page_size); /* unmap page 1 */
		goto cleanup;
	}
	CHECK(tmp1 != tmp2, "adv_mmap6", "tmp1: %p, tmp2: %p\n", tmp1, tmp2);

	map_data = tmp2;
	CHECK_FAIL(bss_data->in_val != 321);
	CHECK_FAIL(bss_data->out_val != 321);
	CHECK_FAIL(skel->bss->in_val != 321);
	CHECK_FAIL(skel->bss->out_val != 321);
	CHECK_FAIL(map_data->val[0] != 111);
	CHECK_FAIL(map_data->val[1] != 222);
	CHECK_FAIL(map_data->val[2] != 321);
	CHECK_FAIL(map_data->val[far] != 3 * 321);

	munmap(tmp2, 4 * page_size);

	/* map all 4 pages, but with pg_off=1 page, should fail */
	tmp1 = mmap(NULL, 4 * page_size, PROT_READ, MAP_SHARED | MAP_FIXED,
		    data_map_fd, page_size /* initial page shift */);
	if (CHECK(tmp1 != MAP_FAILED, "adv_mmap7", "unexpected success")) {
		munmap(tmp1, 4 * page_size);
		goto cleanup;
	}

cleanup:
	if (bss_mmaped)
		CHECK_FAIL(munmap(bss_mmaped, bss_sz));
	if (map_mmaped)
		CHECK_FAIL(munmap(map_mmaped, map_sz));
	test_mmap__destroy(skel);
}
