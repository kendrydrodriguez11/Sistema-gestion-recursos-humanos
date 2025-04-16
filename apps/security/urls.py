from django.urls import path
from apps.security.views import home,menu,country, profile,user,auth
app_name = "security"
urlpatterns = []
# urls de las vistas de menus 
urlpatterns += [
    #path('home/',home.SecurityTemplateView.as_view(),name="home"),
    path('menu/list',menu.MenuListView.as_view(),name="menu_list" ),
    path('menu/create',menu.MenuCreateView.as_view(),name="menu_create" ),
    path('menu/update/<int:pk>',menu.MenuUpdateView.as_view() ,name="menu_update" ),
    path('menu/delete/<int:pk>',menu.MenuDeleteView.as_view() ,name="menu_delete" ),
]
# urls de las vista de pais 
urlpatterns += [
    path('country/list',country.CountryListView.as_view(),name="country_list" ),
    path('country/create',country.CountryCreateView.as_view(),name="country_create" ),
    path('country/update/<int:pk>',country.CountryUpdateView.as_view() ,name="country_update" ),
    path('country/delete/<int:pk>',country.CountryDeleteView.as_view() ,name="country_delete" ),
]
# urls de la vistas de usuarios
urlpatterns += [
    path('user/list',user.UserListView.as_view(),name="user_list" ),
    path('user/create',user.UserCreateView.as_view(),name="user_create" ),
    path('user/update/<int:pk>',user.UserUpdateView.as_view() ,name="user_update" ),
    path('user/delete/<int:pk>',user.UserDeleteView.as_view() ,name="user_delete" ),
]
# urls de authentificacion
urlpatterns += [
    #path('auth/login',auth.iniciarSesion,name="auth_login"),
    path('auth/login',auth.LogLoginView.as_view(),name="auth_login"),
    path('auth/logout',auth.cerrarSesion,name='auth_logout'),
]
# urls de perfil y cambio de password
urlpatterns += [
    path('profile/update',profile.ProfileUpdateView.as_view(),name='profile_update'),
    path('change/password',profile.UserPasswordUpdateView.as_view(),name='change_password'),
]

