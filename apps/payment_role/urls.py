
from django.urls import path
from apps.payment_role.views import overtime
app_name = "payment_role"
urlpatterns = []
# urls de las vistas de organizacion 
urlpatterns += [
    path('overtime/list',overtime.OvertimeListView.as_view(),name="overtime_list" ),
    path('overtime/create',overtime.OvertimeCreateView.as_view(),name="overtime_create" ),
    path('overtime/update/<int:pk>',overtime.OvertimeUpdateView.as_view() ,name="overtime_update" ),
    path('overtime/detail',overtime.OvertimeDetailView.as_view() ,name="overtime_detail" ),
    path('overtime/delete/<int:pk>',overtime.OvertimeDeleteView.as_view() ,name="overtime_delete" ),
    path('overtime/data_employee',overtime.OvertimeValueHours.as_view() ,name="overtime_value_hours" ),
]                                     