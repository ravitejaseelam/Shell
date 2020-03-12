

filename=$1

if [ "$#" -lt "2" ];then
	echo "$0:Requires atleast two arguments filename and word to find example format (bash wordFinder file.txt word1 word2 ....)"
	exit 0
fi

if test ! -f "$filename" ;then
    echo "$filename does not exist"
    exit 0
fi

#[ -s $filename ]&&echo "file is not empty"|| echo "file is empty"

if test ! -s $filename ;then
  echo "$filename is empty" 
  exit 1
fi

for i in "${@:2}"
do
echo -e "\n$i Search result:\n"
echo "No of instances found"
grep -io $i $filename | wc -l
echo "No of lines found"
grep -in "$i" $filename | grep -Eo '^[^:]+'|wc -l
echo "line numbers are :"
if grep -q "$i" $filename;then 
	grep -in "$i" $filename | grep -Eo '^[^:]+'
else
       echo "none"
fi
done

