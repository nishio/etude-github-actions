#!/bin/bash

set -x
git config user.name github-actions[bot]
git config user.email 41898282+github-actions[bot]@users.noreply.github.com
git add -f nishio cache.json
git commit -m "Update pages"
git push -f
