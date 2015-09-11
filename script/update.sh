#!/bin/sh

LOCAL=$(git rev-parse HEAD )
REMOTE=$(git rev-parse @{u})
echo $LOCAL
echo $REMOTE

if [ $LOCAL = $REMOTE ]; then
    echo 'up to date....'
    exit;
fi

echo 'new master detected, pulling now!'
git pull
./script/install.sh
