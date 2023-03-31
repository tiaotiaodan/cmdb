from channels.generic.websocket import WebsocketConsumer
from threading import Thread
import paramiko
import json
from io import StringIO

from system_config.models import Credential

class SSHConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ssh_ip = None
        self.ssh_port = None
        self.credential_id = None
        self.channel = None
        self.ssh = None

    # 处理请求参数
    def connect(self):
        self.ssh_ip = self.scope['url_route']['kwargs']['ssh_ip']
        self.ssh_port = self.scope['url_route']['kwargs']['ssh_port']
        self.credential_id = self.scope['url_route']['kwargs']['credential_id']
        self.accept()  # 与前端建立ws连接
        self.ssh_stream() # 与服务器建立ssh连接

    def ssh_stream(self):
        self.send(bytes_data=b'Connecting ...\r\n')
        try:
            # 获取SSH连接
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            credential = Credential.objects.get(id=self.credential_id)
            username = credential.username
            if credential.auth_mode == 1:
                password = credential.password
                ssh.connect(self.ssh_ip, self.ssh_port, username, password=password)
            else:
                cache = StringIO(credential.private_key)
                private_key = paramiko.RSAKey.from_private_key(cache)
                ssh.connect(self.ssh_ip, self.ssh_port, username, pkey=private_key)
            self.ssh = ssh
        except Exception as e:
            self.send(bytes_data=f'Exception: {e}\r\n'.encode())
            self.close()
            return
        # 创建ssh执行通道
        self.channel = self.ssh.invoke_shell(term='xterm')
        self.channel.transport.set_keepalive(30)
        Thread(target=self.loop_read).start()

    # 循环读取ssh通道数据并发送给前端
    def loop_read(self):
        while True:
            data = self.channel.recv(32 * 1024)
            if not data:
                break
            self.send(bytes_data=data)

    # 接收前端发送过来的数据并发送到ssh执行通道
    def receive(self, text_data=None, bytes_data=None):
        data = text_data or bytes_data
        if data:
            data = json.loads(data)
            # 动态设置终端窗口大小
            resize = data.get('resize')
            if resize and len(resize) == 2:
                self.channel.resize_pty(*resize)
            else:
                self.channel.send(data['data'])

    # 关闭连接
    def disconnect(self, close_code):
        self.channel.close()
        self.ssh.close()
