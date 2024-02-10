import requests
import bs4
import time
import fake_useragent
import json
import lxml

def get_link(text):
    ua = fake_useragent.UserAgent()
    data = requests.get(url=f"https://chelyabinsk.hh.ru/search/vacancy?text"
                            f"={text}&from=suggest_post&salary=&ored_clusters=true&area=104&page=1",
                        headers={"user-agent": ua.random}
                        )
    l_data = []
    if data.status_code != 200:
        return
    soup = bs4.BeautifulSoup(data.content, "lxml")
    # ищем кол-во страниц
    try:
        page_count = int((soup.find("div", attrs={"class": "pager"})
                         .find_all("span", recursive=False)[-1]
                         .find("span", recursive=False)).text)
    except:
        page_count = 1

    # ищем все ссылки (кроме топ работадателей, т.к. div-name разный)
    for page in range(page_count):
        try:
            data = requests.get(url=f"https://chelyabinsk.hh.ru/search/vacancy?text"
                                    f"={text}&from=suggest_post&salary=&ored_clusters=true&area=104&page={page}",
                                headers={"user-agent": ua.random}
                                )
            if data.status_code != 200:
                return "Can't connect to the site (search all vacancy)"
            soup = bs4.BeautifulSoup(data.content, "lxml")
            b = (soup.find("div", attrs={'data-qa':"vacancy-serp__results", "id": "a11y-main-content"})
                 .find_all("div", attrs={"class":"serp-item serp-item_link"}))
            for vacancy in b:
                yield vacancy.find('a').attrs["href"]
        except Exception as e:
            return f"ERROR: {e} block1"
        print(f"page {page + 1} ^^^")
        time.sleep(1)

    # ищем ссылки на топ-работодателей
    for page in range(page_count):
        try:
            data = requests.get(url=f"https://chelyabinsk.hh.ru/search/vacancy?text"
                                    f"={text}&from=suggest_post&salary=&ored_clusters=true&area=104&page={page}",
                                headers={"user-agent": ua.random}
                                )
            if data.status_code != 200:
                return "Can't connect to the site"
            soup = bs4.BeautifulSoup(data.content, "lxml")

            b = (soup.find("div", attrs={'data-qa': "vacancy-serp__results", "id": "a11y-main-content"})
                 .find_all("div", class_="serp-item vacancy-serp-item_clickme serp-item_link"))
            for vacancy in b:
                yield vacancy.find('a').attrs["href"]
        except Exception as e:
            return f"ERROR: {e} block2"
        print(f"page {page + 1} ^^^")
        time.sleep(1)

def get_vacancy_data(link):
    pass

if __name__ == "__main__":
    for link in get_link(""):
        print(link)

