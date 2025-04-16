from django.contrib import admin
from apps.security.models import GroupModulePermission, Menu, Module, User
admin.site.register(Menu)
admin.site.register(User)
admin.site.register(Module)
admin.site.register(GroupModulePermission)
