#!/bin/sh

#valgrind --tool=memcheck --leak-check=full ./tema2_opt_m /export/asc/tema2/input_valgrind > opt_m.memory 2>&1
#valgrind --tool=memcheck --leak-check=full ./tema2_neopt /export/asc/tema2/input_valgrind > neopt.memory 2>&1
#valgrind --tool=memcheck --leak-check=full ./tema2_blas /export/asc/tema2/input_valgrind > blas.memory 2>&1
#valgrind --tool=cachegrind --branch-sim=yes ./tema2_blas /export/asc/tema2/input_valgrind > blas.cache 2>&1
#valgrind --tool=cachegrind --branch-sim=yes ./tema2_neopt /export/asc/tema2/input_valgrind > neopt.cache 2>&1
valgrind --tool=cachegrind --branch-sim=yes ./tema2_opt_m /export/asc/tema2/input_valgrind > opt_m.cache 2>&1