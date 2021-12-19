from django.urls import path
from . import views

urlpatterns = [
    path("blog-list/", views.blog_list_api_view, ),
    path("blog-detail/<pk>/", views.blog_detail_api_view, ),
    path("blog-create/", views.blog_create_api_view),
    path("blog-update/<pk>/", views.blog_update_api_view, )
]
