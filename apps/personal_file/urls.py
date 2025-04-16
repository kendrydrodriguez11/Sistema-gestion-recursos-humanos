from django.urls import path
from apps.personal_file.views import employee
app_name = "personal_file"
urlpatterns = []
# urls de las vistas de organizacion 
urlpatterns += [
    path('employee/list',employee.EmployeeListView.as_view(),name="employee_list" ),
    path('employee/create',employee.EmployeeCreateView.as_view(),name="employee_create" ),
    path('employee/update/<int:pk>',employee.EmployeeUpdateView.as_view() ,name="employee_update" ),
    path('employee/delete/<int:pk>',employee.EmployeeDeleteView.as_view() ,name="employee_delete" ),
]