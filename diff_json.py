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

print(len(updated_pages))

# write diff to file
curr["pages"] = updated_pages
with open("data_en_diff.json", "w") as file:
    json.dump(curr, file, ensure_ascii=False, indent=2)
