import json
cache = json.load(open("cache.json", "r"))
for key in cache:
    if "Yasukazu Nishio" in cache[key]:
        print(key, cache[key])
        # replace
        cache[key] = cache[key].replace("Yasukazu Nishio", "NISHIO Hirokazu")

# write back
json.dump(cache, open("cache.json", "w"), ensure_ascii=False, indent=2)
