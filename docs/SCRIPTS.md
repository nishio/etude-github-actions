# スクリプト詳細

## 主要スクリプト

### export_from_scrapbox.ts
**目的**: Scrapbox APIを使用してプロジェクトページをエクスポートする

**使用法**:
```bash
./export_from_scrapbox.sh
```

**依存関係**:
- Deno
- deps.ts（Scrapbox APIクライアント）
- 環境変数: SID（Scrapboxセッション ID）

**出力**: data.json

---

### translate.py
**目的**: DeepL APIを使用して日本語コンテンツを英語に翻訳する

**使用法**:
```bash
python translate.py
```

**依存関係**:
- Python 3.10+
- requests, tqdm, dotenv
- 環境変数: DEEPL_KEY

**重要な機能**:
- 翻訳キャッシュ（cache.json）の管理
- [en.icon]タグがあるページをスキップ
- 翻訳結果にフッター情報を追加

**入力**: data.json
**出力**: data_en.json

---

### merge_same_title_page.py
**目的**: 同じタイトル（大文字小文字を区別しない）を持つページをマージする

**使用法**:
```bash
python merge_same_title_page.py
```

**入力**: data_en.json
**出力**: 更新された data_en.json（マージ後）

---

### diff_json.py
**目的**: 現在の翻訳と前回の翻訳を比較して差分を抽出する

**使用法**:
```bash
python diff_json.py
```

**入力**:
- data_en.json（現在の翻訳）
- nishio/data_en_prev.json（前回の翻訳）

**出力**: data_en_diff.json（差分のみ）

---

### import_to_scrapbox.ts
**目的**: 翻訳されたコンテンツをScrapboxプロジェクトにインポートする

**使用法**:
```bash
./import_to_scrapbox.sh
```

**依存関係**:
- Deno
- deps.ts（Scrapbox APIクライアント）
- 環境変数: SID（Scrapboxセッション ID）

**入力**: data_en_diff.json
**出力**: none（Scrapboxプロジェクトが更新される）

## ユーティリティスクリプト

### utils.py
**目的**: 共通のユーティリティ関数を提供する

**主な機能**:
- `contains_japanese_characters`: 文字列に日本語文字が含まれているかを判定
- `get_body_of_line`: 行からインデント、本文、アイコンタグを抽出

### commit.sh
**目的**: 変更をリポジトリにコミットする

**使用法**:
```bash
./commit.sh
```

## テストスクリプト

### test_en_icon.py
**目的**: [en.icon]タグを持つページが翻訳されないことをテストする

**使用法**:
```bash
python test_en_icon.py
```

## その他のスクリプト

### correct_trans.py
**目的**: キャッシュ内の翻訳を修正する

**使用法**:
```bash
python correct_trans.py
```

### local_batch.sh
**目的**: ローカル環境でワークフロー全体をテストする

**使用法**:
```bash
./local_batch.sh
```

### crawl.py
**目的**: Scrapboxプロジェクトのページをクロールしてローカルに保存する

**使用法**:
```bash
python crawl.py
```

**主な機能**:
- Scrapbox APIを使用してプロジェクトのすべてのページを取得
- ページデータをJSONファイルとして保存
- 翻訳機能も含まれているが、現在のワークフローでは使用されていない

### collect_keywords.py
**目的**: Scrapboxプロジェクトからキーワードを収集する

**使用法**:
```bash
python collect_keywords.py
```

**主な機能**:
- Scrapbox APIを使用してプロジェクトのキーワードを収集
- 現在のワークフローでは使用されていない
