from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

# def iniciarSesion(request):
#     if request.method == 'GET':
#         context = {'title':'Iniciar Sesion','form':AuthenticationForm()}
#         return render(request, 'auth/login.html',context)
#     else:
#         user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
#         if user is None:
#             context = {'title':'Iniciar Sesion','form':AuthenticationForm(),'error':'Usuario o password incorrecto'}
#             return render(request, 'auth/login.html',context) 
#         else:
#             login(request,user) # crea una cooki del usuario registrado - guardar session
#             return redirect('home')


class LogLoginView(LoginView):
    template_name = 'auth/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        context['grabar'] = 'Login'
        return context

@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('security:auth_login')
