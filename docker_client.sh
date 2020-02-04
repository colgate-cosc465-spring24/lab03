#/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: ./docker_client.py SERVER_HOSTNAME SERVER_PORT"
    exit 1
fi

SERVER_HOSTNAME=$1
SERVER_PORT=$2

docker image remove "${USER}_bot"
docker build --rm --tag="${USER}_bot" .
docker run --tty --interactive --rm --name=${USER}_bot --cap-add=NET_RAW --cap-add=NET_ADMIN ${USER}_bot python ./client_bot.py -h $SERVER_HOSTNAME -p $SERVER_PORT
