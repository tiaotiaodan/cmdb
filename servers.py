#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Author:shichao
# File: .py

from flask import Blueprint
import mysql_tools
from flask import request
from flask import render_template
from flask import  send_from_directory
from werkzeug.utils import  secure_filename    # 使用第三方扩展，来调用，过滤不正常的文件名
import json
import os
import time
import tool_excel

servers = Blueprint("servers", __name__)


# 获取数据库所有数据
@servers.route("/getall")
def getall():
    sql = "select * from servers;"
    result = mysql_tools.selectByParameters(sql)
    return json.dumps(result)


# 获取数据，设置分页
@servers.route("/get_by_page", methods=['get', 'post'])    #获取数据 methods提交数据格式
def get_by_page():
    info = request.get_data()           # 获取ajax的前端传回的数据
    info = json.loads(info)              # 将前端转递的转换为python字典
    pagenow = info['pagenow']           # 获取前端传回的数据
    pagesize = info['pagesize']         # 获取前端传回的数据
    search = info['search']             # 获取前端传回的数据搜索
    search = "%{0}%".format(search)     #
    sql = 'select * from servers where server_name like %s or server_ip like %s limit %s,%s'       # sql分页语句  %s 代码传递数据
    params = (search, search, (pagenow - 1) * pagesize, pagesize)      #
    result = mysql_tools.selectByParameters(sql, params=params)     # 使用mysql封装，查询sql
    return json.dumps(result)      # 将上面的数据转换为json格式，转递给前端


@servers.route('/get_by_id')
def get_by_id():
    id = int( request.args.get('id'))                   # 把前端返回的数据id，转换为int
    sql = "select * from servers where id = %s"
    result = mysql_tools.selectByParameters( sql, params=(id, ) )
    return json.dumps(result)         # 将上面的数据转换为json格式，转递给前端

# 更新字段
@servers.route('/update', methods=['get', 'post'])
def update():
    info = request.get_data()
    info = json.loads(info)
    sql = 'replace into servers (id,server_name,server_ip, server_port, server_user,server_passwd) VALUES(%s, %s, %s, %s, %s,%s);'
    params = (info['id'], info['server_name'], info['server_ip'], info['server_port'], info['server_user'],info['server_passwd'])
    mysql_tools.updateByParameters( sql, params )
    return "Success"

# 服务器添加
@servers.route('/insert', methods=['get', 'post'])
def insert():
    info = request.get_data()
    info = json.loads(info)
    sql = 'replace into servers (server_name,server_ip, server_port, server_user,server_passwd) VALUES(%s, %s, %s, %s,%s);'
    params = ( info['server_name'], info['server_ip'], info['server_port'], info['server_user'], info['server_passwd'])
    mysql_tools.updateByParameters( sql, params )
    return "Success"

# 下载导入execl模板文件
@servers.route('/getexcel')
def getexcel():
    curdir = os.path.dirname(os.path.realpath(__file__))
    return send_from_directory( curdir + "/static/", "servers.xlsx", as_attachment=True )

# 导入execl服务
@servers.route('/insert_from_excel', methods=['get', 'post'])
def insert_from_excel():
    f = request.files.get('servers')
    ramname = int(time.time() * 1000)
    f.save('/tmp/{0}'.format( ramname ))
    tool_excel.insertFromExcel( '/tmp/{0}'.format( ramname ) )
    return "Success!"

# 删除单个
@servers.route('/delete_by_id')
def delete_by_id():
    id = int( request.args.get('id') )
    sql = 'delete from servers where id = %s'
    mysql_tools.updateByParameters( sql, (id, ) )
    return "Servers!"

# 批量删除
@servers.route('/mutidelete', methods=['get', 'post'])
def mutidelete():
    info = request.get_data()
    info = json.loads(info)
    for oneid in info:
        # print(oneid)
        sql = 'delete from servers where id = %s'
        mysql_tools.updateByParameters(sql, (oneid, ))
    return "Success!"