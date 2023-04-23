"""devops_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from cmdb import urls as cmdburls
from system_config import urls as systemconfigurls
from domain import urls as domainurls
from libs import token_auth        # 导入认证登陆接口文件

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cmdb/', include(cmdburls)),    # 主机管理
    path('config/', include(systemconfigurls)),  # 主机账号配置管理
    path('domain/', include(domainurls)),   # 域名管理
    path('login/', token_auth.CustomAuthToken.as_view()),   # 配置认证登陆提交路由
    path('change_password/', token_auth.ChangeUserPasswordView.as_view()),   # 配置密码修改提交路由
    path('user_info/', token_auth.UserList.as_view()), # 获取用户信息
]

