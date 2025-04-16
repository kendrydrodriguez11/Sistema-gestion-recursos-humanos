from django.urls import path
from apps.personal_training.views import supplier, application, course, certificate

app_name = "personal_training"
urlpatterns = []
# urls de las vistas de personal_files 
urlpatterns += [
    #path('home/',home.SecurityTemplateView.as_view(),name="home"),
    path('supplier/list', supplier.SupplierListView.as_view(),name="supplier_list" ),
    path('supplier/create',supplier.SupplierCreateView.as_view(),name="supplier_create" ),
    path('supplier/update/<int:pk>',supplier.SupplierUpdateView.as_view() ,name="supplier_update" ),
    path('supplier/delete/<int:pk>',supplier.SupplierDeleteView.as_view() ,name="supplier_delete" ),
]

# urls de las vistas de cursos
urlpatterns += [
    path('course/list', course.CourseListView.as_view(),name="course_list" ),
    path('course/create',course.CourseCreateView.as_view(),name="course_create" ),
    path('course/update/<int:pk>',course.CourseUpdateView.as_view() ,name="course_update" ),
    path('course/delete/<int:pk>',course.CourseDeleteView.as_view() ,name="course_delete" ),
]

# urls de las vistas de solicitud de capacitacion
urlpatterns += [
    path('application/list', application.ApplicationListView.as_view(),name="application_list" ),
    path('application/create',application.ApplicationCreateView.as_view(),name="application_create" ),
    path('application/create/<int:pk>',application.ApplicationCreateByCurseView.as_view(),name="application_create_by_curse" ),
    path('application/update/<int:pk>',application.ApplicationUpdateView.as_view() ,name="application_update" ),
    path('application/delete/<int:pk>',application.ApplicationDeleteView.as_view() ,name="application_delete" ),
    path('application/details/',application.ApplicationDetailsView.as_view() ,name="application_details" ),
    path('application/toggleapproveboss/<int:pk>',application.ApplicationToggleApproveBossView.as_view() ,name="application_approve_boss" ),
    path('application/toggleapprovecommission/<int:pk>',application.ApplicationToggleApproveCommissionView.as_view() ,name="application_approve_commission" ),
    path('application/set_cost/<int:pk>', application.ApplicationSetCostView.as_view() ,name="application_set_cost" ),
]

# urls de las vistas de solicitud de capacitacion
urlpatterns += [
    path('certificate/list', certificate.CertificateListView.as_view(),name="certificate_list" ),
    path('certificate/create',certificate.CertificateCreateView.as_view(),name="certificate_create" ),
    path('certificate/create/<int:pk>',certificate.CertificateCreateByCourseView.as_view(),name="certificate_create_by_curse" ),
    path('certificate/update/<int:pk>',certificate.CertificateUpdateView.as_view() ,name="certificate_update" ),
    path('certificate/delete/<int:pk>',certificate.CertificateDeleteView.as_view() ,name="certificate_delete" ),
    path('certificate/view/<int:certificate_id>/', certificate.CertificateView.as_view(), name='certificate_view'),

]