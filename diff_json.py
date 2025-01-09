import json
# load prev and current json
prev = json.load(open("nishio/data_en_prev.json", "r"))
curr = json.load(open("data_en.json", "r"))
# find updated pages
updated_pages = []
prev_map = {page["title"]: page for page in prev["pages"]}
for page in curr["pages"]:
    if page["title"] not in prev_map:
        updated_pages.append(page)
        continue
    prev_page = prev_map[page["title"]]
    if prev_page["lines"] != page["lines"]:
        updated_pages.append(page)

print(f"Total pages in current data: {len(curr['pages'])}")
print(f"Total pages in previous data: {len(prev['pages'])}")
print(f"Total updated pages: {len(updated_pages)}")

# Take first 100 pages for testing
test_pages = updated_pages[:100]
print(f"Using first {len(test_pages)} pages for import")
print(f"Pages to be imported: {[page['title'] for page in test_pages]}")

# write diff to file
curr["pages"] = test_pages
with open("data_en_diff.json", "w") as file:
    json.dump(curr, file, ensure_ascii=False, indent=2)
