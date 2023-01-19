from django.urls import path, include

# 导入视图集
from cmdb.views import IdcViewSet, ServerGroupViewSet, CloudServerViewSet, PhysicsServerViewSet, VmServerViewSet, \
    CloudServerCreateHostView, CloudServerExcelCreateHostView, AliyunCloudView, TencentCloudView, \
    CloudServerHostCollectView,PhysicsServerCreateHostView,PhysicsServerExcelCreateHostView,PhysicsServerHostCollectView

# 导入drf路由
from rest_framework import routers

router = routers.DefaultRouter()

# 注册视图集到路由
router.register('idc', IdcViewSet, basename="idc")
router.register('server_group', ServerGroupViewSet, basename="server_group")
router.register('cloud_server', CloudServerViewSet, basename="cloud_server")
router.register('physics_server', PhysicsServerViewSet, basename="physics_server")
router.register('vm_server', VmServerViewSet, basename="vm_server")

urlpatterns = [
    path('', include(router.urls)),
    path('cloud_server_create_host/', CloudServerCreateHostView.as_view()),  # 配置新建云主机单台数据采集同步接口
    path('cloud_server_excel_create_host/', CloudServerExcelCreateHostView.as_view()),  # 配置excel导入和模板下载
    path('aliyun_cloud/', AliyunCloudView.as_view()),  # 阿里云数据信息同步接口
    path('tencent_cloud/', TencentCloudView.as_view()),  # 腾讯云数据信息同步接口
    path('cloud_server_host_collect/', CloudServerHostCollectView.as_view()),  # 配置云服务器主机同步功能
    path('physics_server_create_host/', PhysicsServerCreateHostView.as_view()),  # 配置新建物理主机单台数据采集同步接口
    path('physics_server_excel_create_host/', PhysicsServerExcelCreateHostView.as_view()),  # 配置物理机主机excel导入和模板下载
    path('physics_server_host_collect/', PhysicsServerHostCollectView.as_view()),  # 配置物理主机服务器主机同步功能
]
