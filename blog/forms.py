from django import forms
from .models import Blog, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Validation check --> 1. Object level validation, 2. Full validation


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        # fields = "__all__"
        exclude = ["user", ]

    def clean_content(self):
        print("Validating content inside forms")
        content = self.cleaned_data.get("content")
        print(content)

        if "django" not in content:
            raise forms.ValidationError("Blog is not about Django")

        return content

    def clean_title(self):
        title = self.cleaned_data.get("title")
        # user = self.cleaned_data.get("user")  # it is none
        user = self.instance.user  # Since we made it in view as form.instance.user = request.user
        print("User ", user)
        print("Title ", title)

        qs = Blog.objects.filter(user=user, title=title)
        if qs.exists():
            raise forms.ValidationError("User has already created a blog of this title")

        return title



class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        if not qs.exists():
            raise forms.ValidationError("Username not found")
        return username

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        auth = authenticate(username=username, password=password) # return user object
        if not auth:
            raise forms.ValidationError("Username and Password did not match")       

        return password


class LoginWithPhoneForm(forms.Form):
    phone = forms.CharField(max_length=150)
    password = forms.CharField()




class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password")
    password2 = forms.CharField(label="Confirm Password")

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username Already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email Already exists")
        return email

    
    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")

        if p1 != p2:
            raise forms.ValidationError("Both Password didn't match")

        return p2