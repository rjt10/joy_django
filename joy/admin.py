from django.contrib import admin
from joy.models import User
from joy.models import Group
from joy.models import Membership

# Register your models here.
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Membership)
