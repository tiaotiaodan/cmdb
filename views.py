#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Author:shichao
# File: .py


from flask import  Blueprint
from flask import render_template            # 返回一个文件模板
views = Blueprint("views",__name__)



@views.route('/servers')
def servers():
    return render_template("servers.html")

@views.route('/tools')
def tools():
    return render_template("tools.html")
