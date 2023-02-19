#ifndef ACCPOP_HELPER_H
#define ACCPOP_HELPER_H
#include <stdio.h>

#define DEGREE_TO_RADIANS		0.01745329252f

typedef struct {
    double lat;
    double lon;
} CityPos;

typedef struct {
    double sinPhi;
    double cosPhi;
    double sinTheta;
    double cosTheta;
} CityTrigFunc;

int getNumberOfLines(const char* fileIn);

void readFile(const char* fileIn, CityPos *posArray, int *popArray);

void writeFile(const char* fileOut, int *popArray, int arraySize);

#define DIE(assertion, call_description)                    \
do {                                                        \
    if (assertion) {                                        \
            fprintf(stderr, "(%d): ",                       \
                            __LINE__);                      \
            perror(call_description);                       \
            exit(EXIT_FAILURE);                             \
    }                                                       \
} while(0);

#endif //ACCPOP_HELPER_H
