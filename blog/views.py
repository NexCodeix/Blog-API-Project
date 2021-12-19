from django.core import paginator
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Blog, UserProfile
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse  # JS Object Notation
from .forms import BlogForm, LoginForm, UserRegistrationForm, LoginWithPhoneForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.decorators import login_required

from django.conf import settings

from django.core.mail import send_mail


# CBV, Generic Views
from django.views.generic import ListView, DetailView, UpdateView, CreateView

# Mixin 
from django.contrib.auth.mixins import LoginRequiredMixin


# Login materials
from django.contrib.auth import login, authenticate, logout

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index_page(request):
    qs = Blog.objects.all().order_by("-last_updated")
    paginator = Paginator(qs, 5)

    pages_range = range(1, paginator.num_pages+1)
    print(pages_range)
    page = request.GET.get("page", 1)
    try:
        posts = paginator.page(page)  # returns the Blogs in page 
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    diction = {
        "posts": posts,
        "pages": pages_range,
    }
    return render(request, "main/index.html", context=diction)



class IndexPageView(ListView):
    template_name = "main/index.html"
    context_object_name = "posts"
    
    def get_queryset(self):
        qs = Blog.objects.all()
        return qs



# @login_required
# def Blog_creation(request):
#     print(request.user)  # Current User that is logged in
#     form = BlogForm()
#     if request.method == "POST":
#         form = BlogForm(data=request.POST)
#         form.instance.user = request.user  # We are explicitely setting user of the form to current user

#         if form.is_valid():
#             # self.form_valid(form)
#             obj = form.save()
#             print("Saved")
#             return redirect("Blog_detail", id=obj.id)

#         messages.error(request, "Invalid data provided")
#         print("Invalid data")

#     context = {
#         "form": form,
#     }

#     return render(request, "main/Blog_create.html", context)

class BlogCreationView(LoginRequiredMixin, CreateView):
    template_name = "main/Blog_create.html"
    context_object_name = "form"
    form_class = BlogForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return HttpResponseRedirect(self.success_url)


# @login_required
# def Blog_update(request, pk):
#     obj = Blog.objects.get(pk=pk)

#    # Give a permission denied when other user try to update Blog

#     form = BlogForm(instance=obj)

#     if request.method == "POST":
#         form = BlogForm(data=request.POST, instance=obj)
#         if form.is_valid():
#             form.save()
#             print("Saved")
#             return HttpResponse("<h1>Congrats</h1>")  # task to redirect to detail

#         messages.error(request, "Invalid data provided")
#         print("Invalid data")

#     context = {
#         "form": form,
#     }
#     return render(request, "main/Blog_create.html", context)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "main/Blog_create.html"
    context_object_name = "form"
    form_class = BlogForm
    success_url = "/"
    lookup_url_pk = "pk"

    def get_object(self):
        # self.kwargs  # Dictionary
        Blog_id = self.kwargs.get(self.lookup_url_pk)
        try:
            obj = Blog.objects.get(id=Blog_id)
        except ObjectDoesNotExist:
            return HttpResponse(f"Blog with this Id ({id}) is not found")

        return obj

    def form_valid(self, form):
        # form.instance.user = self.request.user
        form.save()
        return HttpResponseRedirect(self.success_url)

@login_required
def blog_delete(request, number):
    try:
        obj = Blog.objects.get(id=number)
    except ObjectDoesNotExist:
        return HttpResponse(f"Blog with this Id ({number}) is not found To delete")

    # Give a permission denied when other user try to delete Blog


    if request.method == "POST":
        obj.delete()
        # messages.success(request, "Blog has been deleted")
        return redirect("index_page")

    context = {
        "post_obj": obj
    }

    return render(request, "main/Blog_delete.html", context)



def Blog_detail(request, id):
    try:
        obj = Blog.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse(f"Blog with this Id ({id}) is not found")

    addition = 10 + 15

    context = {
        "post_obj": obj,
        "sum": addition,
    }

    return render(request, "main/Blog_detail.html", context)


def addition():
    return 10 + 10


class BlogDetailView(LoginRequiredMixin, DetailView):
    lookup_url_field = "id"
    template_name = "main/Blog_detail.html"
    context_object_name = "post_obj"

    # Detail View.as_view() --> self.get_object()  --> {"post_obj": obj}  --> render(self.template_name)

    def get_object(self):
        # self.kwargs  # Dictionary
        Blog_id = self.kwargs.get(self.lookup_url_field)
        try:
            obj = Blog.objects.get(id=Blog_id)
        except ObjectDoesNotExist:
            return HttpResponse(f"Blog with this Id ({id}) is not found")

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # context --> {}
        # context --> Dictionary
        context["sum"] = addition()
        print(context)
        return context


def login_user(request):
    user = request.user  
    if user.is_authenticated:
        raise PermissionDenied("User is Authenticated")  # Current user that is active in this session
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user_obj = authenticate(username=username, password=password)  # returns user object
            login(request, user_obj)
            print("User has been logged in ", user_obj)
            next = request.GET.get("next")
            print(next)
            if next:
                return redirect(next)
            return redirect("/")

    context = {
        "form": form
    }

    return render(request, "user/login.html", context)


@login_required
def logout_user(request):
    logout(request)
    print("Logged out")
    return redirect(settings.LOGIN_URL)


def register_user(request):
    if request.user.is_authenticated:
        pass  # redirect

    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password2")
            # form.instance.password = password
            user_obj = form.save()  # returns an instance of the model
            user_obj.set_password(password)  # gives a hash password
            user_obj.save()
            print("User is Saved")

            login(request, user_obj)  # logs in the user

            # redirection

    context = {
        "form": form
    }

    return render(request, "user/register.html", context)



# allauth 

def login_with_phone(request):
    form = LoginWithPhoneForm
    if request.method == "POST":
        form = LoginWithPhoneForm(data=request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get("phone")
            password = form.cleaned_data.get("password")
            qs = User.objects.filter(userprofile__phone=phone)
            if not qs.exists():
                raise Http404("Phone Does not Exist")

            obj = qs.get()
            user = authenticate(username=obj.username, password=password)
            if user:
                login(request, user)

            #redirection

    context = {
        "form": form
    }

    return render(request, "user/login_with_phone.html", context)



def send_mail_to_someone(request):
    if request.method == "POST":
        send_mail(
            subject="Testing mail system",
            message="Messaging To Imam and Shovon",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["hossain258@gmail.com", "Shovon.1585@gmail.com"],
        )

    return render(request, "main/send_mail.html")


# user register --> user_verification --> user account verify


@login_required
def password_change_done(request):
    print("Inside Views")
    return redirect("/")


def give_js_response(request):
    dictionary = {
        "function_name": "give_js_response",
        "status": "ok"
    }

    # [{}, {}, {}, {}]

    return JsonResponse([dictionary], safe=False)

import json


@login_required
def create_blog_through_js(request):

    data = request.body
    data = json.loads(data)  # parse --> dict
    print(type(data))

    title = data.get("title")
    text = data.get("text")

    obj = Blog.objects.create(title=title, text=text, user=request.user)
    print("Created Blog", obj)

    return JsonResponse("creating Blog", safe=False)

