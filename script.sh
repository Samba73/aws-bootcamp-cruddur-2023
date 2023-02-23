#!/bin/bash
while $1
do
    echo 'Press [CTRL + C] to break'
    sleep 5
    echo "The second and third arguments are  $2 & $3"
done