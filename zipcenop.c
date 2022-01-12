#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>

#define E 0
#define R 1

static int cenFlag[] = { 80, 75, 1, 2 };

// Java里的 byte 是 signed char
// 所以不用 unsigned char
static char cenEncyptedFlag[] = { 9, 8 };
static char cenNotEncyptedFlag[] = { 0, 8 };


unsigned long get_file_size(const char *path) {
	struct stat statbuff;
	
	if (stat(path, &statbuff) < 0) {
		return -1;
    }
	
	return statbuff.st_size;
}

int main(int argc, char *argv[])
{
	const char *my = argv[0];

	if (argc != 3) {
		fprintf(stderr, "usage: %s <e|r> <.zip|.jar|.apk>\n"
						"\n"
						"  e: do a fake encryption\n"
						"  r: recover a file\n"
						"\n",
				my);

		return 1;
	}

	const char *mode = argv[1];
	const char *file = argv[2];

	int fd = -1;
	char *buffer = NULL;
	unsigned long size = -1;
	int operator = -1;

	fd = open(file, O_RDWR);
	if (fd < 0)
	{
		fprintf(stderr, "%s: open: %s\n", my, strerror(errno));
		return 1;
	}

	size = get_file_size(file);
	if (size == -1)
	{
		fprintf(stderr, "%s: stat: %s\n", my, strerror(errno));
		return 1;
	}

	buffer = (char*) mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
	if (buffer == MAP_FAILED)
	{
		fprintf(stderr, "%s: mmap: %s\n", my, strerror(errno));
		close(fd);
		return 1;
	}

	if (strcmp("e", mode) == 0) {
		operator = E;
	} else if (strcmp("r", mode) == 0) {
		operator = R;
	}

	int count = 0;
	
	for (int position = 0; position < size; ++position) {
		for (int offset = 0; offset < 4; ++offset) {
			if (buffer[position + offset] != cenFlag[offset])
				break;

			if (offset == 3) {
				if (operator == R) {
					buffer[position + 8] = cenNotEncyptedFlag[0];
				} else if (operator == E) {
					buffer[position + 8] = cenEncyptedFlag[0];
				}

				offset += 10;
				++count;
			}
		}
	}


	munmap(buffer, size);
	close(fd);
	return 0;
}

