__author__ = 'Xun'

import urllib2
from bs4 import BeautifulSoup
import numpy
import unicodecsv

rawlinks = [
            'http://www.accuweather.com/en/bg/sofia/51097/july-weather/51097',
            'http://www.accuweather.com/en/br/sao-paulo/45881/july-weather/45881',
            'http://www.accuweather.com/en/ca/vancouver/v5y/july-weather/53286',
            'http://www.accuweather.com/en/cn/chongqing/102144/july-weather/102144',
            'http://www.accuweather.com/en/hr/zagreb/117910/july-weather/117910',
            'http://www.accuweather.com/en/et/addis-ababa/126831/july-weather/126831',
            'http://www.accuweather.com/en/eg/cairo/127164/july-weather/127164',
            'http://www.accuweather.com/en/gh/accra/178551/july-weather/178551',
            'http://www.accuweather.com/en/il/tel-aviv/215854/july-weather/215854',
            'http://www.accuweather.com/en/in/chennai/206671/july-weather/206671',
            'http://www.accuweather.com/en/np/kathmandu/241809/july-weather/241809',
            'http://www.accuweather.com/en/pk/karachi/261158/july-weather/261158',
            'http://www.accuweather.com/en/ru/moscow/294021/july-weather/294021',
            'http://www.accuweather.com/en/tw/taipei-city/315078/july-weather/315078',
            'http://www.accuweather.com/en/ua/odessa/325343/july-weather/325343',
            'http://www.accuweather.com/en/us/raleigh-nc/27601/july-weather/329823'
            ]


def getheader():
    url = urllib2.urlopen('http://www.accuweather.com/en/bg/sofia/51097/july-weather/51097')
    webdoc = url.read()
    tree = BeautifulSoup(webdoc)
    url.close()
    dates = tree.find_all('h3', class_='date')

    datedata = dict()
    i=0
    for days in dates:
        datedata[i] = days.getText()
        i=i+1

    outputdate = datedata.values()

    outputheader = range(33)
    outputheader[0] = 'City'
    outputheader[1:32]=outputdate[3:34]
    outputheader[32] = 'Avg'
    return outputheader

def getcityweather(link):
    url=urllib2.urlopen(link)
    webdoc = url.read()
    tree = BeautifulSoup(webdoc)
    url.close()

    titlestring = tree.title.string
    city = titlestring[0:titlestring.find('July')-1]

    actual = tree.find_all('div', class_='actual')
    history = tree.find_all('div', class_='avg')
    if len(history) == 0:
        history = tree.find_all('div', class_='avg-main')

    actualdata = dict()
    historydata = dict()

    i=0
    for temps in actual:
        if len(actual) == 0:
            actualdata = []
        else:
            actualdata[i] = temps.find('span', class_='temp').getText()
            actualdata[i] = int(actualdata[i][:-1])
        i=i+1

    i=0
    for temps in history:
        historydata[i] = temps.find('span', class_='temp').getText()
        if historydata[i] == 'N/A':
            historydata[i] = 17
        else:
            historydata[i] = int(historydata[i][:-1])
        i=i+1

    difftemp = range(35)

    for i in range(0,35):
        if len(actualdata) == 0:
            difftemp[i] = 'N/A'
        else:
            difftemp[i] = actualdata[i]-historydata[i]

    outputdata = range(33)

    outputdata[0] = city
    outputdata[1:32] = difftemp[3:34]
    if len(actualdata) == 0:
        outputdata[32] = 'N/A'
    else:
        outputdata[32] = "{0:.2f}".format(numpy.average(difftemp[3:34]))

    return outputdata


header=getheader()
with open('temp.csv', 'wb') as f:
    fwriter = unicodecsv.writer(f, encoding='utf-8')
    fwriter.writerow(header)
f.close()

for link in rawlinks:
    inputentry = getcityweather(link)
    with open('temp.csv', 'ab') as f:
        fwriter = unicodecsv.writer(f, encoding='utf-8')
        fwriter.writerow(inputentry)
    f.close()
