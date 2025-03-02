from django.db import models

# Create your models here.


# Create your models here.
class bill_msg(models.Model):
    id = models.CharField(max_length = 150, primary_key=True)    # 博客标题
    name = models.CharField(max_length = 150)   # 博客正文
    url = models.TextField(max_length = 150)                  # root等级
    intruduction = models.TextField(max_length = 150)   
    pic = models.TextField(max_length = 150) 
    up_time = models.TextField(max_length = 150)  
