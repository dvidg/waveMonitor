#!/bin/bash
if [ -s log.txt ]
then
	cp log.txt "pastLogs/log$(date +"%m-%d-%y").txt"
	> log.txt
fi

if [ -s nohup.out ]
then
	cp nohup.out "pastLogs/nohup$(date +"%m-%d-%y").out"
	> nohup.out
fi
