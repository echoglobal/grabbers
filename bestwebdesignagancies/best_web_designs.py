import csv
import os

from grab import Grab
from grab import error


def scrap_company(link):
    """
        Take link on company info.
        Getting all  needed info about company.
        And return list of attrs.
    """

    g = Grab(timeout=5, connect_timeout=5)
    try:
        g.go(link)
    except error.GrabTimeoutError or error.GrabError as e:
        scrap_company(link)
    try:
        name = g.doc.select('//h1[@class="logo-text"]').text()
        web_site = g.doc.select('//a[@class="track-click"]/@href').text()
        person = g.doc.select('//span[@class="name"]').text()
        address = g.doc.select('//div[@class="em_prweek_address"]//p').text()
        address = address.split('Website')[0]
        phone = g.doc.select('//a[@class="btn-talk-2-rep"]').text()
        phone = phone.split('Representative')[1]
        founded = g.xpath_list('//ul[@class="list1"]//li//span')[1].text_content()
        employees = g.xpath_list('//ul[@class="list1"]//li//span')[2].text_content()
        service = g.xpath_list('//ul[@class="list2"]//li//span')[2].text_content()
        return [name, web_site, person, address, phone, founded, employees, service]
    except BaseException or AttributeError or TypeError as e:
        return 0


def run_by_companies_list(url):
    """
        Take companies list.
        And run by it.
    """

    fields = ["Id", "Company Name", "Website", "Person", "Position", "Address",
              "Phone", "Founded", "Employees", "Primary service"]
    name = url.split('/')[-1]

    g = Grab(timeout=5, connect_timeout=5)
    try:
        g.go(url)
        companies_links = g.xpath_list('//a[@class="more_info2"]/@href')
    except error.GrabTimeoutError or error.GrabError or BaseException as e:
        companies_links = []

    if companies_links:
        #  open output file
        with open(name + '.csv', 'a') as file:
            wr_f = csv.DictWriter(file, fieldnames=fields)
            wr_f.writeheader()

            #  start scrap companies
            for i, link in enumerate(companies_links):
                row_id = i + 1
                attrs = scrap_company(link)
                if attrs:
                    name, web_site, person, address, phone, founded, employees, service = attrs
                    position = row_id
                    wr_f.writerow({"Id": row_id, "Company Name": name, "Website": web_site, "Person": person,
                                   "Position": position, "Address": address, "Phone": phone,
                                   "Founded": founded, "Employees": employees, "Primary service": service})


def run_by_categories(url, dir_name):
    """
        Take categories list.
         And run run by it.
    """

    g = Grab(timeout=5, connect_timeout=5)
    try:
        g.go(url)
    except error.GrabTimeoutError or error.GrabError as e:
        run_by_categories(url, dir_name)

    # go to the country folder
    os.chdir(dir_name)

    categories = g.xpath_list('//div[@class="bluebox_services"]//a/@href')
    try:
        categories.remove('#;')
    except ValueError as e:
        pass
    for category in categories:
        run_by_companies_list(category)

    # exit from country folder
    os.chdir('..')


def rm_dir(name):
    """
     Checking if exist dir. If so remove.
    """
    for root, dirs, files in os.walk(name, topdown=False):
        for n in files:
            os.remove(os.path.join(root, n))
    os.rmdir(name)


if __name__ == '__main__':

    g = Grab(timeout=5, connect_timeout=5)
    g.go('http://www.bestwebdesignagencies.com')

    #  geting countries list
    countries = g.xpath_list('//div[@class="edition_box floatleft"]//a/@href')
    countries.remove('#')

    #  run it
    for iter_num, country in enumerate(countries):
        country_name = country.split('/')[-1].split('-')[-1]
        if iter_num == len(countries) - 1:
            country_name = 'usa'
        if country_name in os.listdir():
            rm_dir(country_name)
        os.mkdir(country_name)
        run_by_categories(country, country_name)
