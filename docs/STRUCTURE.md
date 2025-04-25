# リポジトリ構造の改善提案

現在のリポジトリ構造は、すべてのスクリプトがルートディレクトリに配置されており、役割や関連性が分かりにくくなっています。以下のディレクトリ構造への変更を提案します：

```
etude-github-actions/
├── .github/
│   └── workflows/
│       ├── nishio_trans_commit.yaml
│       └── nishio_trans_import.yaml
├── src/
│   ├── export/
│   │   ├── export_from_scrapbox.ts
│   │   └── export_from_scrapbox.sh
│   ├── translate/
│   │   ├── translate.py
│   │   ├── merge_same_title_page.py
│   │   └── diff_json.py
│   ├── import/
│   │   ├── import_to_scrapbox.ts
│   │   └── import_to_scrapbox.sh
│   └── utils/
│       ├── utils.py
│       └── commit.sh
├── scripts/
│   ├── local_batch.sh
│   └── correct_trans.py
├── tests/
│   └── test_en_icon.py
├── docs/
│   ├── SETUP.md
│   ├── WORKFLOW.md
│   └── STRUCTURE.md
├── .env_sample
├── deps.ts
├── requirements.txt
└── README.md
```

この構造の利点：
1. 関連するスクリプトが論理的にグループ化されている
2. 各ディレクトリの目的が明確
3. ドキュメントが専用ディレクトリに整理されている
4. テストが独立したディレクトリに配置されている

## 実装手順

リポジトリ構造を改善するための手順は以下の通りです：

1. 必要なディレクトリを作成する
```bash
mkdir -p src/{export,translate,import,utils} scripts tests
```

2. スクリプトを適切なディレクトリに移動する
```bash
# エクスポート関連
mv export_from_scrapbox.ts export_from_scrapbox.sh src/export/

# 翻訳関連
mv translate.py merge_same_title_page.py diff_json.py src/translate/

# インポート関連
mv import_to_scrapbox.ts import_to_scrapbox.sh src/import/

# ユーティリティ
mv utils.py commit.sh src/utils/

# スクリプト
mv local_batch.sh correct_trans.py crawl.py collect_keywords.py scripts/

# テスト
mv test_en_icon.py tests/
```

3. インポートパスとファイル参照を更新する

各スクリプト内のインポートパスと相対パス参照を更新する必要があります。例えば：

```python
# 変更前
from utils import contains_japanese_characters

# 変更後
from src.utils.utils import contains_japanese_characters
```

4. GitHub Actionsワークフローファイルのパス参照を更新する

`.github/workflows/nishio_trans_commit.yaml` と `.github/workflows/nishio_trans_import.yaml` 内のスクリプトパス参照を更新します：

```yaml
# 変更前
run: ./export_from_scrapbox.sh

# 変更後
run: ./src/export/export_from_scrapbox.sh
```

5. local_batch.shスクリプトを更新する

ローカルテスト用のスクリプトも新しいパス構造に合わせて更新する必要があります。

## 段階的な実装

この構造変更は一度に行うと既存の機能に影響を与える可能性があるため、以下の段階的なアプローチを推奨します：

1. まず、ドキュメントディレクトリ（docs/）を作成し、ドキュメントを整備する
2. テストディレクトリ（tests/）を作成し、テストスクリプトを移動する
3. src/ディレクトリを作成し、各カテゴリごとにスクリプトを移動する
4. 各ステップごとにテストを実行して機能が正常に動作することを確認する

この段階的なアプローチにより、リファクタリングによる影響を最小限に抑えながら、コードベースを整理することができます。
