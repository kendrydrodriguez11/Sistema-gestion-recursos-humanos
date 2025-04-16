from django.urls import path
from apps.core.views import organization
app_name = "core"
urlpatterns = []
# urls de las vistas de organizacion 
urlpatterns += [
    path('organization/list',organization.OrganizationListView.as_view(),name="organization_list" ),
    path('organization/create',organization.OrganizationCreateView.as_view(),name="organization_create" ),
    path('organization/update/<int:pk>',organization.OrganizationUpdateView.as_view() ,name="organization_update" ),
    path('organization/delete/<int:pk>',organization.OrganizationDeleteView.as_view() ,name="organization_delete" ),
]