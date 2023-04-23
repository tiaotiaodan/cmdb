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