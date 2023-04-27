from utils import contains_japanese_characters, get_body_of_line
import requests
import json
import os
import re
from tqdm import tqdm
from time import sleep, perf_counter
import dotenv
dotenv.load_dotenv()
DEEPL_KEY = os.getenv("DEEPL_KEY")
FOOTER = """
This page is auto-translated from [/nishio/{ja_title}].
 If you looks something interesting but the auto-translated English is not good enough to understand it,
 feel free to let me know at @nishio_en https://twitter.com/nishio_en.
 I'm very happy to spread my thought to non-Japanese readers.
""".replace("\n", "")


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
        except Exception as e:
            print(e)
            sleep(60)
            continue

    result = response.json()
    translated_text = result["translations"][0]["text"]
    return translated_text


def generate_line(text):
    return {
        "text": text,
        "created": 946652400,  # 2000-01-01 00:00:00
        "updated": 946652400,
        "userId": "582e63d27c56960011aff09e"  # nishio
    }


def translate_pages(pages):
    total = 0
    no_cache = 0
    # load cache from file
    cache_data = "./cache.json"
    cache = json.load(open(cache_data, "r"))
    print("cache length:", len(cache))

    def translate_links(text):
        # print(text)
        keywords = re.findall("\[(.*?)\]", text)
        # print(keywords)
        for k in keywords:
            en = cache.get(k)
            if en:  # translation exists
                text = text.replace(f"[{k}]", f" [{en}] ")
        # print(text)
        return text

    def to_english(text):
        nonlocal is_updated, total, no_cache
        prefix, body, postfix = get_body_of_line(text)
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

        return prefix + cache[body] + postfix

    for page in tqdm(pages):
        is_updated = False
        ja_title = page["title"]
        page["title"] = to_english(ja_title)
        for line in page["lines"]:
            tl_text = translate_links(line["text"])
            en_text = to_english(tl_text)
            line["text"] = en_text
            # print(en_text)

        page["lines"].extend([
            generate_line("---"),
            generate_line(FOOTER.format(ja_title=ja_title)),
        ])
        # output cache to file
        if is_updated:
            with open(cache_data, "w") as file:
                json.dump(cache, file, ensure_ascii=False, indent=2)
            # print(f"{perf_counter() - start_time:.1f}", "sec: update cache")
    print("total", total, "no_cache", no_cache, "ratio", no_cache / total)


def translate_from_json_to_json():
    start_time = perf_counter()
    in_file = "./data.json"
    data = json.load(open(in_file, "r"))

    # sort page by its updated time
    pages = list(sorted(
        data["pages"],
        key=lambda x: x["updated"], reverse=True))

    translate_pages(pages)  # update pages(and data) destructively
    json.dump(data, open("./data_en.json", "w"), ensure_ascii=False, indent=2)
    print("translate:", perf_counter() - start_time)


def translate_keywords():
    start_time = perf_counter()
    cache_data = "./cache.json"
    in_file = "./keywords.json"
    data = json.load(open(in_file, "r"))
    cache = json.load(open(cache_data, "r"))
    total = 0
    no_cache = 0

    def to_english(text):
        nonlocal total, no_cache
        prefix, body, postfix = get_body_of_line(text)
        if not body:
            return text
        total += len(bytes(body, "utf-8"))

        if body not in cache:
            if not contains_japanese_characters(body):
                return text

            no_cache += len(bytes(body, "utf-8"))
            en = call_deepl(body)
            cache[body] = en

        return prefix + cache[body] + postfix

    print(len(data))
    for kw in tqdm(data):
        # print(kw, to_english(kw))
        to_english(kw)

    with open(cache_data, "w") as file:
        json.dump(cache, file, ensure_ascii=False, indent=2)

    print("total", total, "no_cache", no_cache, "ratio", no_cache / total)
    print("translate:", perf_counter() - start_time)


def main():
    translate_from_json_to_json()


def local_trial_10pages():
    print("running local trial")
    in_file = "./data.json"
    data = json.load(open(in_file, "r"))

    # sort page by its updated time
    pages = list(sorted(
        data["pages"],
        key=lambda x: x["updated"], reverse=True))[:10]
    data["pages"] = pages  # to omit other pages

    translate_pages(pages)  # update pages(and data) destructively
    json.dump(data,
              open("./data_en_local.json", "w"),
              ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # to avoid trials on local environment break CI on GitHub Actions
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        main()
    else:
        print('Not running within a GitHub Actions environment')
        main()
        # local_trial_10pages()
        # translate_keywords()
