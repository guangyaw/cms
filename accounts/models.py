from django.contrib.auth.models import User
from django.db import models
#from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Classification(models.Model):
    main_class = models.CharField(max_length=40, default='')


class BlogPost(models.Model):
    title = models.CharField(max_length=50, default='')
    content = RichTextUploadingField(max_length=300)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    classification = models.ManyToManyField(Classification)


