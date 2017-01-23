import sys

from grab import Grab
from grab import error

global_write_counter = 0

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = 'https://www.topdesignfirms.com/directory'


def grubs(obj, url):
    result = []
    obj.go(url)
    for rec in g.css_list('div.state-listing li a'):
        result.append([rec.values()[0]])
    return result


def parse(obj, url):
    name = address = phone = website = None
    result = []
    obj.go(url)
    for rec in g.css_list('div.city-listning-content'):
        try:
            # ------- NAME -------
            name = rec[0][0].text.replace('\r\n', '')
            # ------- ADDRESS --------
            address = '%s  %s' % (rec[1][0][1][0].text, rec[1][0][0].text)
            # ------- PHONE -------
            phone = rec[1][2].text
            # ------- WEBSITE -------
            website = rec[4].text
        except IndexError:
            print rec.text
        result.append([name, address, phone, website])
    return result


def knocker(obj, url):
    result = url
    obj.go(url)
    try:
        if obj.css('ul.paging')[-1][0].tag == 'a':
            result = obj.css('ul.paging')[-1][0].values()[0]
    except error.DataNotFound:
        return result
    return result


def recursive_parse(obj, url):
    include_url = knocker(obj, url)
    if include_url != url:
        recursive_parse(obj, include_url)
    lst = parse(g, url)
    write_func(lst)


def write_func(lst):
    with open('result_topdesignfirms_com0.csv', 'a') as fl:
        global global_write_counter
        for i in lst:
            global_write_counter += 1
            print('%s;%s;%s;%s;%s\n' % (global_write_counter, i[0], i[1], i[2], i[3]))
            common = '%s;%s;%s;%s;%s\n' % (global_write_counter, i[0], i[1], i[2], i[3])
            fl.write(common.encode('ascii', "ignore"))


if __name__ == '__main__':
    g = Grab()
    tmp = grubs(g, url)

    good_urls_list = []
    counter = 0
    for item in tmp:
        counter += 1
        if item[0].find('usa') > 0:
            for city in grubs(g, item[0]):
                counter += 1
                good_urls_list.append(city[0])
        else:
            good_urls_list.append(item[0])

    for good_url in good_urls_list:
        recursive_parse(g, good_url)
