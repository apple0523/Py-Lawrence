#!/bin/env python
# -*- coding:utf-8 -*-

import pymysql
import configparser
import spider


class MysqlOper:
    # initial database information
    def __init__(self, result_list):
        config = configparser.ConfigParser()
        config.read('db.conf')
        self.host = config['mysql']['HOST']
        self.port = int(config['mysql']['PORT'])
        self.user = config['mysql']['USER']
        self.passwd = config['mysql']['PASSWD']
        self.db = config['mysql']['DB']
        self.table = config['mysql']['TABLE']
        self.charset = config['mysql']['CHARSET']
        self.result_list = result_list

    def mysql_save(self):

        # create db cursor
        try:
            conn = pymysql.connect(self.host, self.user, self.passwd, self.db, port=self.port, charset=self.charset)
            cursor = conn.cursor()
            print('DB connect successfully.')
        except Exception as e:
            print("connect dbserver fail,Please see information:")
            print(e)
            exit(1)

        # check and create tables
        cursor.execute('show tables in test')
        tables = cursor.fetchall()
        flag = True
        for tab in tables:
            if self.table in tab:
                flag = False
                print('%s is exist' % self.table)
        print(flag)
        if flag:
            cursor.execute(
                '''create table ipproxy (id int, protocol varchar(20),content varchar(100))''')
        # else:
        #     return 0

        # write database
        for values in self.result_list:
            for prot, cont in values.items():
                try:
                    sql_insert = "insert into ipproxy (protocol,content) values ('"+prot+"','"+cont+"')"
                    print(sql_insert)
                    cursor.execute(sql_insert)
                    conn.commit()
                except Exception as e:
                    print("insert db occer error", e)
        cursor.close()
        conn.close()
        print("insert db successfully")

if __name__ == "__main__":
    proxyhelper = spider.GetProxyIP(2)
    res_pool = proxyhelper.get_ip()
    proxy_ip = proxyhelper.right_proxies(res_pool)
    dbhelper = MysqlOper(proxy_ip)
    dbhelper.mysql_save()
