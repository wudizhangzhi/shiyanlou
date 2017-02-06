#coding=utf8

import time
import torndb
'''
CREATE DATABASE IF NOT EXISTS `memory`;
USE `memory`;
CREATE table IF NOT EXISTS `memory_data`(
    `id` int unsigned AUTO_INCREMENT COMMENT 'id',
    `createtime` int NOT NULL COMMENT 'time',
    `memuse` int NOT NULL COMMENT 'memory used',
    PRIMARY KEY (`id`)
)engine=InnoDB DEFAULT CHARSET=utf8;
'''
mysql_cursor = torndb.Connection(host='127.0.0.1',database='memory', user='root', password='admin')

def getMem():
    try:
        with open('/proc/meminfo') as f:
            MemTotal = int(f.readline().split()[1])
            MemFree = int(f.readline().split()[1])
            templist = f.readline().split() 
            if 'Available' in templist[0]:
                Buffers = int(f.readline().split()[1]) # skip MemAvailable
            else:
                Buffers = int(templist[1])
            Buffers = int(f.readline().split()[1])
            Cached = int(f.readline().split()[1])
    except Exception,e:
        print e
        return 0
    mem_use = MemTotal-MemFree-Buffers-Cached 
    return mem_use/1024 

def save_mem(mem_use):
    try:
        sql = 'insert into memory_data(`createtime`,`memuse`) values(%s,%s)'
        mysql_cursor.execute(sql, int(time.time()), mem_use),
    except Exception,e:
        print 'insert error:%s' % e

def monitor():
    while True:
        mem_use = getMem()
        save_mem(mem_use)
        print 'save %s' % time.strftime('%Y-%m-%d %H:%M:%S')
        time.sleep(1)


if __name__ == '__main__':
    monitor()

