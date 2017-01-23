import re

from grab import Grab

global_url = 'http://www.designfirms.org'
url_base = 'http://www.designfirms.org/directory/location'

re_template_0 = r"<a class='nul b' style='font-size: 12pt;' href='(.*?)'>(.*?)</a>"
re_template_1 = r"Results | Page \(\d{1,3}\) of \((\d{1,3})\)"


def all_out(url):
    res_dict = {}
    obj = Grab()
    obj.go(url)
    lst = obj.css_list('a.b')[:51]  # numb of states
    for i in lst:
        res_dict[i.text] = i.values()[2]
    return res_dict


def all_out_old(url):
    obj = Grab()
    resp = obj.go(url)
    return resp.body.split('\n')


def handle_state_page(data_dict, tmplt):
    big_firm_list = []
    obj = Grab()
    ipg = Grab()
    cnt = 0
    for i in data_dict:
        cnt += 1
        obj.go(global_url + data_dict[i])
        numb_of_page = int(re.findall(tmplt, obj.css_text('h4'))[1])  # get numb of pages
        big_firm_list += [elem.values()[0] for elem in obj.css_list('div.tl a')[4:]]
        for j in range(2, numb_of_page + 1):
            url_loc = global_url + data_dict[i] + 'p.' + str(j)
            ipg.go(url_loc)
            big_firm_list += [elem.values()[0] for elem in ipg.css_list('div.tl a')[4:]]
    return big_firm_list


def final_parce(urls):
    glob_data_list = []
    g = Grab()
    cnt = 0
    for one_site in urls:
        cnt += 1
        g.go(global_url + one_site)
        name = location = phone = site = facebook = twitter = listed = founded = None
        try:
            # name
            if type(g.css_list('title')[0].text) == type(''):
                name = g.css_list('title')[0].text.replace(' is on DesignFirms', '')

            # phone
            for v in [h.text for h in g.css_list('div.column p')]:
                if v and re.match(r'^\(\d\d\d\).+', v):
                    phone = v

            # web-site
            if [t.values() for t in g.css_list('p a.nul')][2][0] == '_blank':
                site = [t.values() for t in g.css_list('p a.nul')][2][4]

            # location
            sity = [t.text for t in g.css_list('p a.nul')][0]
            state = [t.text for t in g.css_list('p a.nul')][1]
            location = sity + ' ' + state

            # twitter facebook
            for d in [k.values() for k in g.css_list('a.nul')]:
                if d[0] == 'nofollow' and 'insert_click' in d[3]:
                    if 'facebook' in d[4]:
                        facebook = d[4]
                    elif 'twitter' in d[4]:
                        twitter = d[4]

            # listed
            listed = [h.text for h in g.css_list('div.col')][-1]
            if 'Year Founded:' in [h.text for h in g.css_list('div.col')]:
                founded = [h.text for h in g.css_list('div.col')][3]
        except IndexError:
            print('index error')
        except Exception as e:
            print('Somesing else ALARM!!')
            print(e.message)

        glob_data_list.append([name, location, phone, site, facebook, twitter, founded, listed])
    return glob_data_list


if __name__ == '__main__':
    tmp = []
    with open('local_sites_designfirms_org.csv') as fl:
        for lin in fl.readlines():
            tmp.append(lin.split(';')[1].replace('\n', ''))
    counter = 0
    result = final_parce(tmp)
    with open('result_designfirms_org.csv', 'a') as fl:
        for item in result:
            counter += 1
            common = '%s;%s;%s;%s;%s;%s;%s;%s;%s\n' % (
                counter, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7])
            print(common)

            fl.write(common.encode('ascii', "ignore"))
