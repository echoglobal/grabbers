from grab import Grab


def scrap_company(url):
    """
    Collect addition information about company.
    :param url:
    :return list of attr.
    """
    company = Grab(timeout=10, connect_timeout=10)
    company.go(url)
    name = company.doc.select('//div[@itemprop="name"]').text().split(',')
    name = " ".join(name)
    try:
        rating = company.doc.select('//span[@class="default micro-green-btn ratingfive"]').text()
        rating = rating.split('/')[0]
    except BaseException:
        rating = str(0)

    try:
        site = company.doc.select('//a[@class="green-btn visit-website block"]/@href').text()
    except BaseException:
        site = ""

    try:
        fc = company.doc.select('//a[@class="light-fa-facebook"]/@href').text()
    except BaseException:
        fc = ""

    try:
        tw = company.doc.select('//a[@class="light-fa-twitter"]/@href').text()
    except BaseException:
        tw = ""

    try:
        ln = company.doc.select('//a[@class="light-fa-linkedin"]/@href').text()
    except BaseException:
        ln = ""

    service = company.doc.select('//div[@class="nofollow tagc clear"]').text()
    service = " ".join(service.split(','))
    return [name, rating, fc, tw, ln, site, service]


def get_scrap(url):
    """
    Get link on companies category.
    Running on a list of companies and collect information about each.
    :param url:
    :return csv file with all companies in this category.
    """
    g = Grab(timeout=10, connect_timeout=10)
    g.go(url)
    f_name = url.split('/')[-1]
    pages = g.doc.select('//ul[@class="pagination"]//a/@href')[-1].text()  # for list iteration
    pages = pages.split(':')[1]
    url += '/page:'
    page_numbers = 1
    with open(f_name + '.csv', 'w+', newline="\n") as file:
        while page_numbers <= int(pages):
            g.go(url + str(page_numbers))
            companies = g.xpath_list('//div[@class="company-info"]')
            for i in range(len(companies)):
                loc = g.doc.select('//ul[@class="company_overview"]')[i].text()
                loc = loc.split('hr')[1]
                loc = loc.split(',')
                loc = " ".join(loc)
                if "Featured" in loc:
                    loc = str(loc.split('F')[0]).split(',')
                    loc = " ".join(loc)
                rate = g.doc.select('//ul[@class="company_overview"]')[i].text()
                rate = rate.split('/')[0].split(',')
                rate = " ".join(rate)
                new_url = 'https://www.goodfirms.co'
                link = g.doc.select('//a[@class="font18 weight700"]/@href')[i].text()
                id = g.doc.select('//a[@class="font18 weight700"]/@href')[i].text().split('/')[3]
                new_url += link
                info = scrap_company(new_url)
                name, rating, fc, tw, ln, site, service = info
                about = '{}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n'.format(id, name, rating, fc, tw, ln,
                                                                          site, rate, loc, service)
                file.write(about)
            page_numbers += 1
    return


if __name__ == "__main__":
    get_scrap("https://www.goodfirms.co/directory/platform/app-development")
    get_scrap("https://www.goodfirms.co/directory/languages/top-software-development-companies")
    get_scrap("https://www.goodfirms.co/directory/cms/top-website-development-companies")
    get_scrap("https://www.goodfirms.co/directory/platforms/ecommerce-web-development-companies")
    get_scrap("https://www.goodfirms.co/directory/platforms/top-cloud-computing-companies")
    get_scrap("https://www.goodfirms.co/directory/marketing-services/top-digital-marketing-companies")
    get_scrap("https://www.goodfirms.co/directory/platforms/mobile-app-design-companies")
    get_scrap("https://www.goodfirms.co/directory/platforms/top-web-design-companies")
    get_scrap("https://www.goodfirms.co/directory/services/top-mobile-app-testing-companies")
