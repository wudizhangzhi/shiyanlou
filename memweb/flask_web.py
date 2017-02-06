#coding=utf8

from flask import Flask, render_template
import json
import time
import torndb

mysql_cursor = torndb.Connection(host='127.0.0.1',database='memory', user='root', password='admin')
tmp_time = 0

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    global tmp_time
    if tmp_time > 0:
        sql = 'select * from memory_data where createtime>%s'
        ret = mysql_cursor.query(sql, tmp_time)
    else:
        sql = 'select * from memory_data'
        ret = mysql_cursor.query(sql)
    tmp_time = int(time.time())
    data = [(i['createtime']*1000, i['memuse']) for i in ret]

    return json.dumps(data)



if __name__ == '__main__':
    app.run(port=9092, debug=True)