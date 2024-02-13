import requests
import bs4
import time
import fake_useragent
import json
import lxml
import re

area_dict = {"chelyabinsk": "104", "sbp": "2"} #'' if all Russia
area = area_dict.get(input(), "")
ua = fake_useragent.UserAgent()
def get_link(text):
    global ua, area
    data = requests.get(url=f"https://hh.ru/search/vacancy?text"
                            f"={text}&from=suggest_post&salary=&ored_clusters=true&area={area}&page=1",
                        headers={"user-agent": ua.random}
                        )
    if data.status_code != 200:
        return "Can't connect to the site (search all vacancy)"
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
            data = requests.get(url=f"https://hh.ru/search/vacancy?text"
                                    f"={text}&from=suggest_post&salary=&ored_clusters=true&area={area}&page={page}",
                                headers={"user-agent": ua.random}
                                )
            if data.status_code != 200:
                return "Can't connect to the site (search all vacancy)"
            soup = bs4.BeautifulSoup(data.content, "lxml")
            b = (soup.find("div", attrs={'data-qa':"vacancy-serp__results", "id": "a11y-main-content"})
                 .find_all("div", attrs={"class":"serp-item serp-item_link"}))
            for vacancy in b:
                yield vacancy.find('a').attrs["href"].split("?")[0]
        except Exception as e:
            return f"ERROR: {e} block1"
        #time.sleep(1)

    # ищем ссылки на топ-работодателей
    for page in range(page_count):
        try:
            data = requests.get(url=f"https://hh.ru/search/vacancy?text"
                                    f"={text}&from=suggest_post&salary=&ored_clusters=true&area={area}&page={page}",
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
        #time.sleep(1)
def get_vacancy_data(link):
    global ua
    try:
        data = requests.get(url=link, headers={"user-agent": ua.random})
        if data.status_code != 200:
            return "Can't connect to the site"
        soup = bs4.BeautifulSoup(data.content, "lxml")
        #salary
        try:
            b = (soup.find("div", class_="vacancy-title").find("span", class_="bloko-header-section-2_lite"))
            string = re.sub("\xa0","", b.text)
            pattern = r"(\d+)"
            match = [float(i) for i in re.findall(pattern, string)]
            salary = sum(match) / len(match)
        except:
            salary = ""
        #experience
        try:
            b = (soup.find("p", class_="vacancy-description-list-item").find("span").text)
            if b == "3–6 лет":
                experience = "middle"
            elif b == "6 лет":
                experience = "senior"
            elif b == "не требуется":
                experience = "intern"
            else:
                experience = "junior"

        except:
            experience = ""
        #core skill
        try:
            core_skill = set()
            b = (soup.find("div", class_="bloko-tag-list").find_all("div", class_="bloko-tag"))
            for div in b:
                core_skill.add(div.find("span").text)

        except:
            core_skill = set()
        vacancy = {"salary": salary, "experience": experience, "core_skill": core_skill}

        return vacancy


    except Exception as e:
        return f"ERROR: {e} block3"




if __name__ == "__main__":
    pl_list = ["Java", "Python", "C#", "JavaScript", "C++", "Kotlin", "PHP", "Golang", "Perl", "Lua"]
    for pl in pl_list:
        pass
    for link in get_link(pl_list[1]):
            print(get_vacancy_data(link), link)





