from django.shortcuts import render

# Create your views here.
from blog.models import blogsPost
#from django.forms.models import model_to_dict
from blog.rootchk import login_chk

def root_page(request):
    return render(request,'root.html')   # 返回index.html页面
    
# Create your views here.
def main_page(request):
    #校验密码对不对
    #if (login_chk.root_check(request)):
    return render(request,'main.html')   # 进入主页
    #else:
        #return render(request,"log failed Please relogin")   # 返回index.html页面
        #return render(request,'login.html')   # 返回index.html页面

# Create your views here.
def login(request):
        return render(request,'login.html')   # 返回index.html页面

# Create your views here.
def sigin(request):
    if (login_chk.root_check(request)):
        print("check user ok===========")
        return render(request,'main.html')   # 返回index.html页面
    else:
        print("check user failed===========")
        #return render(request,'sigin.html')   # 返回index.html页面
        return render(request,'log failed Please relogin')   # 返回index.html页面

# Create your views here.
def siged(request):
    if (request.method == 'POST'):
        my_param = request.POST.get('username', 'default_value')
    elif (request.method == 'GET'):
        my_param = request.GET.get('password', 'default_value')

    return render(request,'注册账号还没做')   # 返回index.html页面
 
# Create your views here.
def blog_index(request):
    blog_list = blogsPost.objects.all()  # 获取所有数据
    return render(request,'index3.html', {'blog_list':blog_list})   # 返回index.html页面

# Create your views here.
def blog_details(request):
    #blog_list = blogsPost.objects.all()  # 获取所有数据 get
    if (request.method == 'POST'):
        my_param = request.POST.get('title', 'default_value')
    elif (request.method == 'GET'):
        my_param = request.GET.get('title', 'default_value')

    list = blogsPost.objects.filter(title = my_param)   #get 可能会返回多个不行的 __class__
    #userDict = model_to_dict(goal)  #强制转换为dict数据,我也不知道为啥要用这个,直接使用 class blogsPost不就得了嘛

    return render(request,'indexs.html', {'list':list}) #context 类型是map,就算是class,也要包装成map发过去



