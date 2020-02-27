#/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./docker_server.py SERVER_PORT"
    exit 1
fi

SERVER_PORT=$1

docker image remove "${USER}_bot"
docker build --rm --tag="${USER}_bot" .
docker run --tty --interactive --rm --publish=$SERVER_PORT:$SERVER_PORT --name=${USER}_bot --cap-add=NET_RAW --cap-add=NET_ADMIN ${USER}_bot python ./server_bot.py -p $SERVER_PORT
