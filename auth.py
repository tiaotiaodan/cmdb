#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Author:shichao
# File: .py


from flask import Blueprint
from flask import request
from flask import redirect
from flask import make_response
from flask import session
import mysql_tools
import tool_pass

auth = Blueprint("auth", __name__)


@auth.route('/login', methods = ['get', 'post'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    password = tool_pass.md5encrypt(password)
    sql = "select * from user where username = %s and password = %s"
    result = mysql_tools.selectByParameters(sql, ( username, password ))
    if result:
        session['username'] = username
        return redirect('/views/servers')
    else:
        return redirect("/static/login.html")


@auth.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    return redirect('/')

