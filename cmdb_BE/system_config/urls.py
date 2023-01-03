from django.urls import path, include

# 导入视图集
from system_config.views import CredentialViewSet

# 导入drf路由
from rest_framework import routers
router = routers.DefaultRouter()

# 注册视图集到路由
router.register('credential', CredentialViewSet, basename="credential")

urlpatterns = [
    path('', include(router.urls)),
]
