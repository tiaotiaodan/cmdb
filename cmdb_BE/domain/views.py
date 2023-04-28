# 导入modelviewset视图模型
from libs.custom_model_view_set import CustomModelViewSet

# 导入模型
from domain.models import DomainManage, DomainAnalysis

# 导入序列化
from domain.serializers import DomainManageSerializer, DomainAnalysisSerializer

# 导入过滤、搜索和排序插件
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# 导入drf返回 Response模块
from rest_framework.response import Response

# 导入APIView
from rest_framework.views import APIView

# 导入调用阿里云模块
from libs.aliyun_cloud import AliCloud

import os, json, time

# 域名管理视图
class DomainManageViewSet(CustomModelViewSet):
    queryset = DomainManage.objects.all()      # 导入模型类所有数据
    serializer_class =  DomainManageSerializer   # 序列化数据

    # 导入模块，filters.SearchFilter 是指搜索, filters.OrderingFilter 是指排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    filterset_fields = ('name', 'platform')  # 指定可过滤的字段
    search_fields = ('name', 'platform')  # 指定可搜索的字段

    # 排序
    # 注意 filter_backends多了一个filters.OrderingFilter
    ordering_fields = ["id", "name"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            res = {'code': 200, 'msg': '删除成功'}
        except Exception as e:
            res = {'code': 500, 'msg': '该IDC机房管理关联其他应用，请删除关联的应用再操作'}
        return Response(res)

# 域名解析视图
class DomainAnalysisViewSet(CustomModelViewSet):
    queryset = DomainAnalysis.objects.all()      # 导入模型类所有数据
    serializer_class =  DomainAnalysisSerializer   # 序列化数据

    # 导入模块，filters.SearchFilter 是指搜索, filters.OrderingFilter 是指排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    filterset_fields = ('id', 'host_name', 'analyshost')  # 指定可过滤的字段
    search_fields = ('id', 'host_name', 'analyshost')  # 指定可搜索的字段

    # 排序
    # 注意 filter_backends多了一个filters.OrderingFilter
    ordering_fields = ["id", "domain_name"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            res = {'code': 200, 'msg': '删除成功'}
        except Exception as e:
            res = {'code': 500, 'msg': '该域名管理关联其他，请删除关联的应用再操作'}
        return Response(res)


class AliyunCloudDomainManageView(APIView):
    """
    阿里云获取域名管理信息
    """
    def post(self, request):
        """
        根据获取云平台域名，再导入域名到数据库
        """
        # 凭据
        secret_id = request.data.get('secret_id')
        secret_key = request.data.get('secret_key')
        cloud = request.data.get('cloud')



        # 导入阿里云sdk
        Alicloud = AliCloud(secret_id, secret_key)

        # 调用域名管理
        domain_result =  Alicloud.instance_domain(0, 200)

        # 获取指定数据
        result_list = domain_result['data']['TotalItemNum']

        for i in range(result_list):

            # 域名名称
            name = domain_result['data']['Data']['Domain'][i].get('DomainName')

            # 时间设置
            create_time = domain_result['data']['Data']['Domain'][i].get('RegistrationDate')
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(create_time, "%Y-%m-%d %H:%M:%S"))

            # 2022-01-30T04:51Z 需要转换才能存储
            expire_time = domain_result['data']['Data']['Domain'][i].get('ExpirationDate')
            expire_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(expire_time, "%Y-%m-%d %H:%M:%S"))

            # 过期剩余天数
            ExpirationTime = int(domain_result['data']['Data']['Domain'][i].get('ExpirationCurrDateDiff'))

            ExpirationDateStatus = int(domain_result['data']['Data']['Domain'][i].get('ExpirationDateStatus'))

            # 域名状态

            status_list = int(domain_result['data']['Data']['Domain'][i].get('DomainStatus'))
            status_name = []
            if status_list == 1:
                status = "急需续费"
                status_name.append(status)
            elif status_list == 2:
                status = "急需赎回"
                status_name.append(status)
            elif status_list == 3:
                status = "正常"
                status_name.append(status)
            elif status_list == 4:
                status = "转出中"
                status_name.append(status)
            elif status_list == 5:
                status = "域名持有者信息修改中"
                status_name.append(status)
            elif status_list == 6:
                status = "未实名认证"
                status_name.append(status)
            elif status_list == 7:
                status = "实名认证失败"
                status_name.append(status)
            elif status_list == 8:
                status = "实名认证审核中"
                status_name.append(status)
            else:
                status = "没有获取到"
                status_name.append(status)
            status = status_name[0]


            data = {'name': name,
                    'platform': cloud,
                    'status': status,
                    'create_time': create_time,
                    'expire_time': expire_time,
                    'ExpirationTime': ExpirationTime,
                    'ExpirationDateStatus': ExpirationDateStatus,}

            # 如果instance_id不存在才创建
            server = DomainManage.objects.filter(name=name)
            if not server:
                DomainManage.objects.create(**data)

            else:
                server.update(**data)

        res = {'code': 200, 'msg': '导入域名成功'}
        return Response(res)


class AliyunCloudDomainAnalysisView(APIView):
    """
    阿里云获取域名解析管理信息
    """
    def post(self, request):
        """
        根据获取云平台域名，再导入域名到数据库
        """
        # 凭据
        secret_id = request.data.get('secret_id')
        secret_key = request.data.get('secret_key')
        domain_manage_id = int(request.data.get('cloudDomainId'))
        note = request.data.get('note')

        # 通过前端上传id查询域名名称
        domain_manage = DomainManage.objects.get(id=domain_manage_id)
        domain_name = domain_manage.name
        print(domain_name)

        # 导入阿里云sdk
        cloud = AliCloud(secret_id, secret_key)

        domain_result = cloud.instance_domain_analysis(domain_name)


        # 获取指定数据条数
        result_list = domain_result['data']['TotalCount']
        print(result_list)
        for i in range(result_list):

            # 主机记录
            host_name = domain_result['data']['DomainRecords']['Record'][i].get('RR')
            RecordType = domain_result['data']['DomainRecords']['Record'][i].get('Type')
            analyshost = domain_result['data']['DomainRecords']['Record'][i].get('Value')
            host_status = domain_result['data']['DomainRecords']['Record'][i].get('Status')

            data = {'domain_name_id': domain_manage_id,
                    'host_name': host_name,
                    'RecordType': RecordType,
                    'analyshost': analyshost,
                    'host_status': host_status,
                    'note': note}

            # 进行数据库多级判断是否导入数据一致，
            server = DomainAnalysis.objects.filter(domain_name_id=domain_manage_id).filter(host_name=host_name).filter(analyshost=analyshost)
            if not server:
                DomainAnalysis.objects.create(**data)
            else:
                server.update(**data)

        res = {'code': 200, 'msg': '导入域名解析成功'}
        return Response(res)