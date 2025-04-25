# ワークフロー詳細

## 概要

このプロジェクトは、GitHub Actionsを使用してScrapboxページの自動翻訳とバックアップを実行します。ワークフローは2つのステージに分かれています：

1. **コミットステージ**（nishio_trans_commit.yaml）：
   - Scrapboxからデータをエクスポート
   - コンテンツを翻訳
   - 翻訳結果を保存してコミット

2. **インポートステージ**（nishio_trans_import.yaml）：
   - コミットステージが成功した場合に実行
   - 翻訳された内容をScrapboxにインポート

## データフロー図

```
[Scrapbox /nishio] --export_from_scrapbox.ts--> [data.json] --translate.py--> [data_en.json]
                                                                                   |
                                                                        merge_same_title_page.py
                                                                                   |
                                                                                   v
[Scrapbox /nishio-en] <--import_to_scrapbox.ts-- [data_en_diff.json] <--diff_json.py-- [data_en.json]
```

## スクリプトの役割

### 1. エクスポート
- **export_from_scrapbox.ts/sh**:
  - Scrapbox APIを使用して `/nishio` プロジェクトのページをエクスポート
  - JSONデータとして `data.json` に保存

### 2. 翻訳
- **translate.py**:
  - DeepL APIを使用して日本語コンテンツを英語に翻訳
  - 翻訳結果を `data_en.json` に保存
  - キャッシュ（`cache.json`）を使用して同じテキストの再翻訳を防止
  - `[en.icon]` タグがあるページは翻訳しない

### 3. ページマージ
- **merge_same_title_page.py**:
  - 同じタイトル（大文字小文字を区別しない）を持つページを識別
  - 同一タイトルのページをマージして重複を防止

### 4. 差分検出
- **diff_json.py**:
  - 現在の翻訳（`data_en.json`）と前回の翻訳（`nishio/data_en_prev.json`）を比較
  - 新規または更新されたページを抽出して `data_en_diff.json` として保存

### 5. インポート
- **import_to_scrapbox.ts/sh**:
  - 差分データ（`data_en_diff.json`）を `/nishio-en` プロジェクトにインポート

### 6. コミット
- **commit.sh**:
  - 変更されたファイルをリポジトリにコミット
  - GitHub Actionsの実行中に自動的に実行される
