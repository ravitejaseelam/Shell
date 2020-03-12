#!/bin/sh

if [ "$#" -lt "2" ];then
        echo "$0:Argument shortage encountered Requires two arguments source filename and destination filename (bash $0 source.json out.json)"
        exit 0
fi

if [ "$#" -gt "2" ];then
        echo "$0:Extra arguments encountered Requires only two arguments source filename and destination filename (bash $0 source.json out.json)"
        exit 0
fi

filename=$1
outputfilename=$2
if test ! -f "$filename" ;then
    echo "$filename does not exist"
    exit 0
fi

if test ! -s $filename ;then
  echo "$filename is empty" 
  exit 1
fi




echo "Do you want to the duplicates to be deleted (y/n)"
read ans

if test $ans == y ;then 
	cat  $filename | jq -s -c 'unique_by(.Id)|sort_by(.priority, .Id, .name) | .[] | select(.healthchk_enabled)'> $outputfilename
	echo "Process Done Plz find the output in 'output.json' file"
elif test $ans == n ;then
	cat  $filename | jq -s -c 'sort_by(.priority, .Id, .name) | .[] | select(.healthchk_enabled)'> $outputfilename
	echo "Process Done Plz find the output in $outputfilename file"
else
	echo "Wrong Input it should be either y or n be carefull with case"
fi

