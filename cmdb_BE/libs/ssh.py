import paramiko
from io import StringIO  # py2 from StringIO import StringIO
import os

class SSH():
    def __init__(self, ip, port, username, password=None, key=None):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.key = key

    def command(self, shell):
        # 绑定实例
        ssh = paramiko.SSHClient()
        # 允许连接不在known_hosts文件上的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            # 判断是密码登陆，还是密钥登陆
            if self.password:
                ssh.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password, timeout=5)
            else:
                cache = StringIO(self.key)  # 将字符串通过StringIO转为file对象（self.key内容是从数据库查询的文本）
                key = paramiko.RSAKey.from_private_key(cache)  # 接收file对象
                # 使用key登录
                ssh.connect(hostname=self.ip, port=self.port, username=self.username, pkey=key)
            # 执行Shell命令，结果分别保存在标准输入，标准输出和标准错误
            stdin, stdout, stderr = ssh.exec_command(shell)
            stdout = stdout.read()
            error = stderr.read()
            # 判断stderr输出是否为空，为空则打印运行结果，不为空打印报错信息
            ssh.close()
            if not error:
                return {'code':200, 'msg':'执行命令成功', 'data': stdout}
            else:
                return {'code':500, 'msg':'执行命令失败', 'data': error}
        except Exception as e:
            return {'code':500, 'msg':'SSH连接失败! 错误信息： %s' % e}

    def scp(self, local_file, remote_file):
        # 绑定实例
        ts = paramiko.Transport((self.ip, self.port))
        try:
            if self.password:
                ts.connect(username=self.username, password=self.password)
            else:
                cache = StringIO(self.key)
                key = paramiko.RSAKey.from_private_key(cache)
                ts.connect(username=self.username, pkey=key)
            sftp = paramiko.SFTPClient.from_transport(ts)
            try:
                sftp.put(localpath=local_file, remotepath=remote_file)
                ts.close()
                return {'code':200, 'msg':'上传文件成功'}
            except Exception as e:
                return {'code':500, 'msg':'上传文件失败 %s' %e }
        except Exception as e:
            return {'code':500, 'msg':'SSH连接失败 %s' %e }

    # 新增一个ssh验证方法
    def test(self):
        result = self.command('ls')
        return result

if __name__ == '__main__':
    ssh = SSH('192.168.0.200', 22, 'root', '123456')
    ssh.test()
    local_file=os.path.join(os.getcwd(),'local_host_collect_linux.py')
    result = ssh.scp(local_file, '/tmp/local_host_collect_linux.py')
    result = ssh.command('chmod +x /tmp/local_host_collect_linux.py')
    result = ssh.command('python /tmp/local_host_collect_linux.py')

    print(result)