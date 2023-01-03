# 导入数据模型
from cmdb.models import Idc, ServerGroup, Cloud_Server, Physics_Server, Vm_Server

# 导入虚拟化工具
from rest_framework import serializers

class IdcSerializer(serializers.ModelSerializer):
    """
    IDC 机房序列化类
    """
    class Meta:
        model = Idc
        fields = "__all__"
        read_only_fields = ("id",)   # 仅用于序列化（只读）字段，反序列化(更新)可不传

class ServerGroupSerializer(serializers.ModelSerializer):
    """
    主机分组序列化类
    """
    class Meta:
        model = ServerGroup
        fields = "__all__"
        read_only_fields = ("id",)   # 仅用于序列化（只读）字段，反序列化(更新)可不传


class CloudServerSerializer(serializers.ModelSerializer):
    """
    主机分组序列化类
    """
    class Meta:
        model = Cloud_Server
        fields = "__all__"
        read_only_fields = ("id",)   # 仅用于序列化（只读）字段，反序列化(更新)可不传


class PhysicsServerSerializer(serializers.ModelSerializer):
    """
    主机分组序列化类
    """
    class Meta:
        model = Physics_Server
        fields = "__all__"
        read_only_fields = ("id",)   # 仅用于序列化（只读）字段，反序列化(更新)可不传

class VmServerSerializer(serializers.ModelSerializer):
    """
    主机分组序列化类
    """
    class Meta:
        model = Vm_Server
        fields = "__all__"
        read_only_fields = ("id",)   # 仅用于序列化（只读）字段，反序列化(更新)可不传