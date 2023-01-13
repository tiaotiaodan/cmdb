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

# 导入 win脚本
from libs.windows import Win_ssh

# 导入APIView
from rest_framework.views import APIView

# 导入drf返回 Response模块
from rest_framework.response import Response
from django.conf import settings

# 导入文件返回格式FileResponse
from django.http import FileResponse

import os, json, xlrd, time

# 导入调用阿里云模块
from libs.aliyun_cloud import AliCloud
# 导入调用腾讯云模块
from libs.tencent_cloud import TCloud

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
            # 通过凭据ID获取用户名信息
            credential = Credential.objects.get(id=credential_id)
            username = credential.username
            if credential.auth_mode == 1:
                password = credential.password
                win_ssh = Win_ssh(ssh_ip, ssh_port, username, password=password)

            test = win_ssh.test()  # 测试SSH连接通过
            if test['code'] == 200:
                client_agent_name = "cloud_host_collect_windows.py"
                local_file = os.path.join(settings.BASE_DIR, 'cmdb', 'file', client_agent_name)
                remote_file = os.path.join(settings.CLIENT_COLLECT_WIN_DIR, client_agent_name)  # 这个工作路径在setting里配置
                win_ssh.win_scp(local_file, remote_file=remote_file)
                result = win_ssh.win_command('python %s' % remote_file)

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
                    result = {'code': 200, 'msg': '添加云主机windows成功并同步配置'}
                else:
                    result = {'code': 500, 'msg': '采集云主机windows配置失败！错误：%s' % result['msg']}
            else:
                result = {'code': 500, 'msg': 'windows SSH连接异常！错误：%s' % test['msg']}

        return Response(result)


# excel导入数据主机
class CloudServerExcelCreateHostView(APIView):
    # 下载主机导入模板.xlsx
    def get(self, request):
        file_name = 'cloud_server_host.xlsx'
        file_path = os.path.join(settings.BASE_DIR, 'cmdb', 'file', file_name)
        # 通过二进制流式方式打开
        response = FileResponse(open(file_path, 'rb'))
        # 指定下载的格式
        response['Content-Type'] = 'application/octet-stream'
        # 设置下载时看到的文件名称
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name
        # result = {'code': 200, 'msg': '获取文件成功'}
        return response

    # 导入excel
    def post(self,request, *args, **kwargs):
        # 获取前端提交数据
        idc_id = int(request.data.get('idc'))
        server_group_id = request.data.get('server_group')
        excel_file_obj = request.data['file']

        # 直接自定义分隔符，把字符串转换为列表格式
        server_group_list_id = server_group_id.split(',')

        # 判断读取是否是excel文件
        try:
            data = xlrd.open_workbook(file_contents=excel_file_obj.read(), filename=None)
        except Exception:
            result = {'code': 500, 'msg': '请上传Excel文件！'}
            return Response(result)

        idc = Idc.objects.get(id=idc_id)
        # 打开第一个工作表
        table = data.sheets()[0]
        # 获取表的行数
        nrows = table.nrows

        try:
            # 循环行提取数据
            for i in range(nrows):
                if i != 0:   # 跳过标题行
                    # 获取每一行的每一列数据
                    name = table.row_values(i)[0]
                    hostname  = table.row_values(i)[1]
                    machine_type = table.row_values(i)[2]
                    ssh_ip  = table.row_values(i)[3]
                    ssh_port = table.row_values(i)[4]
                    note = table.row_values(i)[5]
                    server = Cloud_Server.objects.create(
                        idc=idc,
                        name=name,
                        hostname=hostname,
                        machine_type=machine_type,
                        ssh_ip=ssh_ip,
                        ssh_port=ssh_port,
                        note=note
                    )
                    # 添加多对多字段
                    for group_id in server_group_list_id:
                        group = ServerGroup.objects.get(id=group_id)   # 获取分组
                        server.server_group.add(group)   # 将服务器添加到分组
            result = {'code': 200, 'msg': '导入成功'}

        except  Exception as e:
            result = {'code': 500, 'msg': '导入异常！%s' % e}

        return Response(result)


# 获取阿里云主机信息
class AliyunCloudView(APIView):
    """
    阿里云获取云主机信息
    """

    # 获取地区(region)
    def get(self, request):
        # 获取用户提交的id和key
        secret_id = request.query_params.get('secret_id')
        secret_key = request.query_params.get('secret_key')
        cloud = AliCloud(secret_id, secret_key)
        result = cloud.region_list()
        print(result)

        if result['code'] == 200:
            data = []
            for i in result['data']['Regions']['Region']:
                rg = {'region_id': i['RegionId'], 'region_name': i['LocalName']}
                data.append(rg)

            res = {'code': 200, 'msg': '获取区域列表成功', 'data': data}
        else:
            res = {'code': 500, 'msg': result['msg']}

        return Response(res)

    # 阿里云导入功能
    def post(self, request, *args, **kwargs):
        """
          根据区域名称创建机房，再导入云主机（绑定机房）到数据库
        """
        # 凭据、IDC机房、主机分组、SSH连接地址（IP、端口）
        secret_id = request.data.get('secret_id')
        secret_key = request.data.get('secret_key')
        server_group_id = request.data.get('server_group')
        region_id = request.data.get('region')        # 区域用于机房里的城市
        ssh_ip = request.data.get('ssh_ip')          # 用户选择使用内网（private）还是公网（public），下面判断对应录入
        ssh_port = request.data.get('ssh_port')


        cloud = AliCloud(secret_id, secret_key)
        result = cloud.instance_list(region_id)

        if result['code'] == 200:
            instance_list = result['data']['Instances']['Instance']
            if len(instance_list) == 0:
                res = {'code': 500, 'msg': '该区域未发现云主机，请重新选择'}
                return Response(res)
        else:
            res = {'code': 500, 'msg': result['msg']}
            return Response(res)

        # 根据地区获取可用区
        zone_result = cloud.zone_list(region_id)
        zone_dict = {}    # cn-chengdu-a  成都A区  可用区
        for i in zone_result['data']['Zones']['Zone']:
            zone_dict[i['ZoneId']] = i['LocalName']

        # 获取主机所在可用区
        # 可用区用于机房里的机房名称
        zone_set = set()
        for host in instance_list:
            zone = host['ZoneId']        # 可用区，例如：ap-beijing-1
            zone_set.add(zone_dict[zone])   # 获取中文名

        # 根据可用区创建机房
        for zone in zone_set:
            # 如果存在不创建
            idc = Idc.objects.filter(name=zone)
            if not idc:
                # 获取region的中文名
                region_list = cloud.region_list()['data']['Regions']['Region']
                for r in region_list:
                    if r['RegionId'] == region_id:
                        city = r['LocalName']


                Idc.objects.create(
                    name=zone,
                    city=city,
                    provider="阿里云",
                )

        # 导入云主机信息到数据库
        for host in instance_list:
            zone = host['ZoneId']
            instance_id = host['InstanceId']  # 实例ID
            # hostname = host['HostName']         # 主机名称
            instance_name = host['InstanceName']   # 机器名称
            os_version = host['OSName']         # 系统版本
            machine_type = host['OSType']       # 获取机器类型

            # 获取私有IP
            private_ip_list =  host['NetworkInterfaces']['NetworkInterface'][0]['PrivateIpSets']['PrivateIpSet']
            private_ip = []
            for ip in private_ip_list:
                private_ip.append(ip['PrivateIpAddress'])

            # 获取公网IP
            public_ip = host['PublicIpAddress']['IpAddress']
            cpu = "%s核" %host['Cpu']
            memory = "%sG" %(int(host['Memory']) / 1024 )

            # 硬盘信息需要单独获取
            disk = []
            disk_list = cloud.instance_disk(region_id, instance_id)['data']['Disks']['Disk']
            for d in disk_list:
                disk.append({'device': d['Device'], 'size': '%sG' % d['Size'], 'type': d['Category']})

            # 获取时间,2022-01-30T04:51Z 由于时间格式显示不对，需要转换才能存储
            # 创建时间
            create_date = time.strftime("%Y-%m-%d", time.strptime(host['CreationTime'], "%Y-%m-%dT%H:%MZ"))

            # 过期时间
            expired_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(host['ExpiredTime'], "%Y-%m-%dT%H:%MZ"))


            # 配置选择ssh ip
            if ssh_ip == "public":
                ssh_ip = public_ip[0]
            elif ssh_ip == "private":
                ssh_ip = private_ip[0]

            # 创建服务器
            zone = host['ZoneId']
            idc_name = zone_dict[zone]
            idc = Idc.objects.get(name=idc_name) # 一对多

            data = {'idc': idc,
                    'name': instance_name,
                    'hostname': instance_id,
                    'ssh_ip': ssh_ip,
                    'ssh_port': ssh_port,
                    'machine_type': machine_type,
                    'os_version': os_version,
                    'public_ip': public_ip,
                    'private_ip': private_ip,
                    'cpu_num': cpu,
                    'memory': memory,
                    'disk': disk,
                    'put_shelves_date': create_date,
                    'expire_datetime': expired_time,
                    'is_verified': 'verified'}
            # 如果instance_id不存在才创建
            server = Cloud_Server.objects.filter(hostname=instance_id)
            if not server:
                server = Cloud_Server.objects.create(**data)   # 创建服务表
                # 分组多对多
                group = ServerGroup.objects.get(id=server_group_id)    # 根据id查询分组
                server.server_group.add(group)       # 将服务器添加到分组
            else:
                server.update(**data)  # 更新

        res = {'code': 200, 'msg': '导入云主机成功'}
        return Response(res)

# 获取腾讯云主机信息
class TencentCloudView(APIView):
    """
    腾讯云获取云主机信息
    """

    # 获取地区(region)
    def get(self, request):
        # 获取用户提交的id和key
        secret_id = request.query_params.get('secret_id')
        secret_key = request.query_params.get('secret_key')
        cloud = TCloud(secret_id, secret_key)
        result = cloud.region_list()

        if result.code == 200:
            data = []
            for i in result.RegionSet:
                rg = {'region_id': i.Region, 'region_name': i.RegionName}
                data.append(rg)

            res = {'code': 200, 'msg': '获取区域列表成功', 'data': data}
        else:
            res = {'code': 500, 'msg': result['msg']}

        return Response(res)

    # 腾讯云导入功能
    def post(self, request, *args, **kwargs):
        """
          根据区域名称创建机房，再导入云主机（绑定机房）到数据库
        """
        # 凭据、IDC机房、主机分组、SSH连接地址（IP、端口）
        secret_id = request.data.get('secret_id')
        secret_key = request.data.get('secret_key')
        server_group_id = request.data.get('server_group')
        region_id = request.data.get('region')        # 区域用于机房里的城市
        ssh_ip = request.data.get('ssh_ip')          # 用户选择使用内网（private）还是公网（public），下面判断对应录入
        ssh_port = request.data.get('ssh_port')


        cloud = TCloud(secret_id, secret_key)
        result = cloud.instance_list(region_id)

        # 判断区域里面是否有实例主机
        if result.code == 200:
            instance_list = result.InstanceSet
            if len(instance_list) == 0:
                res = {'code': 500, 'msg': '该区域未发现云主机，请重新选择'}
                return Response(res)
        else:
            res = {'code': 500, 'msg': result['msg']}
            return Response(res)

        # 根据地区获取可用区
        zone_result = cloud.zone_list(region_id)
        zone_dict = {}    # cn-chengdu-a  成都A区  可用区
        for i in zone_result.ZoneSet:
            zone_dict[i.Zone] = i.ZoneName

        # 获取主机所在可用区
        # 可用区用于机房里的机房名称
        zone_set = set()
        for host in instance_list:
            zone = host.Placement.Zone        # 可用区，例如：ap-shanghai-2
            zone_set.add(zone_dict[zone])   # 获取中文名

        # 根据可用区创建机房
        for zone in zone_set:
            # 如果存在不创建
            idc = Idc.objects.filter(name=zone)
            if not idc:
                # 获取region的中文名
                region_list = cloud.region_list().RegionSet
                for r in region_list:
                    if r.Region == region_id:
                        city = r.RegionName


                Idc.objects.create(
                    name=zone,
                    city=city,
                    provider="腾讯云",
                )

        # 导入云主机信息到数据库
        for host in instance_list:
            zone = host.Placement.Zone
            instance_id = host.InstanceId # 实例ID
            # hostname = host.InstanceName       # 主机名称
            instance_name = host.InstanceName   # 机器名称
            os_version = host.OsName        # 系统版本


            # 获取私有IP
            private_ip = host.PrivateIpAddresses

            # 获取公网IP
            public_ip = host.PublicIpAddresses

            # 获取cpu
            cpu = "%s核" %host.CPU

            # 获取内存
            memory = "%sG" %host.Memory

            Os_Type = "%s" %host.OsName
            Os_Type = Os_Type[:7]
            if Os_Type == 'Windows':
                machine_type = 'windows'
            else:
                machine_type = 'linux'

            # 获取最大带宽
            network_out = "%sM" %host.InternetAccessible.InternetMaxBandwidthOut

            # 硬盘信息需要单独获取
            disk = [{'device': 'None', 'size': '%sG' %host.SystemDisk.DiskSize, 'type': host.SystemDisk.DiskType}]  # 默认保存是系统盘
            DataDisks_list = host.DataDisks
            if DataDisks_list:
                for d in DataDisks_list:
                    disk.append({'device': 'None', 'size': '%sG' %d.DiskSize, 'type': d.DiskType})

            create_date = time.strftime("%Y-%m-%d", time.strptime(host.CreatedTime, "%Y-%m-%dT%H:%M:%SZ"))

            expired_time = host.ExpiredTime
            if expired_time == None:
                expired_time = time.strftime("%Y-%m-%d", time.strptime(host.CreatedTime, "%Y-%m-%dT%H:%M:%SZ"))
            else:
                expired_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(host.ExpiredTime, "%Y-%m-%dT%H:%M:%SZ"))

            # 配置选择ssh ip
            if ssh_ip == "public":
                ssh_ip = public_ip[0]     # 使用第一个IP连接
            elif ssh_ip == "private":
                ssh_ip = private_ip[0]

            # 创建服务器
            idc_name = zone_dict[zone]
            idc = Idc.objects.get(name=idc_name) # 一对多

            data = {'idc': idc,
                    'name': instance_name,
                    'hostname': instance_id,
                    'ssh_ip': ssh_ip,
                    'ssh_port': ssh_port,
                    'machine_type': machine_type,
                    'os_version': os_version,
                    'public_ip': public_ip,
                    'private_ip': private_ip,
                    'network': network_out,
                    'cpu_num': cpu,
                    'memory': memory,
                    'disk': disk,
                    'put_shelves_date': create_date,
                    'expire_datetime': expired_time,
                    'is_verified': 'verified'}
            # 如果instance_id不存在才创建
            server = Cloud_Server.objects.filter(hostname=instance_id)
            if not server:
                server = Cloud_Server.objects.create(**data)   # 创建服务表
                # 分组多对多
                group = ServerGroup.objects.get(id=server_group_id)    # 根据id查询分组
                server.server_group.add(group)       # 将服务器添加到分组
            else:
                server.update(**data)  # 更新

        res = {'code': 200, 'msg': '导入云主机成功'}
        return Response(res)

