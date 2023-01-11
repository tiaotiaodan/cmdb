from django.urls import path, include

# 导入视图集
from cmdb.views import IdcViewSet, ServerGroupViewSet, CloudServerViewSet, PhysicsServerViewSet, VmServerViewSet, CloudServerCreateHostView

# 导入drf路由
from rest_framework import routers
router = routers.DefaultRouter()

# 注册视图集到路由
router.register('idc', IdcViewSet, basename="idc")
router.register('server_group',ServerGroupViewSet, basename="server_group")
router.register('cloud_server',CloudServerViewSet, basename="cloud_server")
router.register('physics_server',PhysicsServerViewSet, basename="physics_server")
router.register('vm_server',VmServerViewSet, basename="vm_server")

urlpatterns = [
    path('', include(router.urls)),
    path('cloud_server_create_host/', CloudServerCreateHostView.as_view()), # 配置新建主机数据采集同步接口
]
