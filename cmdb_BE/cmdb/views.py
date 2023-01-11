from django.shortcuts import render

# 导入modelviewset视图模型
from libs.custom_model_view_set import CustomModelViewSet

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

# 导入 SSH脚本
from libs.ssh import SSH

# 机房管理视图
class IdcViewSet(CustomModelViewSet):
    queryset = Idc.objects.all()      # 导入模型类所有数据
    serializer_class =  IdcSerializer   # 序列化数据

    # 导入模块，filters.SearchFilter 是指搜索, filters.OrderingFilter 是指排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    filterset_fields = ('name',)  # 指定可过滤的字段
    search_fields = ('name','city','provider')  # 指定可搜索的字段

    # 排序
    # 注意 filter_backends多了一个filters.OrderingFilter
    ordering_fields = ["id", "name"]



# 主机分组视图
class ServerGroupViewSet(CustomModelViewSet):
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
class CloudServerViewSet(CustomModelViewSet):
    queryset = Cloud_Server.objects.all()      # 导入模型类所有数据
    serializer_class =  CloudServerSerializer   # 序列化数据

    # 导入模块，filters.SearchFilter 是指搜索, filters.OrderingFilter 是指排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    filterset_fields = ('name',)  # 指定可过滤的字段
    search_fields = ('name',)  # 指定可搜索的字段

    # 排序
    # 注意 filter_backends多了一个filters.OrderingFilter
    ordering_fields = ["id", "name"]

    # 重新更新方法
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        # 获取hostname唯一字段
        hostname = request.data.get('hostname')
        # 一对多
        idc_id = int(request.data.get('idc'))
        idc_obj = Idc.objects.get(id=idc_id)
        Cloud_Server_obj = Cloud_Server.objects.get(hostname=hostname)
        Cloud_Server_obj.idc = idc_obj
        Cloud_Server_obj.save()

        # 多对多
        group_id_list = request.data.get('server_group')
        server = Cloud_Server.objects.get(hostname=hostname)
        server.server_group.add(*group_id_list)

        res = {'code': 200, 'msg': '更新成功'}
        return Response(res)

# 物理机视图
class PhysicsServerViewSet(CustomModelViewSet):
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
class VmServerViewSet(CustomModelViewSet):
    queryset = Vm_Server.objects.all()      # 导入模型类所有数据
    serializer_class =  VmServerSerializer   # 序列化数据

    # 导入模块，filters.SearchFilter 是指搜索, filters.OrderingFilter 是指排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    filterset_fields = ('name',)  # 指定可过滤的字段
    search_fields = ('name',)  # 指定可搜索的字段

    # 排序
    # 注意 filter_backends多了一个filters.OrderingFilter
    ordering_fields = ["id", "name"]




# 新建单台云主机并同步数据
class CloudServerCreateHostView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)

        # 接收前端提交的数据
        name = request.data.get('name')
        hostname = request.data.get('hostname')
        idc_id = int(request.data.get('idc'))   # 机房id
        server_group_id = request.data.get('server_group')   # 分组id
        machine_type = request.data.get('machine_type')
        ssh_ip = request.data.get('ssh_ip')
        ssh_port = int(request.data.get('ssh_port'))
        credential_id = int(request.data.get('credential'))
        note = request.data.get('note')

        # 如果主机存在返回
        server = Cloud_Server.objects.filter(hostname=hostname)
        if server:
            result = {'code': 500, 'msg': '主机已存在！'}
            return Response(result)

        # 判断机器类型，调用不同脚本执行
        if machine_type == 'linux':
            # 通过凭据ID获取用户名信息
            credential = Credential.objects.get(id=credential_id)
            username = credential.username
            if credential.auth_mode == 1:
                password = credential.password
                ssh = SSH(ssh_ip, ssh_port, username, password=password)
            else:
                private_key = credential.private_key
                ssh = SSH(ssh_ip, ssh_port, username, key=private_key)

            test = ssh.test()  # 测试SSH连接通过
            if test['code'] == 200:
                client_agent_name = "cloud_host_collect_linux.py"
                local_file = os.path.join(settings.BASE_DIR, 'cmdb', 'file', client_agent_name)
                remote_file = os.path.join(settings.CLIENT_COLLECT_DIR, client_agent_name)  # 这个工作路径在setting里配置
                ssh.scp(local_file, remote_file=remote_file)
                ssh.command('chmod +x %s' % remote_file)
                result = ssh.command('python %s' % remote_file)

                # 采集脚本执行成功
                if result['code'] == 200:
                    data = json.loads(result['data'])

                    if hostname != data['hostname']:
                        result = {'code': 500, 'msg': '填写的主机名与目标主机不一致，请核对后再提交！'}
                        return Response(result)

                    # 1.基本主机信息入库（人工录入）
                    idc = Idc.objects.get(id=idc_id)  # 根据id查询IDC
                    server_obj = Cloud_Server.objects.create(
                        idc=idc,  # 一对多，传入是一个idc对象
                        name=name if name else hostname,
                        hostname=hostname,
                        machine_type=machine_type,
                        ssh_ip=ssh_ip,
                        ssh_port=ssh_port,
                        is_verified='verified',
                        credential=credential,
                        note=note
                    )
                    # 添加对对多字段
                    for group_id in server_group_id:
                        group = ServerGroup.objects.get(id=group_id)  # 根据id查询分组
                        server_obj.server_group.add(group)  # 将服务器添加到分组

                    # 2.主机配置入库（自动采集）
                    server.update(**data)
                    result = {'code': 200, 'msg': '添加云主机成功并同步配置'}
                else:
                    result = {'code': 500, 'msg': '采集主机配置失败！错误：%s' % result['msg']}
            else:
                result = {'code': 500, 'msg': 'SSH连接异常！错误：%s' % test['msg']}
        else:
            pass

        return Response(result)
