"""
Views for the user API
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticate user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retreive and return the authenticated user"""
        # Endpoint에 접근하면 인증된 user의 객체를 반환함
        # 반환된 user 객체에 대해 update 작업을 진행함
        return self.request.user


# ObtainAuthToken을 사용하면 Token model을 상속함
# Serializer만 설정하면, 해당 serializer 안에서 validation을 check하고,
# 생성된 Token을 Token model 안에 저장함
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    #Browser API를 사용하지 않고 Header를 통해 인증정보를 전송하도록 설정
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES