#coding=utf8

import requests
import time
import json
import csv
import re
from lxml import etree
import threading

class Scan58():
    def __init__(self):
        self.url = 'http://wuxi.58.com/chuzu/pn%s/'
        self.fd = open('data.csv', 'wb')

    @classmethod
    def getJson(cls, html):
        m = re.findall(r'____json4fe = (.+);', html)
        if len(m) < 2:
            return False
        else:
            return json.loads(m[1])

    def run(self):
        page = 1
        try:
            csv_writer = csv.writer(self.fd, delimiter=',')
            while True:
                print 'start crawling page %s' % page
                r = requests.get(self.url % page, timeout=10)
                root = etree.HTML(r.text)
                rowlist = root.xpath('//ul[@class="listUl"]/li')
                for row in rowlist:
                    try:
                        housetitle = row.xpath('.//div[@class="des"]/h2/a/text()')[0].strip().encode('utf8')
                        link = row.xpath('.//div[@class="des"]/h2/a/@href')[0].strip().encode('utf8')
                        location = ' '.join(row.xpath('.//div[@class="des"]/p[@class="add"]/a//text()')).strip().encode('utf8') 
                        money = row.xpath('.//div[@class="listliright"]/div[@class="money"]/b/text()')[0].strip().encode('utf8')
                        csv_writer.writerow([housetitle, location, money, link])
                    except Exception,e:
                        pass
                # 判断是否是最后一页
                next = root.xpath('//div[@class="pager"]/a[@class="next"]')
                if not next:
                    break
                page += 1
                time.sleep(1)
            self.fd.close()
        except Exception,e:
            print e
        finally:
            if not self.fd.closed:
                self.fd.close()
        print 'end'



if __name__ == '__main__':
    client = Scan58()
    client.run()
    # r = requests.get('http://taizhou.58.com/chuzu/pn69/?PGTID=0d3090a7-002b-53bc-c267-62dfb371f5f5&ClickID=1')
    # root = etree.HTML(r.text)
    # next = root.xpath('//div[@class="pager"]/a[@class="next"]')
    # print next
    # j = client.getjson(r.text)
    # print j['xiaoqu']