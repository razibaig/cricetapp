import urllib.request
import time
import scrapy
from scrapy.selector import Selector
import json
import requests

URLS = []


# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    time.sleep(0.5)
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


# Filter the links found in <a> tags
def filter_links(all_links):
    cleaned_links = []
    for i in range(len(all_links)):
        if "/content/player/" in all_links[i]:
            cleaned_links.append(all_links[i])
    return cleaned_links


# Populate the complete urls
def populate_urls(prefix_string, cleaned_links):
    for i in range(len(cleaned_links)):
        complete_url = prefix_string + cleaned_links[i]
        URLS.append(complete_url)


def main():

    source_page = 'http://www.espncricinfo.com/england/content/player/caps.html?'
    espn_url = 'http://www.espncricinfo.com'

    country = 1
    m_type = 1
    scrap_url = "{0}{1}{2}{3}{4}{5}".format(source_page, "country=", country, ";", "class=", m_type)
    print(scrap_url)

    f = urllib.request.urlopen(scrap_url)
    complete_html = f.read()
    # print(complete_html)

    all_found_links = Selector(text=complete_html).xpath('.//a/@href').extract()

    filtered_links = filter_links(all_found_links)

    # print(list(filtered_links))

    populate_urls(espn_url, filtered_links)


def parse_player(self, response):
    return scrapy.Request("http://www.example.com/some_page.html",
                          callback=self.print_json)


def print_json(self, response):
    self.logger.info("Visited %s", response.url)


if __name__ == "__main__":
    main()
