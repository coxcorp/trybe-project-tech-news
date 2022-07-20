import requests
import time
import parsel
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        response = requests.get(
            url, headers={"user-agent": "Fake user-agent"}, timeout=3
        )
        response.raise_for_status()
        time.sleep(1)
    except (requests.HTTPError, requests.ReadTimeout):
        return None
    return response.text


# Requisito 2
def scrape_novidades(html_content):
    selector = parsel.Selector(html_content)
    urls = selector.css(".entry-title a::attr(href)").getall()
    return urls


# Requisito 3
def scrape_next_page_link(html_content):
    selector = parsel.Selector(html_content)
    next = selector.css("a.next::attr(href)").get()
    return next


# Requisito 4
def scrape_noticia(html_content):
    selector = parsel.Selector(html_content)
    return {
        "url": selector.css('link[rel="canonical"]::attr(href)').get(),
        "title": selector.css("h1.entry-title::text").get(),
        "timestamp": selector.css("li.meta-date::text").get(),
        "writer": selector.css("span.author > a::text").get(),
        "comments_count": len(selector.css("ol.comment-list li").getall()),
        "summary": "".join(
            selector.css("div.entry-content p:nth-child(2) *::text").getall()
        ),
        "tags": selector.css('a[rel="tag"]::text').getall(),
        "category": selector.css("a > span.label::text").get(),
    }


# Requisito 5
def get_tech_news(amount):
    page_url = "https://blog.betrybe.com"
    tech_news = list()

    while len(tech_news) < amount:
        for url in scrape_novidades(fetch(page_url)):
            if len(tech_news) < amount:
                tech_news.append(scrape_noticia(fetch(url)))

        page_url = scrape_next_page_link(fetch(page_url))

    create_news(tech_news)

    return tech_news
