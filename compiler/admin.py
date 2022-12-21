

from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Collaboration)
admin.site.register(Projet)

admin.site.register(Customer)
admin.site.register(SaveFiles)


