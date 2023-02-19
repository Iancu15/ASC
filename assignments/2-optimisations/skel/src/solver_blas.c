/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include "utils.h"
#include <cblas.h>
/* 
 * Add your BLAS implementation here
 */
double* my_solver(int N, double *A, double *B) {
	double *C = malloc(N * N * sizeof(double));

	// copiez B in C
	cblas_dcopy(
		N * N,
		B,
		1,
		C,
		1
	);

	// calculez C = C * A = B * A
	cblas_dtrmm(
		CblasRowMajor,
		CblasRight,
		CblasUpper,
		CblasNoTrans,
		CblasNonUnit,
		N,
		N,
		1.0,
		A,
		N,
		C,
		N
	);

	// calculez C = C * A**T = B * A * A**T
	cblas_dtrmm(
		CblasRowMajor,
		CblasRight,
		CblasUpper,
		CblasTrans,
		CblasNonUnit,
		N,
		N,
		1.0,
		A,
		N,
		C,
		N
	);

	// calculez C = B**T * B + C = B**T * B + B * A * A**T
	cblas_dgemm(
		CblasRowMajor,
		CblasTrans,
		CblasNoTrans,
		N,
		N,
		N,
		1.0,
		B,
		N,
		B,
		N,
		1.0,
		C,
		N
	);

	return C;
}
