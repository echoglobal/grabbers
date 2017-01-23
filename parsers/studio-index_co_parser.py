import re

# only copy site 'http://studio-index.co' body  by hand


with open('studio-index.http', 'r') as fl:  # http://studio-index.co
    text = fl.read()

template = r'<span class="col-1 ng-binding" ng-click="navScrollTo\(\$event\)">(.+?)</span>\W+?' + \
           '<span class="col-1 ng-binding">(.+?)</span>\W+?' + \
           '<span class="col-2 ng-binding">(.+?)</span>\W+?' + \
           '<span class="col-2"><a href="(.+?)" target="_blank"><span class="ng-binding">.+?</span></a></span>'

lst = re.findall(template, text)
counter = 0
with open('result_studio_index_cc.csv', 'a') as fl:
    for i in lst:
        counter += 1
        print('%s;%s;%s;%s;%s\n' % (counter, i[2], i[1], i[0], i[3]))
        fl.write('%s;%s;%s;%s;%s\n' % (counter, i[2], i[1], i[0], i[3]))
