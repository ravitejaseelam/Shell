#!/bin/bash
echo "Enter number of inputs"

n=$1

echo "Enter Numbers in array:"

for (( i = 0; i < $n; i++ ))

	do
		read nos[$i]
	done

echo "Numbers in an array are:"

	for (( i = 0; i < $n; i++ ))
		do
			echo ${nos[$i]}
		done

	for (( i = 0; i < $n ; i++ ))
	 do
		for (( j = $i; j < $n; j++ ))
			do
				if [ ${nos[$i]} -gt ${nos[$j]}  ]; then
					t=${nos[$i]}
					nos[$i]=${nos[$j]}
					nos[$j]=$t
				fi
		done
	 done

echo -e "\tSorted Numbers "

	for (( i=0; i < $n; i++ ))
		do
			echo ${nos[$i]}
		done
