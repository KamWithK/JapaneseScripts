import json
import scrapy

from utils import get_word
from scrapy.crawler import CrawlerProcess

URL = "https://jpdb.io/novel/5495/kaji-bannou-no-ore-ga-kokou-no-bishoujo-wo-asa-kara-yoru-made-osewasuru-koto-ni-natta-hanashi/vocabulary-list"
WORD_LIST_PATH = "data/Migaku_Word_List_ja_2022_1_16.json"
FREQUENCY_LIST_PATH = "data/Migaku SoL Top 100 frequency.json"
SAVE_PATH = "outputs/kaji-bannou-no-ore-ga-kokou-no-bishoujo-wo-asa-kara-yoru-made-osewasuru-koto-ni-natta-hanashi.txt"
FREQUENCY_LIMIT = 5000

vocab = []

with open(WORD_LIST_PATH, encoding="utf-8-sig") as word_list_file:
    word_list = map(get_word, json.load(word_list_file))

with open(FREQUENCY_LIST_PATH, encoding="utf-8-sig") as frequency_file:
    frequency_list = map(get_word, json.load(frequency_file)[:FREQUENCY_LIMIT])

class JPDBSpider(scrapy.Spider):
    name = "jpdb"

    def start_requests(self):
        yield scrapy.Request(url=URL, callback=self.start_parse)
    
    def start_parse(self, response):
        entry_count = int(response.css(".container > p").re(r"(?<=from ).*(?= entries)")[0])

        for page in range(0, entry_count + 50, 50):
            yield response.follow(
                response.url + ("&" if "?" in response.url else "?") + f"offset={page}#a",
                callback=self.parse
            )

    def parse(self, response):
        global vocab

        vocab += response.css("div.entry > div > div > a::attr(href)").re(r"(?<=[0-9]\/).*(?=#)")
        next_page = response.xpath("//*[text() = 'Next page']/@href").get()

process = CrawlerProcess()
process.crawl(JPDBSpider)
process.start() # blocking

with open(SAVE_PATH, "w", encoding="utf-8") as file:
    file.write("\n".join(set.intersection(set(vocab) - set(word_list), set(frequency_list))))
