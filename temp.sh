#!/bin/bash

for i in $(seq -f "%02g" 05 14); do
    for j in $(seq -f "%02g" 01 10); do
        sed -i '/20'${i}${j}'/d' ./subset_TRMM_3B42_V7_20190621_002105.txt
    done
done

