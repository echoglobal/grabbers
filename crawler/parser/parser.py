# -*- coding: utf-8 -*-
# !/usr/bin/env python


import csv
from urllib.request import urlopen

from lxml.etree import XMLSyntaxError
from lxml.html import fromstring

URL = 'http://www.topinteractiveagencies.com/'
ITEM_PATH = '.sf-menu .menu-item-has-children'
COMPANY_PATH = '.articlecontainer .indextitle'
INFO_PATH = '.blogcontent'
PAGE_PATH = '.pagination'


def main():
    f = urlopen(URL)
    list_html = f.read().decode('utf-8', errors='ignore')
    list_doc = fromstring(list_html)

    for elem in list_doc.cssselect(ITEM_PATH):
        a = elem.cssselect('a')[0]
        href = a.get('href')
        current_page = pagination(href) + 1

        for i in range(1, current_page):
            new_href = href + 'page/' + str(i) + '/'
            details_html = urlopen(new_href).read().decode('utf-8', errors='ignore')
            try:
                details_doc = fromstring(details_html)
            except XMLSyntaxError:
                continue
            for company_elem in details_doc.cssselect(COMPANY_PATH):
                _a = company_elem.cssselect('a')[0]
                company_link = _a.get('href')
                name = _a.text

                info_list = get_info(company_link)
                project = {
                    'name': name,
                    'link': company_link,
                    'info': info_list
                }
                save(project, 'companies_info.csv')


def save(project, path):
    with open(path, 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('Название', 'Ссылка', 'Информация'))
        writer.writerow((project['name'], project['link'], ', '.join(project['info'])))


def get_info(company_link):
    company_info_html = urlopen(company_link).read().decode('utf-8', errors='ignore')
    company_info_doc = fromstring(company_info_html)
    info_elements = company_info_doc.xpath('.//div[@class="blogcontent"]/p')
    info_list = [info_elem.text_content() for info_elem in info_elements]
    return info_list


def pagination(href):
    details_html = urlopen(href).read().decode('utf-8', errors='ignore')
    details_doc = fromstring(details_html)
    num = details_doc.cssselect(PAGE_PATH)[0].cssselect('a')[2].text
    if num == 'Next »':
        num = details_doc.cssselect(PAGE_PATH)[0].cssselect('a')[1].text
    else:
        return int(num)

    return int(num)


if __name__ == '__main__':
    main()
