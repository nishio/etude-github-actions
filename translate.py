from is_japanese import contains_japanese_characters
import requests
import asyncio
import json
from urllib.parse import quote
import aiohttp
from collections import namedtuple
import os
import re
from tqdm import tqdm
from time import sleep, perf_counter
import dotenv
dotenv.load_dotenv()
DEEPL_KEY = os.getenv("DEEPL_KEY")


def split_indent(line):
    indent, tail = re.match("^([ \t]*)(.*)", line).groups()
    tail = tail.rstrip()  # remove trailing spaces
    return indent, tail


def call_deepl(ja):
    url = "https://api.deepl.com/v2/translate"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "auth_key": DEEPL_KEY,
        "text": ja,
        "source_lang": "JA",
        "target_lang": "EN",
    }
    while True:
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            break
        except:
            sleep(60)
            continue

    result = response.json()
    translated_text = result["translations"][0]["text"]
    return translated_text


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


def translate_from_json_to_json():
    start_time = perf_counter()
    cache_data = "./cache.json"
    in_file = "./data.json"
    data = json.load(open(in_file, "r"))

    total = 0
    no_cache = 0
    # load cache from file
    cache = json.load(open(cache_data, "r"))
    print("cache length:", len(cache))

    def to_english(text):
        nonlocal is_updated, total, no_cache
        indent, body = split_indent(text)
        if not body:
            return text
        total += len(bytes(body, "utf-8"))

        if body not in cache:
            if not contains_japanese_characters(body):
                return text

            no_cache += len(bytes(body, "utf-8"))
            en = call_deepl(body)
            cache[body] = en
            is_updated = True

        return indent + cache[body]

    for page in tqdm(data["pages"]):
        is_updated = False
        page["title"] = to_english(page["title"])
        for line in page["lines"]:
            en_text = to_english(line["text"])
            line["text"] = en_text

        # output cache to file
        if is_updated:
            with open(cache_data, "w") as file:
                json.dump(cache, file, ensure_ascii=False, indent=2)
            print(f"{perf_counter() - start_time:.1f}", "sec: update cache")
    print("total", total, "no_cache", no_cache, "ratio", no_cache / total)
    json.dump(data, open("./data_en.json", "w"), ensure_ascii=False, indent=2)
    print("translate:", perf_counter() - start_time)


def main():
    translate_from_json_to_json()


if __name__ == "__main__":
    main()
