/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include "utils.h"
#define LOOP_SIZE 0

/*
 * Add your optimized implementation here
 */
double* my_solver(int N, double *A, double *B) {
	register int size = N;
	register int size_squared = N * N;
	double *C = calloc(size_squared, sizeof(double));
	register int i;
	register int j;
	register int k;

	// calculez C = B * A
	register int C_line = 0;
	for (i = 0; i < size; i++) {
		register int A_line = 0;
		for (k = 0; k < size; k++) {
			register double constant = B[i * size + k];
			for (j = k; j < size; j++) {
				C[C_line + j] += constant * A[A_line + j];
			}

			A_line += size;
		}

		C_line += size;
	}

	// calculez D = C * A**T = B * A * A**T
	double *D = calloc(size_squared, sizeof(double));
	C_line = 0;
	for (i = 0; i < size; i++) {
		register int A_line = 0;
		for (j = 0; j < size; j++) {
			register double sum = 0;
			for (k = j; k < size; k++) {
				sum += C[C_line + k] * A[A_line + k];
			}

			D[i * size + j] = sum;
			A_line += size;
		}

		C_line += size;
	}

	// golesc C pentru a-l refolosi
	for (i = 0; i < size_squared; i++) {
		C[i] = 0;
	}

	// calculez C = B**T * B
	register int B_line = 0;
	for (k = 0; k < size; k++) {
		register int C_line = 0;
		for (i = 0; i < size; i++) {
			register double constant = B[k * size + i];
			for (j = 0; j < size; j++) {
				C[C_line + j] += constant * B[B_line + j];
			}

			C_line += size;
		}

		B_line += size;
	}

	// calculez D = D + C = B * A * A**T + B**T * B
	for (i = 0; i < size_squared; i++) {
		D[i] += C[i];
	}

	free(C);

	return D;
}
