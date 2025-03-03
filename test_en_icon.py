import json
import os
import sys
from translate import translate_one_page

# グローバル変数の初期化
cache = {}
is_updated = False
total = 0
no_cache = 0

def test_en_icon_tag():
    # テスト用のページデータを作成
    page_with_en_icon = {
        "title": "Test Page with en.icon",
        "lines": [
            {"text": "This is a test page."},
            {"text": "It has [en.icon] tag."},
            {"text": "[en.icon]"}
        ]
    }
    
    page_without_en_icon = {
        "title": "Test Page without en.icon",
        "lines": [
            {"text": "This is a test page."},
            {"text": "It does not have en.icon tag."}
        ]
    }
    
    # [en.icon]タグがあるページの翻訳をテスト
    print("Testing page with [en.icon] tag...")
    result = translate_one_page(page_with_en_icon)
    print(f"Result: {result}")
    if result is False:
        print("✅ Test passed: Page with [en.icon] tag was not translated.")
    else:
        print("❌ Test failed: Page with [en.icon] tag was translated.")

def test_way_of_thinking_page():
    # 「Way of thinking」ページのJSONファイルを読み込む
    try:
        with open("./nishio/pages/61e91b38b3495c001e9ef8be.json", "r") as f:
            way_of_thinking_page = json.load(f)
        
        # [en.icon]タグがあるか確認
        has_en_icon = False
        for line in way_of_thinking_page["lines"]:
            if "[en.icon]" in line["text"]:
                has_en_icon = True
                break
        
        if has_en_icon:
            print("\nTesting 'Way of thinking' page...")
            result = translate_one_page(way_of_thinking_page)
            print(f"Result: {result}")
            if result is False:
                print("✅ Test passed: 'Way of thinking' page with [en.icon] tag was not translated.")
            else:
                print("❌ Test failed: 'Way of thinking' page with [en.icon] tag was translated.")
        else:
            print("\n❓ 'Way of thinking' page does not have [en.icon] tag.")
    except Exception as e:
        print(f"\n❌ Error loading 'Way of thinking' page: {e}")

if __name__ == "__main__":
    # キャッシュファイルの準備
    with open("./cache.json", "w") as f:
        json.dump({}, f)
    
    # テスト実行
    test_en_icon_tag()
    test_way_of_thinking_page()
