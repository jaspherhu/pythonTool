参考：https://www.cnblogs.com/learn643794461/p/11595598.html

一 安装环境
    pip install django #安装django框架

二，生成django工程框架文件，项目名字为：mysite
    django-admin startproject mysite # 创建mysite项目

三，创建APP
    cd mysite # 切换到mysite目录
    python manage.py startapp blog   # 创建blog应用

四，框架结构简单描述
    
mysite/

| --- settings.py ： 包含了项目的默认设置，包括数据库信息，调试标志以及其他一些工作的变量。

| --- urls.py ： 负责把URL模式映射到应用程序。

| --- wsgi.py : 用于项目部署。

blog /

| --- admin.py : django 自带admin后面管理，将models.py 中表映射到后台。

| --- apps.py : blog 应用的相关配置。

| --- models.py : Django 自带的ORM，用于设计数据库表。

| --- tests.py : 用于编写Django单元测试。

| --- veiws.py ：视图文件，用于编写功能的主要处理逻辑
manage.py ： Django项目里面的工具，通过它可以调用django shell和数据库等。

五，初始化admin后台数据库
    5.1 Python 自带SQLite3数据库，Django默认使用SQLite3数据库，如果使用其它数据库请在settings.py文件中设置。
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    之所以确认这个，是因为你可能想使用其他的数据库或者数据库部署在其他网络设备上

六，myblog/settings.py 中添加 blog 到 INSTALLED_APPS 列表中，注意blog只是我们刚才新建的APP，不是mysite(prj)

七：sqlite3数据迁移和管理员创建
    python manage.py makemigrations app1    #新建APP后需要的操作
    python manage.py makemigrations app2
    python manage.py migrate                ##编辑现有的APP数据库后需要的操作
    在项目根目录下生成了一个 db.sqlite3，对照了上面的DATABASES设置里面的 《BASE_DIR / 'db.sqlite3'》

    python manage.py createsuperuser
    //以下是响应内容
    Username (leave blank to use 'jaspher'): hufan
    Email address: hufan530@163.com
    Password:
    Password (again):
    This password is too short. It must contain at least 8 characters.
    This password is entirely numeric.
    Bypass password validation and create user anyway? [y/N]: y
    Superuser created successfully.

八，启动服务器
    python manage.py runserver
    ① 登录服务器主页，显示火箭
    http://127.0.0.1:8000/
    ②登录管理员后台，提示数据账号密码
    http://127.0.0.1:8000/admin/

=========================================到此位置就完成了第一阶段的框架基本搭建,后续开始搭建前后台和数据库了===================================================
现在已经到了第二阶段了，我们学习怎么在这个django平台上开发我们的：模型（数据库），视图（html），路由（url）


                                                                |---module(db)
                                                                |
                                                                |---view(html)
                                                                |
                                                |-----APP1/url--|---class_fucn(py)
                                                |
浏览器 ------- request -------django/mysite/url--|
                                                |
                                                |-----APP2/url--
                                                                |
接下来讨论下开发开发过程：
1，先创建APP/module的数据格式开发
    title = models.CharField(max_length = 150)  # 博客标题
    body = models.TextField()                   # 博客正文
    timestamp = models.DateTimeField()          # 创建时间

2，在APP/views里面导入刚才新建的from blog.models import blogsPost,把新建的同步数据库OMR数据返回回到view来
    from blog.models import blogsPost

3，在将数据库内容返回到新建的html页面上去，或者直接在后台这儿将数据以text方式response回去。
    blog_list = blogsPost.objects.all()  # 获取所有数据
    return render(request,'index.html', {'blog_list':blog_list})   # 返回index.html页面

4，先将APP的路由表添加到项目主路由表里面去:在mysite/urls.py文件里添加blog的url：
    from blog import views

    path('blog/', views.blog_index),

5，在刚才的第1步骤里面修改了数据库，所以这里需要重新执行迁移步骤
    python manage.py makemigrations blog #上次是没有这个blog的,这次新建一个blog数据库
    //回复效果
    Migrations for 'blog':
        blog\migrations\0001_initial.py
            - Create model blogsPost

    python manage.py migrate
    python manage.py migrate --database=usr_db
    python manage.py migrate --database=usr_db
    
    //回复效果
    Running migrations:
        Applying blog.0001_initial... OK
6，使用admin注册方式，方法在如下TIP中，修改db内容，是的你没有db管理工具。
Tip:如果你没有可视化数据库的东西，可以通过django的admin来管理数据库
    在APP/admin.py里面增加注册即可加入管理内容了

from blog.models import blogsPost
from blog.models import login_msg
class BlogsPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'timestamp']

admin.site.register(blogsPost, BlogsPostAdmin)

之后登录admin后台管路数据库内容
http://127.0.0.1:8000/admin/blog/blogspost/

7，重新登录http://127.0.0.1:8000/blog/，你会发现你刚才添加的blog数据已经可以显示了


踩过的坑：
1， href 标签后面接的是跳转链接
    href="http://127.0.0.1:8000/blog/text/?title={{ blog.title }}" #直接跳转到这个链接 ,这么些也可以：href="/blog/text/?title={{ blog.title }}"
    href="#?title={{ blog.title }}" #在原来的基础上直接新增后面的title

