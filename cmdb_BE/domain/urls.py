from django.urls import path, include

# 导入视图集
from domain.views import DomainManageViewSet, DomainAnalysisViewSet

# 导入drf路由
from rest_framework import routers

router = routers.DefaultRouter()

# 注册视图集到路由
router.register('domain_manage', DomainManageViewSet, basename="domain_manage")
router.register('domain_analysis', DomainAnalysisViewSet, basename="domain_analysis")


urlpatterns = [
    path('', include(router.urls)),
]
