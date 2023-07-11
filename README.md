# cmdb

#### 介绍
python3.8.4开发cmdb系统
使用到版本：
    django 3.2版本
    vue 3.0 版本
    element-plus 3.0版本

#### 软件架构
软件架构进行了前后端分离，cmdb_BE为后端代码，cmdb_FE为前端代码，
前后端部署请进入不同代码里面参考README说明进行安装部署

#### 软件整体呈现
![输入图片说明](https://foruda.gitee.com/images/1675066934488544421/3a20af8e_4875258.jpeg "QQ20230130-162009.jpg")
![输入图片说明](https://foruda.gitee.com/images/1675066911730886204/7e27d966_4875258.jpeg "QQ20230130-162027.jpg")
![输入图片说明](https://foruda.gitee.com/images/1675066894214235946/3bfc4031_4875258.jpeg "QQ20230130-162043.jpg")
![输入图片说明](https://foruda.gitee.com/images/1675066876252224072/bd8d8b59_4875258.jpeg "QQ20230130-162058.jpg")
开发域名管理，把阿里云和腾讯云域名集中导入到管理平台管理
完善前后端功能开发，实现平台展示



#### cmdb说明
本次开发的cmdb，实现阿里云和腾讯云通过api，excel文件导入，单台主机创建公共，并实现windows、linux、vmware进行数据采集同步



#### cmdb注意事项

1. 在windows采集同步方面需要在windows机器客户端进行安装openssh、winrm、python工具，并需要开启允许openssh和winrm远程连接和远程文件传输端口功能
2. 需设置openssh设置端口为默认22端口
3. winrm开启端口设置默认为5985端口，
4. 修改了openssh端口和winrm端口，请对应修改代码配置端口设置
