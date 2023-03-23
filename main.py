import asyncio
import json
from urllib.parse import quote
import aiohttp
from collections import namedtuple

TitlePage = namedtuple("TitlePage", ["id", "title", "created", "updated"])

project = "villagepump"
dist_stats = f"./{project}/stats/pages.json"
dist_data = "./data.json"

URL_TEMPLATE = f"https://scrapbox.io/api/pages/{project}"
LIMIT_PARAM = 1000


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def main():
    pages_response = await fetch(f"{URL_TEMPLATE}/?limit=1")
    page_num = pages_response["count"]
    max_index = (page_num // LIMIT_PARAM) + 1

    pages = []
    tasks = [fetch(f"{URL_TEMPLATE}/?limit={LIMIT_PARAM}&skip={index * LIMIT_PARAM}")
             for index in range(max_index)]
    for task in asyncio.as_completed(tasks):
        result = await task
        pages.extend(result["pages"])

    titles = [TitlePage(page["id"], page["title"],
                        page["created"], page["updated"]) for page in pages]
    titles.sort(key=lambda x: x.created)

    write_json(dist_stats, {
        "projectName": project,
        "count": page_num,
        "pages": [title._asdict() for title in titles]
    })

    skip = 100
    detail_pages = []
    for i in range(0, len(titles), skip):
        print(
            f"[scrapbox-external-backup] Start fetching {i} - {i + skip} pages.")

        urls = [
            f"{URL_TEMPLATE}/{quote(title.title, safe='')}" for title in titles[i:i+skip]]
        tasks = [fetch(url) for url in urls]
        for j, task in enumerate(asyncio.as_completed(tasks), start=i):
            print(
                f"[page {j}@scrapbox-external-backup] start fetching /{project}/{titles[j].title}")
            result = await task
            print(
                f"[page {j}@scrapbox-external-backup] finish fetching /{project}/{titles[j].title}")
            detail_pages.append({
                "id": result["id"],
                "title": result["title"],
                "created": result["created"],
                "updated": result["updated"],
                "lines": result["lines"]
            })
        print(f"Finish fetching {i} - {i + skip} pages.")

    with open(dist_data, "w") as file:
        for page in detail_pages:
            file.write(json.dumps(page) + ",\n")
        print("write success")


def write_json(path, data):
    try:
        with open(path, "w") as file:
            json.dump(data, file)
        return "Written to " + path
    except Exception as e:
        return str(e)


asyncio.run(main())
