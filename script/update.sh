#!/bin/sh -e

git fetch

LOCAL=$(git rev-parse HEAD )
REMOTE=$(git rev-parse @{u})

[ $LOCAL = $REMOTE ] && echo "up to date ($REMOTE)" && exit 0

echo "new master detected ($LOCAL -> $REMOTE)!"
git reset --hard $REMOTE

# echo "installing...."
# ./script/install.sh

echo "restarting some janky stuff"
python maind.py restart
