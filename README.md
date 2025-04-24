# etude-github-actions

このリポジトリはScrapboxページを日本語から英語に自動翻訳するためのGitHub Actionsワークフローです。詳細は[Scrapboxページ](https://scrapbox.io/nishio/etude-github-actions)を参照してください。

## リポジトリの概要

このプロジェクトは以下の機能を提供します：

1. **自動翻訳ワークフロー**：
   - Scrapboxプロジェクト「/nishio」から日本語ページをエクスポート
   - DeepL APIを使用して英語に翻訳
   - 翻訳されたコンテンツをScrapboxプロジェクト「/nishio-en」にインポート

2. **主要コンポーネント**：
   - Scrapboxページのエクスポート（Deno/TypeScript）
   - 日本語から英語への翻訳（Python/DeepL API）
   - 更新されたページの差分検出（Python）
   - 翻訳されたページのScrapboxへのインポート（Deno/TypeScript）

3. **自動化スケジュール**：
   - 毎日JST 6:00（UTC 21:00）に自動実行
   - 手動実行も可能（GitHub Actionsのワークフロー画面から）

## Special Thanks

derived from following projects.

- https://github.com/meganii/sandbox-github-actions-scheduler/blob/main/.github/workflows/scheduled-build.yml

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
