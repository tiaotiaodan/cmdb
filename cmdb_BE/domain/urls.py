from django.urls import path, include

# 导入视图集
from domain.views import DomainManageViewSet, DomainAnalysisViewSet,AliyunCloudDomainManageView,AliyunCloudDomainAnalysisView,TenCentCloudDomainManageView, TenCentCloudDomainAnalysisView

# 导入drf路由
from rest_framework import routers

router = routers.DefaultRouter()

# 注册视图集到路由
router.register('domain_manage', DomainManageViewSet, basename="domain_manage")
router.register('domain_analysis', DomainAnalysisViewSet, basename="domain_analysis")


urlpatterns = [
    path('', include(router.urls)),
    path('ali_domain_manage_create/', AliyunCloudDomainManageView.as_view()),  # 配置新建阿里云域名导入
    path('ali_domain_analysis_create/', AliyunCloudDomainAnalysisView.as_view()),  # 配置新建云域名解析导入
    path('tencent_domain_manage_create/', TenCentCloudDomainManageView.as_view()),  # 配置新建腾讯云域名导入
    path('tencent_domain_analysis_create/', TenCentCloudDomainAnalysisView.as_view()),  # 配置新建腾讯云域名解析导入
]
