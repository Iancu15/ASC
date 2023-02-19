#!/bin/bash

for i in {1..100}
do
    ./run_cluster_checker.sh >> cluster_out
    sleep 1
done