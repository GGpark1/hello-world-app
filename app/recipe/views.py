"""
Views for the recipe APIs
"""
from rest_framework import (viewsets,
                            mixins,
                            status,)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (Recipe,
                         Tag,
                         Ingredient)
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        # 모든 list를 반환하지 않고,
        # 요청한 사용자와 관련된 list만 반환하도록 get_queryset를 오버라이딩함
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request"""
        # detail request가 입력될 시 return되는 serializer를 재정의함
        # list 외에 모든 작업(delete, put, patch)는 detail serializer에서 이뤄지기 떄문에,
        # defualt serializer_class를 detail로 설정함
        # 클래스 객체를 반환하는 게 아니라 참조할 클래스를 명시하는 것이기 때문에 '()'를 붙이지 않음
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action =='upload_image':
            #viewset에 get_serializer_class()에서 사용할 수 있는 action이 정의되어 있음
            #정의되어 있지 않은 action은 action 모듈을 Import하여 새롭게 정의해야 함
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    # viewset은 사전에 정의된 url_path가 있기 때문에 request로 입력되는 endpoint와 action을 연결하기 위해
    # url_path를 지정해주어야 함
    def upload_image(self, request, pk=None):
        """Upload an image to recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseRecipeAttrViewSet(mixins.ListModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    """Base viewset for recipe atrributes"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()