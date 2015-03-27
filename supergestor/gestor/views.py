from django.shortcuts import render
#from django.contrib.auth import authenticate, login
#from django.contrib.auth import views
#from django.contrib.auth import logout
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

from gestor.models import MyUser,Permitido
#from django.core.context_processors import csrf
#from django.template.context import RequestContext
#from django.contrib.auth.forms import UserCreationForm
#from django import forms
# Create your views here.
def holaView(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))
    else:
        return render(request,'hola.html',{'usuario':request.user})
    
def registrarUsuarioView(request):
    if request.method == 'GET':
        return render(request, 'crearusuario.html')
"""
def registrarUsuarioView(request):
    if request.method == 'POST':
        if request.method == 'POST':
            form = CustomerRegistrationForm(request.POST)
            if form.is_valid():
                f = form.save(force_insert=True)
            return redirect('/hola/')
    else:
        args = {}
        args.update(csrf(request))
        args['form'] = CustomerRegistrationForm()
    return render_to_response('crearusuario.html', args ,context_instance = RequestContext(request))
    #return render(request, 'crearusuario.html')
    
class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username','password','email')
    def save(self, commit=True):
        user = super(CustomerRegistrationForm, self).save(commit=False)
        if commit:
            user.save(force_insert=True)
        return user
"""   

def guardarUsuarioView(request):
    usuario = MyUser.objects.create_user(username=request.POST['username'], password=request.POST['password1'],email=request.POST['email'])
    usuario.is_admin=False
    usuario.direccion = request.POST['direccion']
    usuario.last_name = request.POST['last_name']
    usuario.user_name = request.POST['user_name']
    #usuario.save(using=request._db)
    usuario.save()
    return HttpResponseRedirect('/login')

"""
def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            pass
    else:
        # Return an 'invalid login' error message.
        pass

def logout_view(request):
    logout(request)
    # Redirect to a success page.

def change_password(request):
    template_response = views.password_change(request)
    # Do something with `template_response`
    #For more details, see the TemplateResponse documentation.
    return template_response
"""