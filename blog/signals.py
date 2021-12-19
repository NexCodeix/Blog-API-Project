from .models import Blog
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver

#post save, presave, postdelete, predelete


@receiver(signal=post_save, sender=Blog)   # sender, instance, created, **kwargs
def validate_title_for_blog(sender, instance, created, **kwargs):
    # print("Inside signals of blog")
    # print(sender, instance, created)

    if created == True:
        user = instance.user
        qs = user.blog_set.filter(title=instance.title)
        if qs.count() > 1:
            instance.delete()
            raise ValueError("TItle already exist for this user")
        else:
            print("Checked successfully and nothing found")


