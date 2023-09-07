import requests
from fake_headers import Headers
import bs4
import json
import re


if __name__ == "__main__":
    headers = Headers(browser="firefox", os="win")
    headers_data = headers.generate()

    hh_html = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=headers_data).text
    hh_soup = bs4.BeautifulSoup(hh_html, "lxml")

    offers_list = hh_soup.find('div', id='a11y-main-content')
    offers = offers_list.find_all("div", class_="vacancy-serp-item__layout")

    offers_info = []

    for offer in offers:
        a_tag = offer.find("a", class_="serp-item__title")
        link = a_tag["href"]

        sal_fork_tag = offer.find("span", class_="bloko-header-section-2")
        if sal_fork_tag:
            sal_fork = re.sub(r" ", r" ", sal_fork_tag.text)
        else:
            sal_fork = "None"

        company_and_city_tag = offer.find("div", class_="vacancy-serp-item-company")
        company_and_city = company_and_city_tag.find_all("div", class_="bloko-text")
        company = company_and_city[0].text
        city = company_and_city[1].text

        description_html = requests.get(link, headers=headers.generate()).text
        description_soup = bs4.BeautifulSoup(description_html, "lxml")

        description_text = description_soup.find("div", class_="g-user-content").text

        if "django" in description_text.lower() and "flask" in description_text.lower():
            offers_info.append({
                "link": link,
                "salary fork": sal_fork,
                "company name": company,
                "city": city
            })

    print(len(offers_info))
    with open('offers_info.json', 'w', encoding='utf-8') as f:
        json.dump(offers_info, f, ensure_ascii=False, indent=2)
