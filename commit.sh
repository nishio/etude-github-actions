#!/bin/bash
set -ex

# GitHub Actions用のユーザ設定
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

# 最新のmainブランチを取得
git fetch origin main
git checkout main
git pull origin main

# 変更を強制的にadd
git add -f nishio cache.json data_en_diff.json

# 変更をコミット
git commit -m "[data] Update translated pages"

# mainブランチにプッシュ
git push origin main