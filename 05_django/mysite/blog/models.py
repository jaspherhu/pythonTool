from django.db import models

# Create your models here.
class blogsPost(models.Model):
    title = models.CharField(max_length = 150)  # 博客标题
    body = models.TextField()                   # 博客正文
    timestamp = models.DateTimeField()          # 创建时间

# Create your models here.
class login_msg(models.Model):
    user = models.CharField(max_length = 150)    # 博客标题
    pasw = models.CharField(max_length = 150)   # 博客正文
    root = models.TextField()                   # root等级

