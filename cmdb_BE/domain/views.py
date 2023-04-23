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

    filterset_fields = ('name',)  # 指定可过滤的字段
    search_fields = ('name','city','provider')  # 指定可搜索的字段

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

    filterset_fields = ('name',)  # 指定可过滤的字段
    search_fields = ('name','city','provider')  # 指定可搜索的字段

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
        platform = request.data.get('platform')

        # 导入阿里云sdk
        cloud = AliCloud(secret_id, secret_key)

        # 调用域名管理
        domain_result =  cloud.instance_domain(0, 200)

        # 获取指定数据
        result_list = domain_result['data']['TotalItemNum']

        for i in range(result_list):
            # 域名名称
            name = domain_result['data']['Data']['Domain'][i].get('DomainName')


            # 域名状态
            status_list = domain_result['data']['Data']['Domain'][i].get('DomainStatus')
            if status_list == 1 :
                status_list = "急需续费"
            elif status_list == 2:
                status_list = "急需赎回"
            elif status_list == 3:
                status_list = "正常"
            elif status_list == 6:
                status_list = "未实名认证"
            elif status_list == 7:
                status_list = "审核失败，重新实名认证"
            elif status_list == 8:
                status_list = "审核中"

            # 时间设置
            create_time = domain_result['data']['Data']['Domain'][i].get('RegistrationDate')
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(create_time, "%Y-%m-%d %H:%M:%S"))

            # 2022-01-30T04:51Z 需要转换才能存储
            expire_time = domain_result['data']['Data']['Domain'][i].get('ExpirationDate')
            expire_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(expire_time, "%Y-%m-%d %H:%M:%S"))

            # 过期剩余天数
            ExpirationTime = domain_result['data']['Data']['Domain'][i].get('ExpirationCurrDateDiff')

            ExpirationDateStatus = domain_result['data']['Data']['Domain'][i].get('ExpirationDateStatus')

            data = {'name': name,
                    'platform': platform,
                    'status': status_list,
                    'create_time': create_time,
                    'expire_time': expire_time,
                    'ExpirationTime': ExpirationTime,
                    'ExpirationDateStatus': ExpirationDateStatus}

            # 如果instance_id不存在才创建
            server = DomainManage.objects.filter(name=name)
            if not server:
                DomainManage.objects.create(**data)

            else:
                server.update(**data)

        res = {'code': 200, 'msg': '导入域名成功'}
        return Response(res)