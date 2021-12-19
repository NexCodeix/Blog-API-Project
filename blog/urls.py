from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path("", views.IndexPageView.as_view(), name="index_page"),
    path("content_create/", views.BlogCreationView.as_view(), name="content_create"),
    path("content_update/<int:pk>/", views.BlogUpdateView.as_view(), name="content_update"),
    path("details/<int:id>/", views.BlogDetailView.as_view(), name="content_detail"),
    path("delete/<int:number>/", views.blog_delete, name="content_delete"),

    # path("user/login/", views.login_user),
    path("user/login/", LoginView.as_view(template_name="user/login.html"), ),
    path("user/phone/login/", views.login_with_phone),
    path("user/logout/", views.logout_user, ),
    path("user/register/", views.register_user, ),

    path("send_mail", views.send_mail_to_someone),

    path("accounts/password_changed/", PasswordChangeView.as_view(), name="password_change"),
    path("accounts/password_change/done/", views.password_change_done, name="password_change_done"),

    path("accounts/user/reset/", PasswordResetView.as_view(), name="password_reset"),
    path("accounts/user/reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),

    path("accounts/password-reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("accounts/password-reset/done/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path("js/response/", views.give_js_response, name="js-response"),
    path("js/post/", views.create_blog_through_js),

]
