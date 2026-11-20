#!/bin/sh
# Usage: ./new-video.sh topic-slug   ->  videos/YYYY-MM-DD-topic-slug/ with the template scripts copied in
set -e
cd "$(dirname "$0")"
[ -z "$1" ] && { echo "usage: $0 topic-slug"; exit 1; }
D="videos/$(date +%Y-%m-%d)-$1"
[ -e "$D" ] && { echo "$D already exists"; exit 1; }
mkdir -p "$D/in" "$D/chk" "$D/work" "$D/exported"
cp kit/template/*.py "$D/"
echo "$D"
