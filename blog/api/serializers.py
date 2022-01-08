
from ..models import Blog, BlogImage
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied


class BlogSerializer(serializers.ModelSerializer):
    """
    BLOG LIST SERIALIZER
    """
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'

    def validate_title(self, value):
        print(value)
        if len(value) > 15:
            raise PermissionDenied("Length shouldn't be greater than 15")

        return value




class BlogImageListSerializer(serializers.ModelSerializer):
    """
    TASK 
    """

    class Meta:
        model = BlogImage
        fields = '__all__'


class BlogDetailSerializer(serializers.ModelSerializer):
    blogimage_set = BlogImageListSerializer(many=True, read_only=True)
    title_number = serializers.SerializerMethodField(method_name="get_char")

    class Meta:
        model = Blog
        fields = "__all__"

    def get_char(self, obj):
        request = self.context.get("request")  # {"request": view_request }
        print("FROM SERIALIZER REQUEST-> ", request.method)
        print("Title -> ", obj.title)
        length = len(obj.title)
        return length

