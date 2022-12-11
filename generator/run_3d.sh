# indicate that this script is bash
#!/bin/bash

# script takes to user arguments, the first is the start frame and the second is the stop frame
# if no arguments are given, the script will run from frame 0 to frame 19999
if [ -z "$1" ]
then
    start=0
else
    start=$1
fi

if [ -z "$2" ]
then
    stop=19999
else
    stop=$2
fi

blender -b -P "main_3d.py" -- $start $stop
