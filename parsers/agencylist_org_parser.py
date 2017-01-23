import re

from grab import Grab

url_base = 'http://agencylist.org/'

re_template_0 = r'<p>(<strong>)?<a'
re_template_1 = r'<div class="listHead1"><h2 class="h2 txtstyle light color3">(.*?)</h2></div>'


def all_out(url_in):
    obj = Grab()
    resp = obj.go(url_in)
    return resp.body.split('\n')


def out_link_filter(o_list, template):
    res_lst = []
    for sng in o_list:
        if len(re.findall(template, sng)) > 0:
            res_lst.append(sng)
    return res_lst


def handle_out_city(lst):
    tmp = {}
    for one_str in lst:
        link = re.findall(r'href="/(.*)"\sdata-wpel', one_str)
        city = re.findall(r'"internal">(.*)</a', one_str)
        if len(city[0]) and len(link[0]):
            tmp[city[0]] = link[0]
    return tmp


def handle_out_category(city_dict):
    result_list = []
    for city in city_dict:
        all_city_data_list = all_out(url_base + city_dict[city])
        for cnt in range(len(all_city_data_list)):
            category = re.findall(re_template_1, all_city_data_list[cnt])
            if category:
                all_items_list = re.findall(
                    r'<a href="(.*?)" target="_blank" rel="nofollow" data-wpel-link="external">(.*?)</a>',
                    all_city_data_list[cnt + 1])
                for item in all_items_list:
                    result_list.append([category[0], item[1], item[0], city])
    return result_list


if __name__ == '__main__':
    raw_out = all_out(url_base)
    out_link_list = out_link_filter(raw_out, re_template_0)
    city_list = handle_out_city(out_link_list)
    result = handle_out_category(city_list)
    counter = 0
    with open('result_agencylist_org.csv', 'wb') as fl:
        for i in result:
            counter += 1
            print('%s;%s;%s;%s;%s\n' % (counter, i[0], i[1], i[2], i[3]))
            fl.write('%s;%s;%s;%s;%s\n' % (counter, i[0], i[1], i[2], i[3]))
