#!/bin/bash
if [ -s log.txt ]
then
	cp log.txt "logs/log$(date +"%m-%d-%y").txt"
	> log.txt
else
	echo "logs empty"
fi

if [ -s nohup.out ]
then
	cp nohup.out "logs/nohup$(date +"%m-%d-%y").out"
	> nohup.out
else
	echo "nohup empty"
fi
