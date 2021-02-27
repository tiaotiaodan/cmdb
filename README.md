# Flask项目cmdb的创建和运行

## flask介绍

#### Flask的安装

1. FLask是python的第三方模块，可以用来网站后台开发
2. flask的安装：pip install flask  -i https://pypi.tuna.tsinghua.edu.cn/simple
3. mysql连接工具： pip install pymysql  -i https://pypi.tuna.tsinghua.edu.cn/simple



#### 软件架构
1. static存放静态文件
2. templates存放模块文件
3. app.py为python web后台编码



### Flask内置web服务器说明

1. Flask运维开发指的是web开发，web开发都需要有web服务器来调试代码
2. flask内置了个简单的web服务器仅供开发调试使用
3. 线上部署flask采用Nginx+Uwsgi的方式



## flask项目cmdb的安装


#### 安装教程

1. centos 7安装python3

   - 1. 首先安装依赖包

           ```shell
        # yum -y install   zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel   readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel   libffi-devel   
        ```

     2. 下载python3安装包

        ```shell
        [root@python tools]#   wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz   
        ```

     3. 解压

           ```shell
        [root@python tools]#   tar xvzf Python-3.7.4.tgz    
        ```

     4. 创建文件夹把python3安装在里面

           ```shell
        [root@python tools]#   mkdir -p /usr/local/python3   
        [root@python tools]#   cd Python-3.7.4   
        [root@python   Python-3.7.4]# ./configure --prefix=/usr/local/python3/   
        [root@python   Python-3.7.4]# make && make install   
        ```

     5. 建立软连接

           ```shell
        [root@python   Python-3.7.4]# ln -s /usr/local/python3/bin/python3.7 /usr/bin/python3   
        [root@python   Python-3.7.4]# ln -s /usr/local/python3/bin/pip3.7 /usr/bin/pip3  
        ```

     6. 验证和测试

           ```python
        [root@python   Python-3.7.4]# python3   
        Python 3.7.4   (default, Jul 26 2019, 04:16:54)    
        [GCC 4.8.5 20150623   (Red Hat 4.8.5-36)] on linux   
        Type   "help", "copyright", "credits" or   "license" for more information.   
        >>>    
        ```

2. 安装程序所要的pip包

   ```shell
   # pip3 install flask
   # pip3 install pymysql 
   # pip3 install xlrd
   ```

3. 安装uwsgi

   1. 说明

      flask默认的web服务器

      - flask默认的web服务器不适用于线上环境
      - 一般线上环境都是使用nginx+Uwsgi

   2. 安装uwsgi

      ```shell
      # pip3 install uwsgi
      [root@web1 uwsgi]# ln -s /usr/local/python3/bin/uwsgi  /usr/bin/uwsgi
      ```

      - 验证uwsgi是否能使用

        ```shell
        [root@web1 uwsgi]# uwsgi -version
        *** Starting uWSGI 2.0.19.1 (64bit) on [Sat Feb 27 13:25:19 2021] ***
        compiled with version: 4.8.5 20150623 (Red Hat 4.8.5-39) on 27 February 2021 03:14:45
        os: Linux-3.10.0-1127.13.1.el7.x86_64 #1 SMP Tue Jun 23 15:46:38 UTC 2020
        nodename: web1
        machine: x86_64
        clock source: unix
        pcre jit disabled
        detected number of CPU cores: 1
        current working directory: /opt/uwsgi
        detected binary path: /usr/local/python3/bin/uwsgi
        uWSGI running as root, you can use --uid/--gid/--chroot options
        *** WARNING: you are running uWSGI as root !!! (use the --uid flag) *** 
        *** WARNING: you are running uWSGI without its master process manager ***
        your processes number limit is 7266
        your memory page size is 4096 bytes
        detected max file descriptor number: 100001
        lock engine: pthread robust mutexes
        thunder lock: disabled (you can enable it with --thunder-lock)
        uWSGI running as root, you can use --uid/--gid/--chroot options
        *** WARNING: you are running uWSGI as root !!! (use the --uid flag) *** 
        uWSGI running as root, you can use --uid/--gid/--chroot options
        *** WARNING: you are running uWSGI as root !!! (use the --uid flag) *** 
        The -s/--socket option is missing and stdin is not a socket.
        
        ```

   3. Uwsgi的编写配置uwsgi.ini

      ```shell
      [root@web1 ~]# cd /opt/
      [root@web1 opt]# mkdir -p uwsgi
      [root@web1 opt]# cd uwsgi/
      [root@web1 uwsgi]# vim uwsgi.ini
      [root@web1 uwsgi]# cat uwsgi.ini
      [uwsgi] 
      uid = root 
      gid = root 
      socket = /dev/shm/uwsgi.sock
      chmod-socket = 666
      enable-threads = true
      master = true
      plugins = /usr/bin/python3
      vhost = true
      workers = 5
      max-requests = 1000
      pidfile = /var/run/uwsgi.pid
      daemonize = /var/log/uwsgi.log
      chdir = /opt/uwsgi/cmdb
      module = app 
      callable = app
      ```
      
   4. 上传cmdb到服务器上

      - 这里通过sftp上传服务到/opt/uwsgi下

        ```shell
        [root@web1 uwsgi]# ll
        total 8
        drwxr-xr-x 8 root root 4096 Feb 27 13:09 cmdb
        -rw-r--r-- 1 root root  302 Feb 27 13:37 uwsgi.ini
        ```

      - 注释：这里根据自己情况上传

   5. 启动uwsgi服务

      ```shell
      [root@web1 uwsgi]# uwsgi uwsgi.ini 
      [uWSGI] getting INI configuration from uwsgi.ini
      open("/usr/bin/python3_plugin.so"): No such file or directory [core/utils.c line 3732]
      /usr/bin/python3_plugin.so: cannot open shared object file: No such file or directory
      ```
      
   6. 验证uwsgi是否启动
      
      ```shell
      [root@web1 uwsgi]# ps -auxfw
      USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
      .........省略
      root     26478  0.0  0.0  97404  1856 ?        Sl   13:07   0:00 /usr/local/qcloud/stargate/bin/sgagent -d
      root       759  0.0  0.3 165372  6996 ?        S    13:37   0:00 uwsgi uwsgi.ini
      root       761  0.0  0.4 181360  7984 ?        S    13:37   0:00  \_ uwsgi uwsgi.ini
      root       762  0.0  0.4 181360  7984 ?        S    13:37   0:00  \_ uwsgi uwsgi.ini
      root       763  0.0  0.4 181360  7984 ?        S    13:37   0:00  \_ uwsgi uwsgi.ini
      root       764  0.0  0.4 181360  7984 ?        S    13:37   0:00  \_ uwsgi uwsgi.ini
      root       765  0.0  0.4 181360  7984 ?        S    13:37   0:00  \_ uwsgi uwsgi.ini
      ```

4. 安装nginx

   1. 安装nginx

      ```shell
      # rpm -ivh http://mirrors.ustc.edu.cn/epel/7/x86_64/Packages/e/epel-release-7-13.noarch.rpm 
      # rpm -ivh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
      # yum install -y  nginx
      ```

   2. 启动nginx和设置开机启动

      ```shell
      # /bin/systemctl start nginx.service
      # /bin/systemctl enable nginx.service
      ```

5. 配置nginx请求uswgi处理

   1. 配置nginx

      ```shell
      [root@web1 uwsgi]# cd /etc/nginx/conf.d/
      [root@web1 conf.d]# vim default.conf 
      [root@web1 conf.d]# cat default.conf 
       server {
             listen       80;
             server_name  cmdb.scajy.cn;
             location / {
      	uwsgi_pass unix:/dev/shm/uwsgi.sock;
      	include uwsgi_params;
       }
      [root@web1 conf.d]# cat ../uwsgi_params 
      
      uwsgi_param  QUERY_STRING       $query_string;
      uwsgi_param  REQUEST_METHOD     $request_method;
      uwsgi_param  CONTENT_TYPE       $content_type;
      uwsgi_param  CONTENT_LENGTH     $content_length;
      
      uwsgi_param  REQUEST_URI        $request_uri;
      uwsgi_param  PATH_INFO          $document_uri;
      uwsgi_param  DOCUMENT_ROOT      $document_root;
      uwsgi_param  SERVER_PROTOCOL    $server_protocol;
      uwsgi_param  REQUEST_SCHEME     $scheme;
      uwsgi_param  HTTPS              $https if_not_empty;
      
      uwsgi_param  REMOTE_ADDR        $remote_addr;
      uwsgi_param  REMOTE_PORT        $remote_port;
      uwsgi_param  SERVER_PORT        $server_port;
      uwsgi_param  SERVER_NAME        $server_name;
      ```

   2. 检查nginx配置文件

      ```
      [root@web1 conf.d]# nginx -t
      nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
      nginx: configuration file /etc/nginx/nginx.conf test is successful
      
      ```

   3. 重启nginx

      ```shell
      [root@web1 conf.d]# /bin/systemctl restart nginx
      ```

   4. 浏览器访问验证

      ```shell
      [root@web2 ~]# curl  -I cmdb.scajy.cn
      HTTP/1.1 200 OK
      Server: nginx/1.18.0
      Date: Sat, 27 Feb 2021 06:07:26 GMT
      Content-Type: text/html; charset=utf-8
      Content-Length: 1689
      Connection: keep-alive
      ```

#### 提示

1.  本次cmdb开发，是临时公司存储密码和账号开发，功能不是很完善，
2.  sql目录是导入数据库的表和字段
3.  有需要的可以进行二次开发
