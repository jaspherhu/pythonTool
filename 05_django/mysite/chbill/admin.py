from django.contrib import admin

# Register your models here.
# Register your models here.
from chbill.models import  bill_msg

class bill_msgAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url', 'intruduction', 'pic', 'up_time']


admin.site.register(bill_msg, bill_msgAdmin)
