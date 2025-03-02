from django.shortcuts import render

# Create your views here.
from chbill.models import bill_msg
#from django.forms.models import model_to_dict


# Create your views here.
def bill_show_main(request):
    parm1 = 0
    if (request.method == 'POST'):
        parm1 = request.POST.get('wb', 'default_value')
    
    if parm1:
        bill_list = bill_msg.objects.filter(name = parm1)[0:8]
    else:
        bill_list = bill_msg.objects.all()[0:8]  # 获取所有数据
    #print("user search:",parm1)    
    return render(request,'billtotal.html', {'bill_list':bill_list})   # 返回index.html页面

# Create your views here.
def bill_find(request):

    if (request.method == 'POST'):
        parm1 = request.POST.get('wd', 'default_value')
    elif (request.method == 'GET'):
        parm1 = request.GET.get('wd', 'default_value')

    
    #endtile = parm1*10 + 10
    #bill_list = bill_msg.objects.filter(name = parm1)
    bill_list = bill_msg.objects.filter(name__contains=parm1)[0:8]   #db_id + __contains = param 
    #print("find page",parm1,bill_list)

    return render(request,'billfind.html', {'bill_list':bill_list})   # 返回index.html页面