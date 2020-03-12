#!/bin/bash

sort()
{
size=$1
array=$2
        for (( i = 0; i < $size ; i++ ))
        do
                for (( j = $i; j < $size; j++ ))
                do
                        if [ ${array[$i]} -gt ${array[$j]}  ]; then
			t=${array[$i]}
                        array[$i]=${array[$j]}
                        array[$j]=$t
                        fi
                done
        done
}



if test $# -lt 1;
	then
	echo "You should provide size of array in arguments example format(bash $0 10) "
	exit 0
		elif test $# -gt 1;
		then
		echo "More than one argument is passed only size of array is need example format(bash $0 10)"
		exit 1
fi

echo "Given length of array is $1"

	size=$1
	if [[ -n ${size//[0-9]/} ]]; then
	echo "Size should be given only in numbers"
	 exit 2
	fi

	echo "Enter $1 Numbers in array:(With','Seperation)"

	        read List

	length=0
	comma=0
	comp=$((size-1))

	for ((i=0;i<${#List};i++))
	do
		if [ ${List:$i:1} != "," ];then
			length=$((length+1))
		else
			comma=$((comma+1))
		fi
	done
        
	if test $length -eq $size;then
		echo ""
		if test $comma -lt $comp;then
			echo "Plz provide input with ',' seperation" 
			exit 3
		fi

	fi

	array=( ${List//,/ } )	
	
	if test ${#array[@]} -ne $1;
	then
		echo "Size dosent match!"
		exit 3
	fi

	for ((i=0;i<$size;i++))
	do
	if [[ -n ${array[$i]//[0-9]/} ]]; then
  	  echo "Contains letters!"
	  exit 4
	fi
	done

echo "Numbers in an array are:" 	
delim="{"
	for item in "${array[@]}"; do
	  printf "%s" "$delim$item"
	  delim=","
	done
delim="}"  
printf "%s""$delim"

sort $size $array

echo -e "\n$0 has Sorted Numbers"

delim="{"
for item in "${array[@]}"; do
  printf "%s" "$delim$item"
  delim=","
done
delim="}"
printf "%s""$delim"
echo -e "\n"
