"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

    存在问题：Django 项目里多个app目录共用一个 urls 容易造成混淆，后期维护也不方便。

    解决：使用路由分发（include），让每个app目录都单独拥有自己的 urls。

    步骤：

    1、在每个 app 目录里都创建一个 urls.py 文件。
    2、在项目名称目录下的 urls 文件里，统一将路径分发给各个 app 目录。
"""
from django.contrib import admin
from django.urls import path,include # 从 django.urls 引入 include

from blog import views
from chbill import views
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("blog/", include("blog.urls")),
    path("chbill/", include("chbill.urls")),

    
    #path('blog/', views.blog_index),
    path("login/sigin", views.sigin),
    path("login/siged", views.siged),
    path("login/", views.login),
    #path("app02/", include("app02.urls")),

    path("main/", views.main_page),
    path("", views.root_page),
]
