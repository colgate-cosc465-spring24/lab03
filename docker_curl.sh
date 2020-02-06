#/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./docker_curl.py URI"
    exit 1
fi

URI=$1

docker image remove "${USER}_bot"
docker build --rm --tag="${USER}_bot" .
docker run --tty --interactive --rm --name=${USER}_bot --cap-add=NET_RAW --cap-add=NET_ADMIN ${USER}_bot python ./run_curl.py -u $URI
