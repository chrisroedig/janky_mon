#!/bin/sh

LOCAL=$(git rev-parse HEAD )
REMOTE=$(git rev-parse @{u})
BASE=$(git merge-base @ @{u})

if [ $LOCAL = $REMOTE ]; then
    echo 'up to date....'
    exit;
fi

echo 'new master detected, pulling now!'
git pull
./script/install.sh
