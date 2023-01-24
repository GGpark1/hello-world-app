"""
Serializers for the user API View
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        # 암호화된 Password(validated_data['password'])를 DB에 저장하고,
        # 암호화된 Password로 만들어진 객체를 return한다.
        # validated_data가 생성된 경우에만(=유효성 검증을 통과한 경우) user 객체를 생성한다.
        return get_user_model().objects.create_user(**validated_data)