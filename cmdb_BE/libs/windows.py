#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# Author:shichao
# File: .py

import winrm

class windows_ssh():
    def __init__(self, ip, username, password):
        self.ip = ip
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

    # 新增一个远程连接测试方法
    def test(self):
        result = self.win_command('dir')
        return result


if __name__ == '__main__':
    ssh = windows_ssh("172.16.128.98", "admin", "Aa@963852#@!")
    # result = ssh.test()
    result = ssh.win_command('python C:/Users/admin/Desktop/test.py')
    print(result)

