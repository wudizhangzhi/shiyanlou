#coding=utf8

import requests
import threading

'''
简单的多线程下载器 
'''
class Downloader():
    def __init__(self, url, num=4):
        self.url = url
        self.num = num
        self.filename = url.split('/')[-1]
        r = requests.head(self.url)
        self.total = int(r.headers['Content-Length'])
        self.fd = None # file descriptor

    def get_range(self):
        offset = self.total/self.num
        rangelist = []
        for i in xrange(self.num):
            if i == self.num-1: #last part
                part = (offset*i, '')
            else:
                part = (offset*i, offset*(i+1)) 
            rangelist.append(part)
        return rangelist

    def download(self, start, end):
        headers = {'Range':'Bytes=%s-%s' % (start, end),'Accept-Encoding':'*'}
        r = requests.get(self.url, headers=headers, timeout=10)
        if not self.fd:
            raise 'no file opened!'
            return
        self.fd.seek(start)
        self.fd.write(r.content)
        print '%s-%s completed' % (start, end)

    def run(self):
        try:
            self.fd = open(self.filename, 'w')
            threadlist = []
            for start, end in self.get_range():
                t = threading.Thread(target=self.download, args=(start, end))
                t.start()
                print '%s start' % t.getName()
                threadlist.append(t)

            for t in threadlist:
                t.join()
            print 'download %s success!' % self.filename
            self.fd.close()
        except Exception,e:
            print e
        finally:
            if not self.fd.closed:
                print 'file is still open'
                self.fd.close()

if __name__ == '__main__':
    url = 'https://pic2.zhimg.com/2a92f27f1_xl.jpg'
    d = Downloader(url)
    d.run()