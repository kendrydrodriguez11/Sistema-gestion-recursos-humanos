from django.contrib import admin

from apps.personal_file.models import Employee,Category,TypeContract,TypeArea,TypeEmployee,Post,TypeRegime,Area

admin.site.register(TypeContract)
admin.site.register(TypeEmployee)
admin.site.register(TypeRegime)
admin.site.register(TypeArea)
admin.site.register(Area)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Employee)