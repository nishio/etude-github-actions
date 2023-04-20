"""
translated from import_to_scrapbox.ts
"""

import aiohttp
import asyncio
from typing import Any, Dict, Tuple, Union
import json
import requests
import os
import dotenv
dotenv.load_dotenv()
SID = os.getenv("SID")
CSRF = os.getenv("CSRF")
PROJECT_NAME = os.getenv("DESTINATION_PROJECT_NAME")


async def get_profile(sid) -> Union[Dict[str, Any], Dict[str, Any]]:
    headers = {}
    headers["Cookie"] = f"connect.sid={sid}"
    url = f"https://scrapbox.io/api/users/me"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            return await response.json()


async def import_pages(project: str, data: Dict[str, Any], init: Dict[str, Any]) -> requests.Response:
    if len(data["pages"]) == 0:
        return "No pages to import."

    sid = init["sid"]
    csrf = init.get("csrf", CSRF)
    # if not csrf:
    #     csrf = await get_csrf_token(sid)
    #     print("crsf", csrf)

    headers = {
        "Accept": "application/json, text/plain, */*",
        "X-CSRF-TOKEN": csrf
    }
    if sid:
        headers["Cookie"] = f"connect.sid={sid}"

    files = {
        "import-file": ("import-file", json.dumps(data), "application/octet-stream"),
        "name": (None, "undefined")
    }

    url = f"https://scrapbox.io/api/page-data/import/{project}.json"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=files) as res:
            res.raise_for_status()
            return res


async def get_csrf_token(sid) -> str:
    user = await get_profile(sid)
    return user["csrfToken"]


async def main():
    with open("data_en.json", "r") as file:
        data = json.load(file)

    importing_pages = data["pages"]

    if len(importing_pages) == 0:
        print("No page to be imported found.")
    else:
        print(
            f"Importing {len(importing_pages)} pages to '/{PROJECT_NAME}'...")

        result = await import_pages(
            PROJECT_NAME,
            {
                "pages": importing_pages,
            },
            {
                "sid": SID,
            }
        )
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
