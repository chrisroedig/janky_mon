#!/bin/sh

git fetch

LOCAL=$(git rev-parse HEAD )
REMOTE=$(git rev-parse @{u})

echo $LOCAL
echo $REMOTE

if [ $LOCAL = $REMOTE ]; then
    echo 'up to date....'
    exit 0;
fi

echo 'new master detected, pulling now!'
git pull
./script/install.sh

exit 1;
