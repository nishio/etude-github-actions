#!/bin/bash

set -x
git config user.name github-actions[bot]
git config user.email 41898282+github-actions[bot]@users.noreply.github.com

# 現在のブランチを保存
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# auto-updateブランチが存在するか確認し、なければ作成
git fetch
if git show-ref --verify --quiet refs/remotes/origin/auto-update; then
  # ブランチが存在する場合、チェックアウト
  git checkout auto-update
  git pull origin auto-update
else
  # ブランチが存在しない場合、新規作成
  git checkout -b auto-update
fi

# 変更をコミット
git add -f nishio cache.json
git commit -m "Update pages"

# プッシュ（強制プッシュなし）
git push origin auto-update

# 元のブランチに戻る
git checkout $CURRENT_BRANCH
