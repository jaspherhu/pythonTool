
from django.urls import path,re_path 
from blog import views # 从自己的 app 目录引入 views 

urlpatterns = [ 
    #re_path(r'^login/(?P<m>[0-9]{2})/$', views.index, ),
    re_path('text/', views.blog_details), #子集路由链接一定要放在头部位置,不然默认访问了根目录了
    
    re_path('', views.blog_index),  
]