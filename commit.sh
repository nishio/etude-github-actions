#!/bin/bash
set -ex

# GitHub Actions用のユーザ設定
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

# 現在のブランチを保存
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# 未コミットの変更をstashする
git stash push --include-untracked -m "Stash before switching to auto-update branch"

# リモートの最新情報を取得
git fetch

# auto-updateブランチが存在するか確認
if git show-ref --verify --quiet refs/remotes/origin/auto-update; then
  # auto-updateが存在する場合はチェックアウトして--rebaseで更新
  git checkout auto-update
  git pull --rebase origin auto-update
else
  # 存在しなければ新規作成
  git checkout -b auto-update
fi

# ポップして変更を適用
git stash pop

# 変更を強制的にadd
git add -f nishio cache.json data_en_diff.json

# 変更をコミット
git commit -m "Update pages"

# auto-updateブランチにプッシュ
git push origin auto-update

# 元のブランチに戻る
git checkout $CURRENT_BRANCH