# 環境設定とテスト方法

## 前提条件

- [Node.js](https://nodejs.org/)
- [Python 3.10+](https://www.python.org/downloads/)
- [Deno](https://deno.land/#installation)
- DeepL APIキー
- Scrapboxアカウントとセッション ID (SID)

## 環境変数の設定

1. リポジトリのルートディレクトリに `.env` ファイルを作成します:

```bash
cp .env_sample .env
```

2. `.env` ファイルに必要な環境変数を設定します:

```
DEEPL_KEY=your_deepl_api_key
SID=connect.sid=your_scrapbox_session_id
```

### Scrapboxセッション ID (SID) の取得方法

1. Scrapboxにログインします
2. ブラウザの開発者ツール（F12）を開きます
3. Application（アプリケーション）タブに移動します
4. Storage > Cookies > scrapbox.io を選択します
5. `connect.sid` の値がSIDです

## 依存関係のインストール

### Pythonの依存関係

```bash
pip install -r requirements.txt
```

### Denoの依存関係

Denoは依存関係を自動的に管理するため、特別なインストール手順は必要ありません。

## ローカルでのテスト方法

### ワークフロー全体のテスト

```bash
./local_batch.sh
```

このスクリプトは以下の処理を順番に実行します:
1. Scrapboxからデータをエクスポート
2. データを翻訳
3. 同一タイトルのページをマージ
4. 差分を計算
5. 翻訳されたデータをScrapboxにインポート
6. データを保存
7. 変更をコミット

### 個別のステップのテスト

1. エクスポートのみをテスト:
```bash
./export_from_scrapbox.sh
```

2. 翻訳のみをテスト:
```bash
python translate.py
```

3. 差分計算のみをテスト:
```bash
python diff_json.py
```

4. インポートのみをテスト:
```bash
./import_to_scrapbox.sh
```

## [en.icon]タグのテスト

[en.icon]タグを持つページが翻訳されないことをテストするには:

```bash
python test_en_icon.py
```

## GitHub Actionsでの実行

GitHub Actionsは以下の2つのワークフローを使用します:

1. **Commitワークフロー**: データのエクスポート、翻訳、コミット
   - 毎日JST 6:00（UTC 21:00）に自動実行
   - GitHub Actionsタブから手動で実行可能

2. **Importワークフロー**: 翻訳されたデータのインポート
   - Commitワークフローが成功した後に自動実行
   - GitHub Actionsタブから手動で実行可能

### GitHub Secretsの設定

GitHub Actionsでワークフローを実行するには、リポジトリのSettings > Secrets and variables > Actionsから以下のシークレットを設定する必要があります:

1. `SID`: ScrapboxのセッションID
2. `DEEPL_KEY`: DeepL APIのキー
