"""
Initial code for translating all pages in a directory.
Those page files are from `crawl.py`.
However currently I focus on translating `data.json` file from `export_from_scrapbox.ts`.

This code is not used in the project now. Maybe in future I need this.
"""

# def translate_from_dir():
#     start_time = perf_counter()
#     cache_data = "./cache.json"
#     PAGES_DIR = f"./nishio/pages"
#     ENGLISH_DIR = f"./nishio/pages_en"
#     os.makedirs(ENGLISH_DIR, exist_ok=True)

#     total = 0
#     no_cache = 0
#     # load cache from file
#     cache = json.load(open(cache_data, "r"))

#     print("cache length:", len(cache))
#     target = os.listdir(PAGES_DIR)
#     # target = target[:300]
#     for name in tqdm(target):
#         is_updated = False
#         with open(os.path.join(PAGES_DIR, name), "r") as file:
#             data = json.load(file)
#             result_lines = []
#             for line in data["lines"]:
#                 # for line in tqdm(data["lines"]):
#                 text = line["text"]
#                 indent, body = split_indent(text)
#                 if not body:
#                     result_lines.append(text)
#                     continue
#                 total += len(bytes(body, "utf-8"))
#                 # print(line)

#                 if body not in cache:
#                     if not contains_japanese_characters(body):
#                         result_lines.append(text)
#                         continue

#                     no_cache += len(bytes(body, "utf-8"))
#                     en = call_deepl(body)
#                     cache[body] = en
#                     is_updated = True

#                 result_lines.append(indent + cache[body])
#         # output to file
#         base, ext = os.path.splitext(name)
#         outpath = os.path.join(ENGLISH_DIR, base + ".txt")
#         with open(outpath, "w") as file:
#             file.write("\n".join(result_lines))
#         # output cache to file
#         if is_updated:
#             with open(cache_data, "w") as file:
#                 json.dump(cache, file, ensure_ascii=False, indent=2)
#             print(f"{perf_counter() - start_time:.1f}", "sec: update cache")
#     print("total", total, "no_cache", no_cache, "ratio", no_cache / total)

#     print("translate:", perf_counter() - start_time)
