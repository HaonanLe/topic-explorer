#!/bin/bash
EXIT=0

echo "Pinging server in PID"
echo $1
kill -0 $1
[ $(curl -i http://localhost:8000/docs.json 2>/dev/null | head -n 1 | cut -d$' ' -f2) == "200" ]
EXIT=$(($EXIT+$?))
[ $(curl -i http://localhost:8000/20/topics.json 2>/dev/null | head -n 1 | cut -d$' ' -f2) == "200" ]
EXIT=$(($EXIT+$?))
[ $(curl -i http://localhost:8000/ 2>/dev/null | head -n 1 | cut -d$' ' -f2) == "200" ]
EXIT=$(($EXIT+$?))
[ $(curl -i http://localhost:8000/20/ 2>/dev/null | head -n 1 | cut -d$' ' -f2) == "200" ]
EXIT=$(($EXIT+$?))
[ $(curl -i http://localhost:8000/topics 2>/dev/null | head -n 1 | cut -d$' ' -f2) == "200" ]
EXIT=$(($EXIT+$?))

kill -INT $1
echo "Now I've killed it I hope"
kill -0 $1

echo "Exiting with code ${EXIT}"
exit $EXIT
