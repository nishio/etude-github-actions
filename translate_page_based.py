import concurrent.futures
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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FOOTER = """
This page is auto-translated from [/nishio/{ja_title}] using DeepL.
 If you looks something interesting but the auto-translated English is not good enough to understand it,
 feel free to let me know at [@nishio_en https://twitter.com/nishio_en].
 I'm very happy to spread my thought to non-Japanese readers.
""".replace(
    "\n", ""
)


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


def call_openai(ja):
    """
    OpenAI GPT APIを使用して翻訳を行う関数
    """
    import openai
    openai.api_key = OPENAI_API_KEY
    
    system_prompt = """
    あなたは日本語から英語への翻訳者です。提供された日本語のテキストを英語に翻訳してください。
    注意点：
    1. Scrapboxの角かっこ記法 [...]（リンク記法）はそのまま保持してください
    2. 技術的な専門用語は適切に翻訳してください
    3. 自然で読みやすい英語に翻訳してください
    4. 元の文章のニュアンスと意図を保持してください
    """
    
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"以下の日本語テキストを英語に翻訳してください：\n\n{ja}"}
                ],
                temperature=0.3,
            )
            break
        except Exception as e:
            print(e)
            sleep(60)
            continue
    
    return response.choices[0].message.content.strip()


def generate_line(text):
    return {
        "text": text,
        "created": 946652400,  # 2000-01-01 00:00:00
        "updated": 946652400,
        "userId": "582e63d27c56960011aff09e",  # nishio
    }


def translate_links(text):
    global cache
    keywords = re.findall(r"\[(.*?)\]", text)
    for k in keywords:
        en = cache.get(k)
        if en:  # translation exists
            text = text.replace(f"[{k}]", f" [{en}] ")
    return text


def to_english(text):
    global is_updated, total, no_cache
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


def group_lines_into_paragraphs(lines):
    """
    インデントレベルが同じ連続した行をグループ化して段落として扱う関数
    """
    paragraphs = []
    current_paragraph = []
    current_indent = None
    
    for line in lines:
        text = line["text"]
        indent_match = re.match(r'^(\s*)', text)
        indent = indent_match.group(1) if indent_match else ""
        
        if "[en.icon]" in text or "[enjabelow.icon]" in text:
            if current_paragraph:
                paragraphs.append(current_paragraph)
                current_paragraph = []
            paragraphs.append([line])
            current_indent = None
            continue
            
        if not text.strip() or (current_indent is not None and indent != current_indent):
            if current_paragraph:
                paragraphs.append(current_paragraph)
                current_paragraph = []
            current_indent = indent
        
        current_paragraph.append(line)
    
    if current_paragraph:
        paragraphs.append(current_paragraph)
        
    return paragraphs


def preprocess_scrapbox_notation(text):
    """
    Scrapbox記法を翻訳前に一時的にマークする関数
    """
    def replace_link(match):
        link_text = match.group(1)
        return f"__SCRAPBOX_LINK_START__{link_text}__SCRAPBOX_LINK_END__"
    
    processed_text = re.sub(r'\[(.*?)\]', replace_link, text)
    return processed_text


def postprocess_scrapbox_notation(text):
    """
    一時的にマークされたScrapbox記法を元に戻す関数
    """
    def restore_link(match):
        link_text = match.group(1)
        return f"[{link_text}]"
    
    processed_text = re.sub(r'__SCRAPBOX_LINK_START__(.*?)__SCRAPBOX_LINK_END__', restore_link, text)
    return processed_text


def translate_one_page_paragraph_based(page):
    for line in page["lines"]:
        if "[en.icon]" in line["text"]:
            return False
            
    is_updated = False
    ja_title = page["title"]
    en_title = to_english(ja_title)
    
    use_chatgpt = False
    for line in page["lines"]:
        if "[priority.icon]" in line["text"] or "[important.icon]" in line["text"]:
            use_chatgpt = True
            break
            
    page["title"] = en_title
    
    paragraphs = group_lines_into_paragraphs(page["lines"])
    
    for paragraph_idx, paragraph in enumerate(paragraphs):
        paragraph_text = "\n".join([line["text"] for line in paragraph])
        
        preprocessed_text = preprocess_scrapbox_notation(paragraph_text)
        
        if use_chatgpt and len(paragraph) > 1:  # 段落が複数行の場合のみChatGPTを使用
            translated_text = call_openai(preprocessed_text)
        else:
            translated_text = call_deepl(preprocessed_text)
        
        postprocessed_text = postprocess_scrapbox_notation(translated_text)
        
        translated_lines = postprocessed_text.split("\n")
        
        for i, translated_line in enumerate(translated_lines):
            if i < len(paragraph):
                paragraph[i]["text"] = translated_line
    
    page["lines"].extend(
        [
            generate_line("---"),
            generate_line(FOOTER.format(ja_title=ja_title)),
        ]
    )
    
    return is_updated


def translate_pages_paragraph_based(pages):
    global total, no_cache, cache
    total = 0
    no_cache = 0
    cache_data = "./cache_paragraph.json"
    if os.path.exists(cache_data):
        cache = json.load(open(cache_data, "r"))
    else:
        cache = {}
    print("cache length:", len(cache))

    for page in tqdm(pages):
        is_updated = translate_one_page_paragraph_based(page)  # update destructively
        if is_updated:  # currently it is always False
            with open(cache_data, "w") as file:
                json.dump(cache, file, ensure_ascii=False, indent=2)

    with open(cache_data, "w") as file:
        json.dump(cache, file, ensure_ascii=False, indent=2)

    print("total", total, "no_cache", no_cache, "ratio", no_cache / total)


def translate_from_json_to_json_paragraph_based():
    start_time = perf_counter()
    in_file = "./data.json"
    data = json.load(open(in_file, "r"))

    pages = list(sorted(data["pages"], key=lambda x: x["updated"], reverse=True))

    translate_pages_paragraph_based(pages)  # update pages(and data) destructively
    json.dump(data, open("./data_en_paragraph.json", "w"), ensure_ascii=False, indent=2)
    print("translate:", perf_counter() - start_time)


def main():
    translate_from_json_to_json_paragraph_based()


def local_trial_10pages():
    print("running local trial")
    in_file = "./data.json"
    data = json.load(open(in_file, "r"))

    pages = list(sorted(data["pages"], key=lambda x: x["updated"], reverse=True))[:10]
    data["pages"] = pages  # to omit other pages

    translate_pages_paragraph_based(pages)  # update pages(and data) destructively
    json.dump(data, open("./data_en_paragraph_local.json", "w"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    if os.environ.get("GITHUB_ACTIONS") == "true":
        main()
    else:
        print("Not running within a GitHub Actions environment")
        main()
