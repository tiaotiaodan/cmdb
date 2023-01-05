from django.shortcuts import render

# 导入modelviewset视图模型
from rest_framework.viewsets import ModelViewSet

# 导入模型
from cmdb.models import Idc, ServerGroup, Cloud_Server, Physics_Server, Vm_Server

# 导入序列化
from cmdb.serializers import IdcSerializer, ServerGroupSerializer, CloudServerSerializer, PhysicsServerSerializer, VmServerSerializer

# 导入过滤、搜索和排序插件
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# 导入系统管理模型
from system_config.models import Credential

# 导入 SSH脚本
from libs.ssh import SSH
# 导入APIView
from rest_framework.views import APIView
# 导入drf返回 Response模块
from rest_framework.response import Response
from django.conf import settings

import os, json

# 机房管理视图
class IdcViewSet(ModelViewSet):
    queryset = Idc.objects.all()      # 导入模型类所有数据
    serializer_class =  IdcSerializer   # 序列化数据

    # 导入模块，filters.SearchFilter 是指搜索, filters.OrderingFilter 是指排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    filterset_fields = ('name',)  # 指定可过滤的字段
    search_fields = ('name',)  # 指定可搜索的字段

    # 排序
    # 注意 filter_backends多了一个filters.OrderingFilter
    ordering_fields = ["id", "name"]



# 主机分组视图
class ServerGroupViewSet(ModelViewSet):
    queryset = ServerGroup.objects.all()      # 导入模型类所有数据
    serializer_class =  ServerGroupSerializer   # 序列化数据

    # 导入模块，filters.SearchFilter 是指搜索, filters.OrderingFilter 是指排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    filterset_fields = ('name',)  # 指定可过滤的字段
    search_fields = ('name',)  # 指定可搜索的字段

    # 排序
    # 注意 filter_backends多了一个filters.OrderingFilter
    ordering_fields = ["id", "name"]

# 云主机视图
class CloudServerViewSet(ModelViewSet):
    queryset = Cloud_Server.objects.all()      # 导入模型类所有数据
    serializer_class =  CloudServerSerializer   # 序列化数据

    # 导入模块，filters.SearchFilter 是指搜索, filters.OrderingFilter 是指排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    filterset_fields = ('name',)  # 指定可过滤的字段
    search_fields = ('name',)  # 指定可搜索的字段

    # 排序
    # 注意 filter_backends多了一个filters.OrderingFilter
    ordering_fields = ["id", "name"]

# 物理机视图
class PhysicsServerViewSet(ModelViewSet):
    queryset = Physics_Server.objects.all()      # 导入模型类所有数据
    serializer_class =  PhysicsServerSerializer   # 序列化数据

    # 导入模块，filters.SearchFilter 是指搜索, filters.OrderingFilter 是指排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    filterset_fields = ('name',)  # 指定可过滤的字段
    search_fields = ('name',)  # 指定可搜索的字段

    # 排序
    # 注意 filter_backends多了一个filters.OrderingFilter
    ordering_fields = ["id", "name"]

# 虚拟机视图
class VmServerViewSet(ModelViewSet):
    queryset = Vm_Server.objects.all()      # 导入模型类所有数据
    serializer_class =  VmServerSerializer   # 序列化数据

    # 导入模块，filters.SearchFilter 是指搜索, filters.OrderingFilter 是指排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    filterset_fields = ('name',)  # 指定可过滤的字段
    search_fields = ('name',)  # 指定可搜索的字段

    # 排序
    # 注意 filter_backends多了一个filters.OrderingFilter
    ordering_fields = ["id", "name"]


#

# linux同步
class PhysicsServerSshConnView(APIView):
    def get(self, request, *args, **kwargs):
        # 获取前端提交数据
        hostname = request.query_params.get("hostname")

        # 通过server模型调用数据库进行查询
        server = Physics_Server.objects.get(hostname=hostname)
        credential_id = server.credential.id           # 这里是一对多的关系，直接表关联，是取的对象
        ssh_ip = server.ssh_ip
        ssh_port = server.ssh_port

        # 查询系统配置
        credential = Credential.objects.get(id=credential_id)
        username = credential.username
        password = credential.password
        private_key = credential.private_key

        if credential.auth_mode == 1:
            print("密码")
            ssh = SSH(ssh_ip, ssh_port, username, password=password)
        else:
            print("密钥")
            ssh = SSH(ssh_ip, ssh_port, username, key=private_key)

        # 测试是否ssh连接成功
        result = ssh.test()
        if result['code'] == 200:
            client_agent_name = "local_host_collect_linux.py"
            local_file = os.path.join(settings.BASE_DIR, 'cmdb', 'file', client_agent_name)
            remote_file = os.path.join(settings.CLIENT_COLLECT_DIR, client_agent_name)  # 这个工作路径在setting里配置
            ssh.scp(local_file, remote_file)
            ssh.command('chmod +x %s' % remote_file)
            result = ssh.command('python %s' % remote_file)
            if result['code'] == 200:
                data = json.loads(result['data'])
                data['is_verified'] = 'verified'
                Physics_Server.objects.filter(hostname=hostname).update(**data)
                code = 200
                msg = '主机配置同步成功'
            else:
                code = 500
                msg = '主机配置同步失败，错误： %s' % result['msg']

            res = {'code': code, 'msg':  msg}
        else:
            res = {'code': 500, 'msg':'主机数据同步失败'}

        return Response(res)