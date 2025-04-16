from django.contrib import admin
from apps.payment_role.models import Calendar, Item, Overtime, OvertimeDetail, RoleFrequency, TypePermission, WorkPermission

# formfield_overrides = {
#         models.TextField: {
#             'widget': Textarea(attrs={'rows': 4, 'cols': 60})
#         },
#     }

class OvertimeDetailInline(admin.TabularInline):
    model = OvertimeDetail
    extra = 1
    can_delete = True
    show_change_link = True

class OvertimeAdmin(admin.ModelAdmin):
    inlines = (OvertimeDetailInline,)
    list_display = (
        'calendar',
        'employee',
        'total',
        'calendar_process',
        'processed',
       
    )
    search_fields = ('processed', 'employee__last_name')
    list_filter = (
        'calendar',
        'processed',
    )

admin.site.register(Overtime, OvertimeAdmin)
admin.site.register(Calendar)
admin.site.register(Item)
admin.site.register(RoleFrequency)
admin.site.register(TypePermission)
admin.site.register(WorkPermission)


