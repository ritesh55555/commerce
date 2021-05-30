from django.contrib import admin
from .models import Listing, User , Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Comment)
