#!/bin/sh -e

git fetch

LOCAL=$(git rev-parse HEAD )
REMOTE=$(git rev-parse @{u})

[ $LOCAL = $REMOTE ] && echo "up to date ($REMOTE)" && exit 0

echo "new master detected ($LOCAL -> $REMOTE)!"
git reset --hard $REMOTE
./script/install.sh

