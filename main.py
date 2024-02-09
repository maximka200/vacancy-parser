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
    if data.status_code != 200:
        return

    soup = bs4.BeautifulSoup(data.content, "lxml")
    try:
        page_count = (soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").text)
    except:
        return
    print(soup)

    print(data.text)


def get_resume_data(link):
    pass

if __name__ == "__main__":
    get_link("Javascript")

