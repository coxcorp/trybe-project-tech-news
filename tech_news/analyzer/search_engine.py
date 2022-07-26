from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    news_list = list()

    for news in search_news({"title": {"$regex": title, "$options": "i"}}):
        news_list.append((news["title"], news["url"]))

    return news_list


# Requisito 7
def search_by_date(date):
    try:
    date = datetime.strptime(date, "%Y-%m-%d")
    news_list = list()
    for news in search_news({"timestamp": date.strftime("%d/%m/%Y")}):
        news_list.append((news["title"], news["url"]))
    return news_list

    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_tag(tag):
    news_list = list()

    for news in search_news({"tags": {"$regex": tag, "$options": "i"}}):
        news_list.append((news["title"], news["url"]))

    return news_list


# Requisito 9
def search_by_category(category):
    news_list = list()

    for news in search_news(
        {"category": {"$regex": category, "$options": "i"}}
    ):
        news_list.append((news["title"], news["url"]))

    return news_list
