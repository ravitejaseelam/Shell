#!/bin/bash

ip_check()
{
IP=$1
OCT=( ${IP//./ } )
REGEX_IP='^[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}$'

if [[ ${IP} =~ ${REGEX_IP} ]]
then
    if [[ ${OCT[0]} -gt 255 || ${OCT[1]} -gt 255 || ${OCT[2]} -gt 255 || ${OCT[3]} -gt 255 ]]
        then
                echo "IP size mismatch each part in ip must be in the range of (0-255)"
                exit 2
        else
                echo "$1 is valid ip address"
    fi

else
        echo "IP address format mistake you should have 4 numbers ranging from (0-255) with'.'seperating it exapmle(192.2.1.0) "
        exit 3
fi

}

if test $# -lt 1;
        then
	echo "You should provide Ip Address in arguments example format(bash $0 192.1.5.0) "
	exit 0

elif test $# -gt 1;
	then
	echo "More than one argument is passed only ip address is needed example format(bash $0 192.1.5.0)"
        exit 1

fi

IP=$1

ip_check $IP
