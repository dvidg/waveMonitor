#!/bin/bash

cp log.txt "logs/log$(date +"%m-%d-%y").txt"
> log.txt
cp nohup.out "logs/nohup$(date +"%m-%d-%y").out"
> nohup.out
