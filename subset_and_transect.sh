#!/bin/bash

sh subset.sh V V
sh subset.sh W W

python3 WRF_transect_UVW.py
