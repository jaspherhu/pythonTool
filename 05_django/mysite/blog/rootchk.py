from django.db import models
from blog.models import login_msg

# Create your models here.
class login_chk:
    #use_list = []

    #def __user_check__(self):
        #use_list = usr_msg.objects.all()  # 获取所有数据

    def root_check(request):
        if (request.method == 'POST'):
            email_input = request.POST.get('email', 'default_value')
            user_input = request.POST.get('user', 'default_value')
            pasw_input = request.POST.get('password', 'default_value')
        elif (request.method == 'GET'):
            email_input = request.GET.get('email', 'default_value')
            user_input = request.GET.get('user', 'default_value')
            pasw_input = request.GET.get('password', 'default_value')

        print("user input:",email_input,user_input,pasw_input)
        use_list = login_msg.objects.all()  # 获取所有数据
        

        for usr in use_list:
            return((usr.user == user_input) and (usr.pasw == pasw_input))
        
        return False
