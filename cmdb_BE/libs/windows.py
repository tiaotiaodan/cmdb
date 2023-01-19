#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# Author:shichao
# File: .py

import winrm
import paramiko
import os

class Win_ssh():
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def win_command(self, shell):
        try:
            wintest = winrm.Session('http://' + self.ip + ':5985/wsman', auth=(self.username, self.password))
            ret = wintest.run_cmd(shell)
            ret = ret.std_out.decode()
            return {'code':200, 'msg': '执行命令成功', 'data': ret}
        except Exception as e:
            return {'code': 500, 'msg': '执行命令失败! 错误信息： %s' % e}


    def win_scp(self, local_file, remote_file):
        try:
            ts = paramiko.Transport(self.ip, self.port )  # 获取Transport实例，其中22为端口号
            ts.connect(username=self.username, password=self.password)  # 建立连接

            try:
                # 获取SFTP实例
                sftp = paramiko.SFTPClient.from_transport(ts)

                # 执行上传动作
                sftp.put(localpath=local_file, remotepath=remote_file)
                ts.close()
                return {'code': 200, 'msg': '上传文件成功'}
            except Exception as e:
                return {'code':500, 'msg':'上传文件失败 %s' %e }
        except Exception as e:
            return {'code':500, 'msg':'SSH连接失败 %s' %e }


    # 新增一个远程连接测试方法
    def test(self):
        result = self.win_command('dir')
        return result


if __name__ == '__main__':
    ssh = Win_ssh("172.16.128.98", 22, "admin", "Aa@963852#@!")
    # result = ssh.test()  # 验证是否能连接
    local_file = os.path.join(os.getcwd(), 'local_host_collect_windows.py')   # 本地需要上传的文件

    ssh.win_scp(local_file, "C:\\Users\\admin\\Desktop\\local_host_collect_windows.py")    # 执行paramiko上传文件功能
    result = ssh.win_command('python C:/Users/admin/Desktop/local_host_collect_windows.py')  # 使用winrm功能进行执行命令

    print(result)