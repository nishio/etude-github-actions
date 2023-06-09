from utils import contains_japanese_characters
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

TitlePage = namedtuple("TitlePage", ["id", "title", "created", "updated"])


LIMIT_PARAM = 1000


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def crawl(project):
    start_time = perf_counter()
    URL_TEMPLATE = f"https://scrapbox.io/api/pages/{project}"
    pages_response = await fetch(f"{URL_TEMPLATE}/?limit=1")
    page_num = pages_response["count"]
    max_index = (page_num // LIMIT_PARAM) + 1

    pages = []
    tasks = [fetch(f"{URL_TEMPLATE}/?limit={LIMIT_PARAM}&skip={index * LIMIT_PARAM}")
             for index in range(max_index)]
    for task in asyncio.as_completed(tasks):
        result = await task
        pages.extend(result["pages"])

    titles = [
        TitlePage(
            page["id"], page["title"],
            page["created"], page["updated"])
        for page in pages]
    titles.sort(key=lambda x: -x.created)

    stat = {
        "projectName": project,
        "count": page_num,
        "pages": [title._asdict() for title in titles]
    }

    os.makedirs(f"./{project}/stats", exist_ok=True)
    dist_stats = f"./{project}/stats/pages.json"
    with open(dist_stats, "w") as file:
        json.dump(stat, file, ensure_ascii=False, indent=2)

    skip = 100
    detail_pages = []
    for i in tqdm(range(0, len(titles), skip)):
        # print(
        #     f"[scrapbox-external-backup] Start fetching {i} - {i + skip} pages.")

        urls = [
            f"{URL_TEMPLATE}/{quote(title.title, safe='')}"
            for title in titles[i:i+skip]]
        tasks = [fetch(url) for url in urls]
        for j, task in enumerate(asyncio.as_completed(tasks), start=i):
            # print(
            #     f"[page {j}@scrapbox-external-backup] start fetching /{project}/{titles[j].title}")
            result = await task
            # print(
            #     f"[page {j}@scrapbox-external-backup] finish fetching /{project}/{titles[j].title}")
            detail_pages.append({
                "id": result["id"],
                "title": result["title"],
                "created": result["created"],
                "updated": result["updated"],
                "lines": result["lines"]
            })
        print(f"Finish fetching {i} - {i + skip} pages.")

    PAGES_DIR = f"./{project}/pages"
    os.makedirs(PAGES_DIR, exist_ok=True)

    for page in detail_pages:
        with open(f"{PAGES_DIR}/{page['id']}.json", "w") as file:
            json.dump(page, file, ensure_ascii=False, indent=2)

    print("crawl:", perf_counter() - start_time)


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


def translate():
    start_time = perf_counter()
    cache_data = "./cache.json"
    PAGES_DIR = f"./nishio/pages"
    ENGLISH_DIR = f"./nishio/pages_en"
    os.makedirs(ENGLISH_DIR, exist_ok=True)

    total = 0
    no_cache = 0
    # load cache from file
    cache = json.load(open(cache_data, "r"))
    print("cache length:", len(cache))
    target = os.listdir(PAGES_DIR)
    # target = target[:300]
    for name in tqdm(target):
        is_updated = False
        with open(os.path.join(PAGES_DIR, name), "r") as file:
            data = json.load(file)
            result_lines = []
            for line in data["lines"]:
                # for line in tqdm(data["lines"]):
                text = line["text"]
                indent, body = split_indent(text)
                if not body:
                    result_lines.append(text)
                    continue
                total += len(bytes(body, "utf-8"))
                # print(line)

                if body not in cache:
                    if not contains_japanese_characters(body):
                        result_lines.append(text)
                        continue

                    no_cache += len(bytes(body, "utf-8"))
                    en = call_deepl(body)
                    cache[body] = en
                    is_updated = True

                result_lines.append(indent + cache[body])
        # output to file
        base, ext = os.path.splitext(name)
        outpath = os.path.join(ENGLISH_DIR, base + ".txt")
        with open(outpath, "w") as file:
            file.write("\n".join(result_lines))
        # output cache to file
        if is_updated:
            with open(cache_data, "w") as file:
                json.dump(cache, file, ensure_ascii=False, indent=2)
            print(f"{perf_counter() - start_time:.1f}", "sec: update cache")
    print("total", total, "no_cache", no_cache, "ratio", no_cache / total)

    print("translate:", perf_counter() - start_time)


def main():
    print("crawl")
    asyncio.run(crawl("nishio"))
    print("translate")
    translate()


if __name__ == "__main__":
    main()
