import re

from grab import Grab

params = {
    'Advertising': ('Companies', 'Agencies', 'Design Studios'),
    'Digital Design': ('Companies', 'Consultancies', 'Design Studious'),
    'Web Design': ('Companies', 'Consultancies', 'Design Studious'),
    'Interface Design': ('Companies', 'Consultancies', 'Design Studious')
}


def first(obj, url='https://www.dexigner.com/directory/'):
    '''for parsing first page for categories'''
    result = []
    obj.go(url)

    for item in g.css_list('a.catlink'):
        if item.text in [pk for pk in params.keys()]:
            result.append([item.text, item.values()[0]])
    return result


def second(obj, urls_list, basic_url='https://www.dexigner.com'):
    '''second: for parse categories --> types '''
    result = []
    for u in urls_list:
        obj.go(basic_url + u[1])
        for item in obj.css_list('a.catlink'):
            if item.text in params[u[0]]:
                result.append(item.values()[0])
    return result


def third(obj, urls_list, basic_url='https://www.dexigner.com'):
    '''third: parsing directly firms url_s'''
    result = []
    for u in urls_list:
        obj.go(basic_url + u)
        for item in obj.css_list('div.item h3 a'):
            result.append([item.text, item.values()[0]])
    return result


def extreme(obj, urls_list, basic_url='https://www.dexigner.com'):
    result = []
    counter = 0
    for u in urls_list:
        counter += 1
        sht = obj.go(basic_url + u[1])

        # ------- NAME -------
        name = obj.css_list('article h1')[0].text

        # ------- WEBSITE -------
        website = obj.css_list('#linkurl')[0].values()[0]

        # ------- CATEGORY -------
        category = obj.css_list('#category')[0].text

        # ------- TEL -------
        try:
            tel = obj.css_list('#telephone span')[0].text
        except IndexError:
            print(counter, 'Index Error: telephone ', u[0], basic_url + u[1])

        # ------- FULL_ADDRESS -------
        try:
            full_address = obj.css('#location').text_content().replace('\r\n', ' ')
        except IndexError:
            print(counter, 'Index Error: full_adress ', u[0], basic_url + u[1])

        # ------- COUNTRY -------
        try:
            country = re.findall(r'.+[\d\d\d|\s\d\w\w](.+)$', obj.css('#location').text_content())[0]
            country = re.findall('"addressCountry":"(.+?)"},"', sht.body)[0]
        except IndexError:
            print('!!!', counter, 'Index Error: country ', u[0], basic_url + u[1])

        # ------- UPDATED -------
        updated = obj.css('footer.detailnew span.small time').text

        print(counter, name, website, category, tel, full_address, country, updated, basic_url + u[1])
        result.append([name, website, category, tel, full_address, country, updated])
    return result


if __name__ == '__main__':
    g = Grab()
    tmp = first(g)
    tmp = second(g, tmp)
    tmp = third(g, tmp)
    tmp = extreme(g, tmp)
    counter = 0

    with open('result_designer_com1.csv', 'a') as fl:
        for i in tmp:
            counter += 1
            common = '%s;%s;%s;%s;%s;%s;%s;%s\n' % (counter, i[0], i[1], i[2], i[3], i[4], i[5], i[6])
            fl.write(common.encode('ascii', "ignore"))
