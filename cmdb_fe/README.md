# 线上部署-前端



### 1. 线上部署-前端

- 进行代码编译打包

  ```
  npm install
  npm run build
  ```

  > 会自动生成dist目录，把dist目录下的所有文件拷贝到nginx对应目录处理

- 编写前端nginx配置

  ```shell
  [root@prod conf.d]# cat test.conf 
  #www
      server {
          listen       80;
          server_name  test.scajy.cn;
          location / {
              root   /var/www/html/cmdb.test.cn;
              try_files $uri $uri  /index.html;
              # 需要指向下面的@router否则会出现vue的路由在nginx中刷新出现404
          }
          location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$ {
              expires      30d;
              root   /var/www/html/cmdb.test.cn;
          }
          location ~ .*\.(js|css)?$ {
              expires          30d;
              root   /var/www/html/cmdb.test.cn;
          }
          access_log /var/log/nginx/cmdb.test.cn_access.log    main;
     }
  ```

  
