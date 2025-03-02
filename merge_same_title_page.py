import json
import copy
from collections import Counter

# data_en_prev.jsonを読む
with open("nishio/data_en_prev.json", "r", encoding="utf-8") as f:
    data_en_prev = json.load(f)

# data_en_prev.pages.titleを取得して何件あるか確認
titles = [page["title"] for page in data_en_prev["pages"]]
print(f"data_en_prev.jsonのタイトル数: {len(titles)}")

# タイトルの重複をチェックし、タイトルごとにページのインデックスを保存
# 大文字小文字を区別せずにチェック
title_indices = {}
duplicates = []
title_case_map = {}  # 小文字のタイトルから元のタイトルへのマッピング

for i, page in enumerate(data_en_prev["pages"]):
    title = page["title"]
    title_lower = title.lower()  # タイトルを小文字に変換

    if title_lower in title_indices:
        title_indices[title_lower].append(i)
        if (
            len(title_indices[title_lower]) == 2
        ):  # 初めて重複を検出した時だけリストに追加
            duplicates.append(title_lower)
    else:
        title_indices[title_lower] = [i]
        title_case_map[title_lower] = title  # 元のケースを保存

# 重複タイトルの報告
print(f"\n重複タイトル数（大文字小文字を区別しない）: {len(duplicates)}")

# 新しいpagesリストを作成
new_pages = []

# 重複していないタイトルのページをそのまま追加
for page in data_en_prev["pages"]:
    title = page["title"]
    title_lower = title.lower()
    if title_lower not in duplicates:
        new_pages.append(page)

# 重複タイトルを持つページをマージして追加
for title_lower in duplicates:
    # 同じタイトルを持つページのインデックスを取得
    indices = title_indices[title_lower]

    # updatedの値でソート（新しい順）
    pages_to_merge = [data_en_prev["pages"][idx] for idx in indices]
    pages_to_merge.sort(key=lambda x: x.get("updated", 0), reverse=True)

    # マージされたページを作成
    merged_page = copy.deepcopy(pages_to_merge[0])  # 最も新しいページをベースにする
    merged_lines = []

    # 全てのページのlinesを結合
    for p in pages_to_merge:
        if "lines" in p:
            merged_lines.extend(p.get("lines", []))

    merged_page["lines"] = merged_lines
    new_pages.append(merged_page)

# マージ結果の報告
print(f"\n元のページ数: {len(data_en_prev['pages'])}")
print(f"マージ後のページ数: {len(new_pages)}")

# マージ後のタイトルの重複をチェック（大文字小文字を区別しない）
new_titles_lower = [page["title"].lower() for page in new_pages]
unique_titles_lower = set(new_titles_lower)
print(
    f"マージ後の一意のタイトル数（大文字小文字を区別しない）: {len(unique_titles_lower)}"
)
print(
    f"タイトルの重複がないことを確認（大文字小文字を区別しない）: {len(new_titles_lower) == len(unique_titles_lower)}"
)

# マージされたページの例を表示（最初の5件）
print("\nマージされたページの例（最初の5件）:")
for i, title_lower in enumerate(duplicates[:5]):
    print(f"\n- {title_case_map.get(title_lower, title_lower)}")
    # 該当するページを探す
    merged_page = None
    for page in new_pages:
        if page["title"].lower() == title_lower:
            merged_page = page
            break

    if merged_page:
        lines_preview = merged_page.get("lines", [])[:5]  # 最初の5行を表示
        for line in lines_preview:
            print(f"  {line[:100]}..." if len(line) > 100 else f"  {line}")

# マージされたデータを新しいJSONファイルに保存
merged_data = copy.deepcopy(data_en_prev)
merged_data["pages"] = new_pages

with open("nishio/data_en_merged.json", "w", encoding="utf-8") as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=2)

print("\nマージされたデータを nishio/data_en_merged.json に保存しました。")

# マージされたデータを読み込んで重複がないか詳細に確認（大文字小文字を区別しない）
print("\n=== マージされたデータの詳細確認（大文字小文字を区別しない） ===")
with open("nishio/data_en_merged.json", "r", encoding="utf-8") as f:
    merged_data = json.load(f)

# タイトルの重複を詳細にチェック（大文字小文字を区別しない）
merged_titles_lower = [page["title"].lower() for page in merged_data["pages"]]
title_counts = Counter(merged_titles_lower)
duplicate_titles = [title for title, count in title_counts.items() if count > 1]

if duplicate_titles:
    print(
        f"警告: マージ後のデータにまだ重複タイトルが {len(duplicate_titles)} 件あります。"
    )
    print("重複タイトルの一覧:")
    for title in duplicate_titles:
        print(f"- {title} (出現回数: {title_counts[title]})")
        # 該当するページのタイトルを表示
        for page in merged_data["pages"]:
            if page["title"].lower() == title:
                print(f"  - {page['title']}")
else:
    print(
        "確認完了: マージ後のデータにタイトルの重複はありません（大文字小文字を区別しない）。"
    )
    print(
        f"合計 {len(merged_data['pages'])} 件のページがあり、全て一意のタイトルを持っています。"
    )
