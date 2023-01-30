# 线上部署-后端



### 1. 线上部署-后端

- 部署架构

  Nginx 前端Web服务，接收到动态请求通过uwsgi模块将请求转发给uwsgi服务器，uwsgi服务器通过django处理完后返回给Nginx，Nginx返回用户浏览器展示。

   

  **既然uwsgi是一个可以独立部署的服务器，为什么还用Nginx代理？**

  •     Nginx作为入口可配置安全策略，并且可以为uwsgi提供负载均衡。

  •     Nginx处理静态资源能力强

- 将本地项目开发的项目环境打包

  - 导出依赖模块列表

    ```shell
    (cmdb) [admin@shichaodeMacBook-Pro cmdb_BE]#  pip3 freeze > requirements.txt
    
    (cmdb) [admin@shichaodeMacBook-Pro cmdb_BE]#  cat requirements.txt 
    aliyun-python-sdk-core==2.13.36
    aliyun-python-sdk-ecs==4.24.28
    asgiref==3.6.0
    bcrypt==4.0.1
    certifi==2022.12.7
    cffi==1.15.1
    charset-normalizer==3.0.1
    cryptography==39.0.0
    Django==3.2.13
    django-cors-headers==3.13.0
    django-filter==22.1
    djangorestframework==3.14.0
    docopt==0.6.2
    idna==3.4
    jmespath==0.10.0
    ntlm-auth==1.5.0
    paramiko==2.12.0
    prompt-toolkit==1.0.18
    pycparser==2.21
    pyflakes==3.0.1
    Pygments==2.14.0
    PyMySQL==1.0.2
    PyNaCl==1.5.0
    pytz==2022.7.1
    pyvim==0.0.21
    pyvmomi==6.7.1
    pywinrm==0.4.3
    requests==2.28.2
    requests-ntlm==1.1.0
    six==1.16.0
    sqlparse==0.4.3
    tencentcloud-sdk-python==3.0.816
    urllib3==1.26.14
    wcwidth==0.2.6
    xlrd==1.2.0
    xmltodict==0.13.0
    
    ```

  - 修改数据库驱动或配置

    ```python
    # devops_api/__init__.py
    import pymysql
    pymysql.install_as_MySQLdb()
    
    ```

    ```python
    # vi devops_api/settings.py
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'cmdb',
            'USER': 'root',
            'PASSWORD': '123456',
            'HOST': '127.0.0.1',
            'PORT': 3306,
        }
    }
    ```

  - 关闭debug模式和白名单：

    ```python
    DEBUG = False   # 调试模式
    ALLOWED_HOSTS = ['*']  # 白名单，只允许列表中的ip访问，*代表所有
    ```

- 服务器环境准备

  - 安装python3

    ```shell
    yum install zlib-devel libffi-devel mysql-devel bzip2-devel git -y
    wget  https://www.python.org/ftp/python/3.8.4/Python-3.8.4.tgz
    tar zxvf Python-3.8.4.tgz
    cd Python-3.8.4
    ./configure 
    make && make install
    ```

  - 安装依赖模块列表

    ```
    pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
    ```

  - 安装数据库

    ```shell
    docker run -d --name db -p 3306:3306 -v mysqldata:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 mysql:5.7 --character-set-server=utf8
    
    docker exec -it db bash
    root@e2eff2d75dd2:/# mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "create database cmdb;"
    
    ```

  - 启动开发环境，验证依赖模块

    ```shell
    python3 manage.py runserver 0.0.0.0:8080
    ```

  - 测试问题，同步数据库

    ```shell
    python3 manage.py migrate
    ```

  - 收集静态文件

    ```python
    # 编写settings.py文件，创建生成静态文件目录
    vi settings.py
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR,'static')
    
    # 执行生成静态
    python3 manage.py collectstatic
    
    ```

  - 创建管理员账号：

    ```
    python3 manage.py createsuperuser
    ```

- 安装与配置uwsgi

  - uWSGI是一个[Web服务器](https://baike.baidu.com/item/Web服务器/8390210)，也是Python的一个模块，直接pip安装即可： 

    ```
    pip3 install uwsgi -i https://mirrors.aliyun.com/pypi/simple
    ```

  - 创建uwsgi配置文件，路径任意:

    ```shell
    mkdir /opt/cmdb/uwsgi
    # vi /opt/devops_api/uwsgi/uwsgi.ini 
    [uwsgi]
    # 项目目录
    chdir = /opt/cmdb
    
    # 指定sock的文件路径
    socket = /opt/cmdb/uwsgi/uwsgi.sock
    # 指定监听端口
    # http = 0.0.0.0:8080
    
    # 静态资源
    static-map = /static=/opt/cmdb/static
    
    # wsgi文件（django入口）
    wsgi-file=cmdb/wsgi.py
    
    # 进程个数
    processes = 2
    
    # 指定项目的应用
    # module = devops_api.wsgi
    
    # 进程pid
    pidfile = /opt/uwsgi/uwsgi.pid
    
    # 日志路径
    daemonize = /opt/uwsgi/uwsgi.log
    
    ```

  - 启动：

    ```shell
    vi /usr/lib/systemd/system/uwsgi.service 
    
    [Unit]
    Description=HTTP Interface Server
    
    [Service]
    Type=forking
    ExecStart=/usr/local/bin/uwsgi --ini /opt/uwsgi/uwsgi.ini
    ExecReload=/bin/kill -s HUP $MAINPID
    Restart=always
    
    [Install]
    WantedBy=multi-user.target
    
    systemctl daemon-reload
    systemctl start uwsgi
    systemctl enable uwsgi
    ```

- 配置nginx

  - 安装nginx服务

    ```shell
    yum install epel-release –y
    yum install nginx -y
    ```

  - 配置nginx配置文件

    ```shell
    [root@prod conf.d]# cat api.scajy.cn.conf 
    server {
            listen       80;
            server_name  api.scajy.cn;
    
            location / {
               include     uwsgi_params;  # 导入模块用于与uwsgi通信
               uwsgi_pass unix:/opt/uwsgi/uwsgi.sock; 
            }
            # 静态文件目录
            location /static {
               alias /opt/devops_api/static;
            }
    }
    ```

  - 重启nginx

    ```shell
    [root@prod conf.d]# nginx -t
    nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
    nginx: configuration file /etc/nginx/nginx.conf test is successful
    [root@prod conf.d]# nginx -s reload
    ```

  

- 浏览器验证api接口是否正常

  
