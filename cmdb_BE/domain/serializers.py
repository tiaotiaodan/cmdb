# 导入数据模型
from domain.models import DomainManage, DomainAnalysis

# 导入虚拟化工具
from rest_framework import serializers


class DomainManageSerializer(serializers.ModelSerializer):
    """
    DomainManage 域名管理序列化
    """

    class Meta:
        model = DomainManage
        fields = "__all__"
        read_only_fields = ("id",)  # 仅用于序列化（只读）字段，反序列化(更新)可不传



class DomainAnalysisSerializer(serializers.ModelSerializer):
    """
    DomainAnalysis 域名解析序列化类
    """

    class Meta:
        model = DomainAnalysis
        fields = "__all__"
        read_only_fields = ("id",)  # 仅用于序列化（只读）字段，反序列化(更新)可不传