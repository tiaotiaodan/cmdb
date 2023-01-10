from django.shortcuts import render


# 导入modelviewset视图模型
from libs.custom_model_view_set import CustomModelViewSet

# 导入模型
from system_config.models import Credential

# 导入序列化
from system_config.serializers import CredentialSerializer

# 导入过滤、搜索和排序插件
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class CredentialViewSet(CustomModelViewSet):
    queryset = Credential.objects.all()      # 导入模型类所有数据
    serializer_class =  CredentialSerializer   # 序列化数据

    # 导入模块，filters.SearchFilter 是指搜索, filters.OrderingFilter 是指排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    filterset_fields = ('name',)  # 指定可过滤的字段
    search_fields = ('name',)  # 指定可搜索的字段

    # 排序
    # 注意 filter_backends多了一个filters.OrderingFilter
    ordering_fields = ["id", "name"]