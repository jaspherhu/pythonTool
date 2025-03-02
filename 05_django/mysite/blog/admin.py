from django.contrib import admin

# Register your models here.
from blog.models import blogsPost , login_msg

class BlogsPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'timestamp']

class login_msgAdmin(admin.ModelAdmin):
    list_display = ['user', 'pasw', 'root']



admin.site.register(blogsPost, BlogsPostAdmin)
admin.site.register(login_msg, login_msgAdmin)
