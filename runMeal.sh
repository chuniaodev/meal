#!/bin/bash

if [ "start" == "$1" ]
then
    cd /home/chuniao/workspace/git/meal
    ./chat/mealdemo.py &

elif [ "stop" == "$1" ]
then
    kill -9  $(ps -ef | grep mealdemo.py | cut -d " " -f 4 | head -n1)
else
    echo "args error"
fi

