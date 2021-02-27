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

2. 安装uwsgi

   1. 说明

      flask默认的web服务器

      - flask默认的web服务器不适用于线上环境
      - 一般线上环境都是使用nginx+Uwsgi

   2. 安装uwsgi

      ```shell
      # pip3 install uwsgi
      ```

   3. 配置Uwsgi

      ```
      
      ```

      

3. xxx

4. xxx

#### 使用说明

1.  xxxx
2.  xxxx
3.  xxxx

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request
