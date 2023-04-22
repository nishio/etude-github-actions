import requests

API = "https://scrapbox.io/api/pages/nishio/search/titles"
EXTRA = "?followingId={id}"

keywords = set()


def get(last_id=None):
    if last_id is None:
        url = API
    else:
        url = API + EXTRA.format(id=last_id)
    data = requests.get(url).json()
    for page in data:
        last_id = page["id"]
        keywords.update(page["links"])

    return last_id

# get()

#  json.dump(list(keywords), open("keywords.json", "w"), ensure_ascii=False)
