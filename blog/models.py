from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)   # when created, 
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True)

    image = models.ImageField(upload_to="blog_images")

    date_created = models.DateTimeField(auto_now_add=True)  # when created, 
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.blog)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # models.OneToOneRel
    phone = models.CharField(max_length=15, unique=True)
    address_1 = models.TextField()
    address_2 = models.TextField()

    def __str__(self):
        return self.user.username
