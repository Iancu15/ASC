#include <iostream>
#include <stdlib.h>
#include <cuda_runtime_api.h>
#include <cuda.h>
#include "helper.h"

__global__ void calcTrigAngles(const CityPos *posArray, CityTrigFunc *trigFuncArray) {
    // compute global element index
  	unsigned int globalID = threadIdx.x + blockDim.x * blockIdx.x;

    CityPos pos = posArray[globalID];
    CityTrigFunc trigFunc;

    // compute sin and cos of phi and of theta for the city with id globalID
    double phi = (90.f - pos.lat) * DEGREE_TO_RADIANS;
    double theta = pos.lon * DEGREE_TO_RADIANS;
    trigFunc.sinPhi = sin(phi);
    trigFunc.cosPhi = cos(phi);
    trigFunc.sinTheta = sin(theta);
    trigFunc.cosTheta = cos(theta);
    trigFuncArray[globalID] = trigFunc;
}

__global__ void calcAccesiblePopulations(const CityTrigFunc *trigFuncArray, const int *popArrayIn,
                                        int *popArrayOut, const size_t numberOfCities, double kmRange) {
  	// compute global element index
  	unsigned int globalID = threadIdx.x + blockDim.x * blockIdx.x;

  	// avoid out of bounds exceptions
  	if (globalID < numberOfCities) {
        // take sin and cos for phi and theta for the city assigned to the current thread
        CityTrigFunc trigFunc1 = trigFuncArray[globalID];
        double sinPhi1 = trigFunc1.sinPhi;
        double cosPhi1 = trigFunc1.cosPhi;
        double sinTheta1 = trigFunc1.sinTheta;
        double cosTheta1 = trigFunc1.cosTheta;

        // in totalPop I would store the accessible population of the city
        // assigned to the current thread
        int totalPop = 0;
        for (size_t cityID = 0; cityID < numberOfCities; cityID++) {
            // take sin and cos for phi and theta for the current city in the loop
            CityTrigFunc trigFunc2 = trigFuncArray[cityID];
            double sinPhi2 = trigFunc2.sinPhi;
            double cosPhi2 = trigFunc2.cosPhi;
            double sinTheta2 = trigFunc2.sinTheta;
            double cosTheta2 = trigFunc2.cosTheta;

            // calculate cs
            double cosTheta1MinusTheta2 = cosTheta1 * cosTheta2 + sinTheta1 * sinTheta2;
            double cs = sinPhi1 * sinPhi2 * cosTheta1MinusTheta2 + cosPhi1 * cosPhi2;
            if (cs > 1) {
                cs = 1;
            } else if (cs < -1) {
                cs = -1;
            }

            double negate = double(cs < 0);
            if (cs < 0) {
                cs = -cs;
            }

            // calculate acos(cs) using Nvidia implementation
            double aCosOfCs = -0.0187293;
            aCosOfCs = aCosOfCs * cs;
            aCosOfCs = aCosOfCs + 0.0742610;
            aCosOfCs = aCosOfCs * cs;
            aCosOfCs = aCosOfCs - 0.2121144;
            aCosOfCs = aCosOfCs * cs;
            aCosOfCs = aCosOfCs + 1.5707288;
            aCosOfCs = aCosOfCs * sqrt(1.0-cs);
            aCosOfCs = aCosOfCs - 2 * negate * aCosOfCs;
            aCosOfCs = negate * 3.14159265358979 + aCosOfCs;

            // calculate distance
            double dist = 6371.f * aCosOfCs;
            if (dist <= kmRange) {
                totalPop += popArrayIn[cityID];
            }
        }

        popArrayOut[globalID] = totalPop;
  	}
}

int main(int argc, char** argv) {
    DIE( argc == 1,
         "./accpop <kmrange1> <file1in> <file1out> ...");
    DIE( (argc - 1) % 3 != 0,
         "./accpop <kmrange1> <file1in> <file1out> ...");

    // declare host arrays
    CityPos *hostPosArray;
    int *hostPopArray;

    // declare device arrays
    CityPos *devicePosArray;
    CityTrigFunc *deviceTrigFuncArray;
    int *devicePopArrayIn;
    int *devicePopArrayOut;

    // constants
    const size_t blockSize = 256;

    for(int argcID = 1; argcID < argc; argcID += 3) {
        double kmRange = atof(argv[argcID]);
        size_t numberOfCities = getNumberOfLines(argv[argcID + 1]);

        // allocate host arrays for the individual file
        hostPosArray = (CityPos *) malloc(numberOfCities * sizeof(CityPos));
        hostPopArray = (int *) malloc(numberOfCities * sizeof(int));

        // allocate device arrays for the individual file
        cudaMalloc((void **) &devicePosArray, numberOfCities * sizeof(CityPos));
        cudaMalloc((void **) &devicePopArrayIn, numberOfCities * sizeof(int));
        cudaMalloc((void **) &devicePopArrayOut, numberOfCities * sizeof(int));
        cudaMalloc((void **) &deviceTrigFuncArray, numberOfCities * sizeof(CityTrigFunc));

        // populating the arrays with data
        readFile(argv[argcID + 1], hostPosArray, hostPopArray);

        // copy host arrays to device
        cudaMemcpy(devicePosArray, hostPosArray, numberOfCities * sizeof(CityPos), cudaMemcpyHostToDevice);
        cudaMemcpy(devicePopArrayIn, hostPopArray, numberOfCities * sizeof(int), cudaMemcpyHostToDevice);

        // calling kernel functions
        size_t numberOfBlocks = (numberOfCities / blockSize) + 1;
        calcTrigAngles<<<numberOfBlocks, blockSize>>>(devicePosArray, deviceTrigFuncArray);
        calcAccesiblePopulations<<<numberOfBlocks, blockSize>>>(deviceTrigFuncArray, devicePopArrayIn, devicePopArrayOut, numberOfCities, kmRange);

        // copy result back to host
        cudaMemcpy(hostPopArray, devicePopArrayOut, numberOfCities * sizeof(int), cudaMemcpyDeviceToHost);

        // writing output
        writeFile(argv[argcID + 2], hostPopArray, numberOfCities);

        // free host arrays
        free(hostPosArray);
        free(hostPopArray);

        // free device arrays
        cudaFree(devicePosArray);
        cudaFree(devicePopArrayIn); 
        cudaFree(devicePopArrayOut);
        cudaFree(deviceTrigFuncArray);
    }
}
