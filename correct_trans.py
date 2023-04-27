import json


def correct(bad, good=None):
    # if good is None, just print

    if bad in cache[key]:
        print(key, cache[key])
        if good is not None:
            # replace
            cache[key] = cache[key].replace(bad, good)


cache = json.load(open("cache.json", "r"))
for key in cache:
    correct("Yasukazu Nishio", "NISHIO Hirokazu")
    correct("reader is you", "reader is myself")
    correct(
        "Polis Experience Report: Do you want to investigate the causes of terrorism?",
        "Polis Experience Report: Should we investigate the causes of terrorism?")
    correct("deliberative", "deliberation")
# write back
json.dump(cache, open("cache.json", "w"), ensure_ascii=False, indent=2)
