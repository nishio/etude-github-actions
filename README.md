# etude-github-actions

This is a repository for studying GitHub Actions. see more in [my Scrapbox](https://scrapbox.io/nishio/etude-github-actions).

## Special Thanks

derived from following projects.

- https://github.com/meganii/sandbox-github-actions-scheduler/blob/main/.github/workflows/scheduled-build.yml

    - Idea that use Github Action to backup Scrapbox pages.

- https://github.com/blu3mo/Scrapbox-Duplicator/blob/master/index.ts

    - Idea that automatically import and export Scrapbox pages.

- https://github.com/takker99/scrapbox-userscript-std/

    - Useful libraries to handle Scrapbox.

# Japanese

このリポジトリはGitHub Actionsを使用してScrapboxページの自動翻訳とバックアップを行うためのものです。詳細は[Scrapboxページ](https://scrapbox.io/nishio/etude-github-actions)を参照してください。

## GitHub Actionsの説明

このプロジェクトでは、GitHub Actionsを使用して以下の処理を自動化しています：

### ワークフロー: Auto-translate /nishio

ファイル: `.github/workflows/nishio_trans.yaml`

#### 実行タイミング
- 毎日JST 6:00（UTC 21:00）に自動実行
- 手動実行も可能（workflow_dispatch）

#### 処理の流れ
1. **Scrapboxからデータをエクスポート**
   - `/nishio`プロジェクトのページデータを取得し、`data.json`として保存
   - 使用スクリプト: `export_from_scrapbox.sh` → `export_from_scrapbox.ts`

2. **日本語から英語への翻訳**
   - DeepL APIを使用して`data.json`の内容を英語に翻訳し、`data_en.json`として保存
   - 翻訳結果はキャッシュ（`cache.json`）に保存され、同じテキストの再翻訳を防止
   - 使用スクリプト: `translate.py`

3. **差分の抽出**
   - 前回の翻訳結果（`nishio/data_en_prev.json`）と今回の翻訳結果（`data_en.json`）を比較
   - 新規または更新されたページのみを抽出し、`data_en_diff.json`として保存
   - 使用スクリプト: `diff_json.py`

4. **データの保存**
   - 現在のデータを`nishio`ディレクトリに保存
   - 翻訳結果を次回の差分比較のために保存

5. **変更のコミット**
   - 変更されたファイルをGitHubリポジトリにコミット
   - 使用スクリプト: `commit.sh`

6. **Scrapboxへのインポート**
   - 差分データ（`data_en_diff.json`）を`/nishio-en`プロジェクトにインポート
   - 使用スクリプト: `import_to_scrapbox.sh` → `import_to_scrapbox.ts`

### 環境変数の設定

このワークフローでは以下の環境変数（GitHub Secrets）を使用しています：
- `SID`: ScrapboxのセッションID（エクスポート・インポートに必要）
- `DEEPL_KEY`: DeepL APIのアクセスキー（翻訳に必要）

## 手動実行方法

GitHub Actionsのワークフローは以下の手順で手動実行できます：
1. リポジトリのActionsタブに移動
2. 「Auto-translate /nishio」ワークフローを選択
3. 「Run workflow」ボタンをクリック

## Special Thanks

以下のプロジェクトを参考にしています：

- https://github.com/meganii/sandbox-github-actions-scheduler/blob/main/.github/workflows/scheduled-build.yml
    - GitHub Actionsを使用してScrapboxページをバックアップするアイデア

- https://github.com/blu3mo/Scrapbox-Duplicator/blob/master/index.ts
    - Scrapboxページの自動インポート・エクスポートのアイデア

- https://github.com/takker99/scrapbox-userscript-std/
    - Scrapboxを扱うための便利なライブラリ