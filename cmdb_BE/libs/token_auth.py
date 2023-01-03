############### 导入user认证的token认证模块 ######################
from rest_framework.authtoken.views import ObtainAuthToken     # 导入authtoken认证模块
from rest_framework.authtoken.models import Token              # 导入Token
from rest_framework.response import Response          # 导入Response的json返回格式

############### 导入user修改密码模块 #################
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import AllowAny

# 登陆认证
class CustomAuthToken(ObtainAuthToken):
    permission_classes = (AllowAny,)  # AllowAny 允许所有用户（登录不需要身份认证）
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            res = {'code': 200,'msg': '认证成功','token': token.key,'username': user.username,}
            return Response(res)
        else:
            res = {'code': 500,'msg': '用户名或密码错误！',}
            return Response(res)
# 修改密码
class ChangeUserPasswordView(APIView):
    def post(self, request, *args, **kwargs):

        # 获取用户名
        username = request.data.get("username")

        # 获取旧密码和新密码
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        try:
            user = User.objects.get(username=username)
        except:
            res = {'code': 500, 'msg': '用户不存在！'}
            return Response(res)

        if check_password(old_password, user.password):
            user.password = make_password(new_password)
            user.save()
            res = {'code': 200, 'msg': '修改密码成功'}
        else:
            res = {'code': 500, 'msg': '原密码不正确！'}
        return Response(res)