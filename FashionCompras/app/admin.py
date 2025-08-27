from django.contrib import admin
from .models import * #Imported all models

admin.site.register(Auth) #Registered
admin.site.register(Item) #Registered

