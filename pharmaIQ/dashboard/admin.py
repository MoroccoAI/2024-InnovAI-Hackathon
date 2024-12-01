"""
    Supper user data :
    username : youssef
    password : youssef.05.  
    email : youssefmoustaid90@gmail.com
"""

from django.contrib import admin
from .models import *

admin.site.register(Drug)
admin.site.register(Stock)
admin.site.register(Alert)  
admin.site.register(Sale)
admin.site.register(Archive)
admin.site.register(Report)

# Register your models here.
