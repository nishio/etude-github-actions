# etude-github-actions

This repository contains GitHub Actions workflows for automatic translation and backup of Scrapbox pages. The primary function is to export pages from a Japanese Scrapbox project, translate them to English using DeepL API, and import them to an English Scrapbox project. For more details, see [my Scrapbox](https://scrapbox.io/nishio/etude-github-actions).

## Repository Overview

This project provides the following features:

1. **Automated Translation Workflow**:
   - Export Japanese pages from the Scrapbox project "/nishio"
   - Translate content to English using DeepL API
   - Import translated content to the Scrapbox project "/nishio-en"

2. **Key Components**:
   - Scrapbox page export (Deno/TypeScript)
   - Japanese to English translation (Python/DeepL API)
   - Updated page difference detection (Python)
   - Translated page import to Scrapbox (Deno/TypeScript)

3. **Automation Schedule**:
   - Automatically runs daily at 6:00 JST (21:00 UTC)
   - Can also be manually triggered from the GitHub Actions workflow interface

## Requirements

- GitHub account with repository access
- Scrapbox account with projects to export from and import to
- DeepL API key for translation
- Scrapbox session ID (SID) for authentication

## Repository Structure

- `.github/workflows/`: Contains GitHub Actions workflow configurations
- `scripts/`: Contains utility scripts for the translation process
- `nishio/`: Directory for storing exported and translated data

## GitHub Actions Workflows

This project uses GitHub Actions to automate the translation process:

### Workflow: Auto-translate /nishio (Commit)

File: `.github/workflows/nishio_trans_commit.yaml`

#### Execution Timing
- Automatically runs daily at 6:00 JST (21:00 UTC)
- Can be manually triggered (workflow_dispatch)

#### Process Flow
1. **Export Data from Scrapbox**
   - Retrieves page data from the `/nishio` project
   - Saves as `data.json`
   - Script: `export_from_scrapbox.sh` → `export_from_scrapbox.ts`

2. **Translate from Japanese to English**
   - Uses DeepL API to translate content in `data.json` to English
   - Saves as `data_en.json`
   - Caches translation results in `cache.json` to prevent re-translating the same text
   - Script: `translate.py`

3. **Merge Pages with Same Title**
   - Identifies and merges pages with identical titles
   - Script: `merge_same_title_page.py`

4. **Extract Differences**
   - Compares the previous translation (`nishio/data_en_prev.json`) with the current one (`data_en.json`)
   - Extracts only new or updated pages
   - Saves as `data_en_diff.json`
   - Script: `diff_json.py`

5. **Save Data**
   - Stores current data in the `nishio` directory
   - Saves translation results for future comparison

6. **Commit Changes**
   - Commits modified files to the GitHub repository
   - Script: `commit.sh`

### Workflow: Auto-translate /nishio (Import)

File: `.github/workflows/nishio_trans_import.yaml`

#### Execution Timing
- Automatically runs after the Commit workflow succeeds
- Can be manually triggered (workflow_dispatch)

#### Process Flow
1. **Import to Scrapbox**
   - Imports the difference data (`data_en_diff.json`) to the `/nishio-en` project
   - Script: `import_to_scrapbox.sh` → `import_to_scrapbox.ts`

## Environment Variables

This workflow uses the following environment variables:

### Local Environment Setup

For testing locally, create a `.env` file in the root directory with the following variables:

- `SID`: Scrapbox session ID (required for export and import)
- `DEEPL_KEY`: DeepL API access key (required for translation)

### GitHub Actions Setup

For running in GitHub Actions, set the following secrets in the repository's "Settings" > "Secrets and variables" > "Actions":

- `SID`: Scrapbox session ID
- `DEEPL_KEY`: DeepL API key

These secrets are referenced in the workflow YAML files as `${{ secrets.SID }}` and `${{ secrets.DEEPL_KEY }}`.

## Manual Execution

GitHub Actions workflows can be manually executed with the following steps:

### Commit Workflow

1. Go to the Actions tab of the repository
2. Select the "Auto-translate /nishio (Commit)" workflow
3. Click the "Run workflow" button

### Import Workflow

1. Go to the Actions tab of the repository
2. Select the "Auto-translate /nishio (Import)" workflow
3. Click the "Run workflow" button

## Documentation

Detailed documentation is available in the following files:

- [Setup Guide](./docs/SETUP.md) - Environment setup and testing procedures
- [Workflow Details](./docs/WORKFLOW.md) - Workflow overview and process flow
- [Script Details](./docs/SCRIPTS.md) - Purpose and usage of each script
- [Structure Improvement Proposal](./docs/STRUCTURE.md) - Repository structure improvement proposal

## Special Thanks

Derived from the following projects:

- [sandbox-github-actions-scheduler](https://github.com/meganii/sandbox-github-actions-scheduler/blob/main/.github/workflows/scheduled-build.yml)
  - Idea that use Github Action to backup Scrapbox pages.

- [Scrapbox-Duplicator](https://github.com/blu3mo/Scrapbox-Duplicator/blob/master/index.ts)
  - Idea that automatically import and export Scrapbox pages.

- [scrapbox-userscript-std](https://github.com/takker99/scrapbox-userscript-std/)
  - Useful libraries to handle Scrapbox.

# Japanese

このリポジトリはGitHub Actionsを使用してScrapboxページの自動翻訳とバックアップを行うためのものです。主な機能は、日本語のScrapboxプロジェクトからページをエクスポートし、DeepL APIを使用して英語に翻訳し、英語のScrapboxプロジェクトにインポートすることです。詳細は[Scrapboxページ](https://scrapbox.io/nishio/etude-github-actions)を参照してください。

## 必要条件

- リポジトリへのアクセス権を持つGitHubアカウント
- エクスポート元とインポート先のプロジェクトを持つScrapboxアカウント
- 翻訳用のDeepL APIキー
- 認証用のScrapboxセッションID（SID）

## リポジトリ構造

- `.github/workflows/`: GitHub Actionsワークフローの設定ファイルを含むディレクトリ
- `scripts/`: 翻訳プロセス用のユーティリティスクリプトを含むディレクトリ
- `nishio/`: エクスポートおよび翻訳されたデータを保存するディレクトリ

## GitHub Actionsの説明

このプロジェクトでは、GitHub Actionsを使用して以下の処理を自動化しています：

### ワークフロー: Auto-translate /nishio (Commit)

ファイル: `.github/workflows/nishio_trans_commit.yaml`

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

3. **同一タイトルのページのマージ**
   - 同じタイトルを持つページを識別し、マージします
   - 使用スクリプト: `merge_same_title_page.py`

4. **差分の抽出**
   - 前回の翻訳結果（`nishio/data_en_prev.json`）と今回の翻訳結果（`data_en.json`）を比較
   - 新規または更新されたページのみを抽出し、`data_en_diff.json`として保存
   - 使用スクリプト: `diff_json.py`

5. **データの保存**
   - 現在のデータを`nishio`ディレクトリに保存
   - 翻訳結果を次回の差分比較のために保存

6. **変更のコミット**
   - 変更されたファイルをGitHubリポジトリにコミット
   - 使用スクリプト: `commit.sh`

### ワークフロー: Auto-translate /nishio (Import)

ファイル: `.github/workflows/nishio_trans_import.yaml`

#### 実行タイミング
- Commitワークフローが成功した後に自動実行
- 手動実行も可能（workflow_dispatch）

#### 処理の流れ
1. **Scrapboxへのインポート**
   - 差分データ（`data_en_diff.json`）を`/nishio-en`プロジェクトにインポート
   - 使用スクリプト: `import_to_scrapbox.sh` → `import_to_scrapbox.ts`

## 環境変数の設定

このワークフローでは以下の環境変数を使用しています：

### ローカル環境での設定

ローカル環境でテストする場合は、ルートディレクトリに`.env`ファイルを作成し、以下の変数を設定します：

- `SID`: ScrapboxのセッションID（エクスポート・インポートに必要）
- `DEEPL_KEY`: DeepL APIのアクセスキー（翻訳に必要）

### GitHub Actionsでの設定

GitHub Actionsで実行する場合は、リポジトリの「Settings」>「Secrets and variables」>「Actions」から以下のシークレットを設定します：

- `SID`: ScrapboxのセッションID
- `DEEPL_KEY`: DeepL APIのアクセスキー

これらのシークレットは、ワークフローのYAMLファイルで`${{ secrets.SID }}`および`${{ secrets.DEEPL_KEY }}`として参照されています。

## 手動実行方法

GitHub Actionsのワークフローは以下の手順で手動実行できます：

### Commitワークフロー

1. リポジトリのActionsタブに移動
2. 「Auto-translate /nishio (Commit)」ワークフローを選択
3. 「Run workflow」ボタンをクリック

### Importワークフロー

1. リポジトリのActionsタブに移動
2. 「Auto-translate /nishio (Import)」ワークフローを選択
3. 「Run workflow」ボタンをクリック

## Special Thanks

以下のプロジェクトを参考にしています：

- https://github.com/meganii/sandbox-github-actions-scheduler/blob/main/.github/workflows/scheduled-build.yml
    - GitHub Actionsを使用してScrapboxページをバックアップするアイデア

- https://github.com/blu3mo/Scrapbox-Duplicator/blob/master/index.ts
    - Scrapboxページの自動インポート・エクスポートのアイデア

- https://github.com/takker99/scrapbox-userscript-std/
    - Scrapboxを扱うための便利なライブラリ

## ドキュメント

詳細なドキュメントは以下のファイルを参照してください：

- [セットアップ手順](./docs/SETUP.md) - 環境設定とテスト方法
- [ワークフロー詳細](./docs/WORKFLOW.md) - ワークフローの全体像と処理フロー
- [スクリプト詳細](./docs/SCRIPTS.md) - 各スクリプトの役割と使い方
- [構造改善提案](./docs/STRUCTURE.md) - リポジトリ構造の改善案

※ 将来的には、コードの整理とリファクタリングも検討していますが、まずはドキュメントの整備を行いました。
