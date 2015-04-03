#coding: utf-8
"""Archivo que contiene los metodos que contienen
las peticiones, las manipula y gestiona la respuesta a enviar
a los clientes , cada vista obtiene de request que se le es envado
luego de pasar por el filtro de expresiones regulares"""
from django.shortcuts import render, render_to_response
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from gestor.models import MyUser, asignacion, proyecto, rol, Flujo
from django import forms
from django.core.mail.message import EmailMessage
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
#from gestor.admin import proyectoFrom

# Create your views and forms here.
@login_required
def holaView(request):
    """Vista que redirige a la pagina principal de administracion tanto a usuarios como a
    superusuarios, los superusuarios son redirigidos a la aplicacion admin mientras que los 
    usuarios obtienen una respuesta con el template hola.html"""
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))
    else:
        nombres_de_proyecto = {}
        for a in asignacion.objects.all():
            if a.usuario.id == request.user.id:
                rol_lista = rol.objects.get(rol_id = a.rol.rol_id)
                for p in proyecto.objects.all():
                    if p.proyecto_id == a.proyecto.proyecto_id:
                        nombres_de_proyecto[rol_lista] = p
        return render(request,'hola.html',{'usuario':request.user, 'proyectos':nombres_de_proyecto})

def holaScrumView(request): 
    return render(request,'rol-flujo-para-scrum.html',{'roles':rol.objects.all(), 'flujos':Flujo.objects.all()})

def ListarUsuarioParaFormarEquipo(request):
    return render(request,'formarEquipo.html',{'usuarios':MyUser.objects.all(), 'roles':rol.objects.all()})

def registrarUsuarioView(request):
    """Vista que se obitene del regex /registrar solicitado al precionar el boton
    registrar en el login, devuelve un formulario html para crear un nuevo usuario
    con un correo existente"""
    if request.method == 'GET':
        return render(request, 'crearusuario.html')

def guardarUsuarioView(request):
    """Vista de guardado de nuevo usuario relacionado con un correo autorizado en la tabla Permitidos
    que se utiliza en la interfaz devuelta por /registrar """
    try:
    
        usuario = MyUser.objects.create_user(username=request.POST['username'], password=request.POST['password1'],email=request.POST['email'])
        usuario.is_admin=False
        usuario.direccion = request.POST['direccion']
        usuario.last_name = request.POST['last_name']
        usuario.user_name = request.POST['user_name']
        #usuario.save(using=request._db)
        usuario.save()
        return HttpResponseRedirect('/login')
    except ObjectDoesNotExist:
        print "Either the entry or blog doesn't exist." 
        return HttpResponseRedirect('/registrar')
    
class FormularioContacto(forms.Form):
    usuario = forms.CharField()
    correo = forms.EmailField()

class Formulario(forms.Form):
    nombre = forms.CharField(max_length=100)
    mensaje = forms.CharField()
    mail = forms.EmailField()

class FormularioSeteoContrasenha(forms.Form):
    password_nueva1 = forms.CharField(widget=forms.PasswordInput)
    password_nueva2 = forms.CharField(widget=forms.PasswordInput)
    
def contactomail(request):
    if request.method == 'POST':
        formulario = FormularioContacto(request.POST)
        if formulario.is_valid():
            asunto = 'RECUPERACION DE CONTRASEÑA'
            username_cargado = formulario.cleaned_data['usuario']
            usuario = MyUser.objects.get(username = username_cargado)
            if (str(usuario.email) == formulario.cleaned_data['correo']):
                mensaje = 'Puedes dirigirte a esta URL de seteo de tu password:  djangoserver/seteoPassword/' + str(usuario.id) + '/'
                mail = EmailMessage(asunto, mensaje, to=[request.POST['correo']])
                mail.send()
                return HttpResponseRedirect('/login') 
            else:
                return HttpResponse('El email no coincide con tu email unico asociado a tu usuario')  
             
    else:
        formulario = FormularioContacto()
        
    return render_to_response('contactoMail.html', {'formulario': formulario},
                              context_instance=RequestContext(request))
    
def seteoPassword(request, usuario_id):
    if request.method == 'POST':
        formulario = FormularioSeteoContrasenha(request.POST)
        if formulario.is_valid():
            passwor1 = formulario.cleaned_data['password_nueva1']
            passwor2 = formulario.cleaned_data['password_nueva2']
            usuario = MyUser.objects.get(id = usuario_id)
            if (usuario is not None):
                if passwor1 and passwor2 and passwor1 != passwor2:
                    raise forms.ValidationError("Passwords don't match")
                else:
                    usuario.set_password(formulario.cleaned_data['password_nueva1'])
                    usuario.save()
                return HttpResponse('Tu contrasenha ha sido cambiada, puedes loguearte con tu nueva contrasenha')    
    else:
        formulario = FormularioSeteoContrasenha()
        
    return render_to_response('seteoPassword.html', {'formulario': formulario},
                              context_instance=RequestContext(request))
    

class FormularioRolProyecto(forms.ModelForm):
    
    """ permiso=forms.ModelMultipleChoiceField()
    nombre=forms.CharField()
    descripcion= forms.CharField()"""
    class Meta:
        model= rol
        fields=['permisos','nombre_rol_id','descripcion']
        
        
    
def vistaModicarRolProyecto(request,rolid):
    if request.method == 'POST':
        rol_to_change= rol.objects.get(rol_id=rolid)
        formulario_loaded = FormularioRolProyecto(request.POST,instance=rol_to_change)
        formulario_loaded.save()
    else:  
        """asignation= asignacion.objects.get(asignacion_id=request.asignacion)  #asignacion supongo que es lo que me manda kathe
        rolproyecto= rol.objects.get(rol=asignation.rol)""" #me dalta ver si chequear asi nomas o el rol
        rolproyecto= rol.objects.get(rol_id=rolid)
        formulario =  FormularioRolProyecto(initial=rolproyecto)      
        return render_to_response('changerol.html',{'formulario':formulario},
                                  context_instance=RequestContext(request))

class proyectoFrom(forms.ModelForm):
    """Clase meta de un ModelForm donde se indica el Modelo relacionado y los campos a mostrar"""
    class Meta:
        model = proyecto
        fields = ['nombre_corto', 'nombre_largo', 'descripcion','fecha_inicio','fecha_fin']

def modificarProyecto(request, proyecto_id=2):
    """Modifica el proyecto"""
    p=proyecto.objects.get(proyecto_id=2)
    if request.method == 'POST':
        form = proyectoFrom(request.POST)
        if form.is_valid():
            nombre_corto=form.cleanned_data['nombre_corto']
            nombre_largo=form.cleanned_data['nombre_largo']
            descripcion=form.cleanned_data['descripcion']
            fecha_inicio=form.cleanned_data['fecha_inicio']
            fecha_fin=form.cleanned_data['fecha_fin']
            p.nombre_corto=nombre_corto
            p.nombre_largo=nombre_largo
            p.descripcion=descripcion
            p.fecha_inicio=fecha_inicio
            p.fecha_fin=fecha_fin
            p.save() #Guardamos el modelo de manera Editada
            return HttpResponse('Tu proyecto a sido guardado exitosamente')
    else:
        
        form = proyectoFrom(initial={
                                         'nombre_corto': p.nombre_corto,
                                         'nombre_largo': p.nombre_largo,
                                         'descripcion': p.descripcion,
                                         'fecha_inicio': p.fecha_inicio,
                                         'fecha_fin': p.fecha_fin,
                                     
                                         })
        ctx = {'form':form, 'proyecto':p}
        return render_to_response('modificarProyecto.html', ctx ,context_instance=RequestContext(request))
