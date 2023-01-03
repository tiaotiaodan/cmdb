# 导入序列化组件
from rest_framework import serializers

# 导入数据模型类
from system_config.models import Credential

class CredentialSerializer(serializers.ModelSerializer):
    """
    凭据管理序列化类
    """
    class Meta:
        model = Credential
        fields = "__all__"
        read_only_fields = ("id",)   # 仅用于序列化（只读）字段，反序列化(更新)可不传