#include <math.h>
#include <fstream>

#include "helper.h"

using namespace std;

// count the number of lines in the input file
// the number of lines would be equal to the number of cities
int getNumberOfLines(const char* fileIn) {
    string geon;
    double lat;
    double lon;
    int pop;

    ifstream ifs(fileIn);

    int numberOfLines = 0;
    while (ifs >> geon >> lat >> lon >> pop) {
        numberOfLines++;
    }

    ifs.close();

    return numberOfLines;
}

// reads lat, lon and pop from each city and store them in arrays
void readFile(const char* fileIn, CityPos *posArray, int *popArray) {
    string geon;
    double lat;
    double lon;
    int pop;
    
    ifstream ifs(fileIn);

    int lineID = 0;
    while (ifs >> geon >> lat >> lon >> pop) {
        CityPos pos;
        pos.lat = lat;
        pos.lon = lon;
        posArray[lineID] = pos;
        popArray[lineID] = pop;
        lineID++;
    }

    ifs.close();
}

// writes the population array to the output file
void writeFile(const char* fileOut, int *popArray, int arraySize) {
    ofstream ofs(fileOut);

    for (int cityID = 0; cityID < arraySize; cityID++) {
        ofs << popArray[cityID] << endl;
    }

    ofs.close();
}
