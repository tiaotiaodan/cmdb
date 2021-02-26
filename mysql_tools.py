#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Author:shichao
# File: .py
import pymysql


# 封装连接
def getConnect():
    try:
        connection = pymysql.connect(
            host="127.0.0.1",
            user="cmdb",
            password="Aa123456",
            database="cmdb",
            port=3306)
        return connection
    except Exception as e:
        print(e)


def selectByParameters(sql, params=None):
    try:
        connection = getConnect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql,params)
        fc = cursor.fetchall()
        return fc
    except Exception as e:
        print(e)
    finally:
        try:
            cursor.close()
        except Exception as e:
            print(e)
        try:
            connection.close()
        except Exception as e:
            print(e)


def updateByParameters(sql, params=None):
    try:
        connection = getConnect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        count = cursor.execute(sql,params)
        connection.commit()
        return count
    except Exception as e:
        connection.rollback()
        print(e)
    finally:
        try:
            cursor.close()
        except Exception as e:
            print(e)
        try:
            connection.close()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    sql = "select * from servers"
    result = selectByParameters( sql )
    print(result)
