/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include "utils.h"

/*
 * Add your unoptimized implementation here
 */
double* my_solver(int N, double *A, double *B) {
	double *C = calloc(N * N, sizeof(double));
	int i, j, k;

	// calculez C = B * A
	for (i = 0; i < N; i++) {
		for (k = 0; k < N; k++) {
			for (j = k; j < N; j++) {
				C[i * N + j] += B[i * N + k] * A[k * N + j];
			}
		}
	}

	// notatie A**T este A transpusa
	// calculez D = C * A**T = B * A * A**T
	// [j][k] in loc de [k][j] pentru transpusa
	double *D = calloc(N * N, sizeof(double));
	for (i = 0; i < N; i++) {
		for (j = 0; j < N; j++) {
			for (k = j; k < N; k++) {
				D[i * N + j] += C[i * N + k] * A[j * N + k];
			}
		}
	}

	// golesc C pentru a-l refolosi
	for (i = 0; i < N * N; i++) {
		C[i] = 0;
	}

	// calculez C = B**T * B
	// [k][i] in loc de [i][k] pentru transpusa
	for (i = 0; i < N; i++) {
		for (j = 0; j < N; j++) {
			for (k = 0; k < N; k++) {
				C[i * N + j] += B[k * N + i] * B[k * N + j];
			}
		}
	}

	// calculez D = D + C = B * A * A**T + B**T * B
	for (i = 0; i < N * N; i++) {
		D[i] += C[i];
	}

	free(C);

	return D;
}
