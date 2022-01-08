from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from ..models import Blog
from .serializers import BlogSerializer, BlogDetailSerializer

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .pagination import LargeResultsSetPagination


@api_view(http_method_names=["GET", ])
def blog_list_api_view(request):
    # if request.method == "POST":
    #     pass
    qs = Blog.objects.all()
    serialized = BlogSerializer(instance=qs, many=True)
    data = serialized.data
    return Response(data, status.HTTP_200_OK)


class BlogListCreateAPIView(ListCreateAPIView):
    serializer_class = BlogSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        qs = Blog.objects.all()
        return qs

    # def get(self, *args, **kwargs):
    #     qs = self.get_queryset()
    #     serialized = BlogSerializer(instance=qs, many=True)
    #     data = serialized.data

    #     return Response(data, status.HTTP_200_OK)

    # def create(self, *args, **kwargs):
    #     data = self.request.data  # Requested Data from Forms
    #     data["user"] = user.pk

    #     serialized = BlogSerializer(data=data)
    #     if serialized.is_valid():
    #         self.perform_create(serializer)
    #         serialized.save()
    #         data = serialized.data
    #         print(data)
    #         return Response(data, status.HTTP_201_CREATED)
    #     else:
    #         return Response(serialized.error_messages, status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BlogRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BlogDetailSerializer
    lookup_url_kwarg = "id"

    def get_object(self):
        url_id = self.kwargs.get(self.lookup_url_kwarg)
        try:
            obj = Blog.objects.get(id=url_id)
        except ObjectDoesNotExist:
            raise NotFound("Blog with this is not found")

        return obj


@api_view(http_method_names=["GET", ])
def blog_detail_api_view(request, pk):
    # if request.method == "POST":
    #     pass

    print("FROM VIEW REQUEST METHOD ", request.method)
    try:
        obj = Blog.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response("data not Found", status.HTTP_404_NOT_FOUND)
    serialized = BlogDetailSerializer()
    serialized.context["request"] = request
    serialized.instance = obj
    data = serialized.data
    return Response(data, status.HTTP_200_OK)


@api_view(http_method_names=["POST", ])
def blog_create_api_view(request):
    user = request.user
    if not user.is_authenticated:
        return Response("User UNAUTHORIZED", status.HTTP_401_UNAUTHORIZED)

    """
    {
        "title": "new Title",
        "content": "new Content",
    }
    """

    data = request.data  # Requested Data from Forms
    data["user"] = user.pk
    
    serialized = BlogSerializer(data=data)
    if serialized.is_valid():
        serialized.save()
        data = serialized.data
        print(data)
        return Response(data, status.HTTP_201_CREATED)
    else:
        return Response(serialized.error_messages, status.HTTP_400_BAD_REQUEST)



@api_view(http_method_names=["GET", "PUT"])
def blog_update_api_view(request, pk):
    qs = Blog.objects.filter(pk=pk)
    if not qs.exists():
        return Response("Blog not Found", status.HTTP_404_NOT_FOUND)

    blog = qs.get()

    if request.method == "PUT":
        user = request.user
        if not user.is_authenticated:
            return Response("User UNAUTHORIZED", status.HTTP_401_UNAUTHORIZED)

        """
        {
            "title": "new Title",
            "content": "new Content",
        }
        """

        data = request.data  # Requested Data from Forms
        data["user"] = user.pk
        serialized = BlogSerializer(instance=blog, data=data)
        if serialized.is_valid():
            serialized.save()
            data = serialized.data
            print(data)
            return Response(data, status.HTTP_200_OK)
        else:
            return Response(serialized.error_messages, status.HTTP_400_BAD_REQUEST)

    serialized = BlogSerializer(instance=blog)
    return Response(serialized.data, status.HTTP_200_OK)