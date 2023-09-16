#!/bin/bash


rm command1

touch command1

# rm *.out
python submit.py 1 1001 >> command1
sh command1
sleep 10