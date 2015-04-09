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
from gestor.models import MyUser, asignacion, proyecto, rol, Flujo, Actividades
from django import forms
from django.core.mail.message import EmailMessage
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.models import Permission


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
                rol_lista = rol.objects.get(id = a.rol.id)
                for p in proyecto.objects.all():
                    if p.id == a.proyecto.id:
                        nombres_de_proyecto[p] = rol_lista
        return render(request,'hola.html',{'usuario':request.user, 'proyectos':nombres_de_proyecto})

def holaScrumView(request,usuario_id,proyectoid): 
    proyectox=proyecto.objects.get(id=proyectoid)
    usuario=MyUser.objects.get(id=usuario_id)
    return render(request,'rol-flujo-para-scrum.html',{'roles':rol.objects.all(), 'flujos':Flujo.objects.all(),'proyecto':proyectox,'usuario':usuario})

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
    
        usuario = MyUser.objects.create_superuser(username=request.POST['username'], password=request.POST['password1'],email=request.POST['email'])
        usuario.is_admin=True
        usuario.direccion = request.POST['direccion']
        usuario.last_name = request.POST['last_name']
        usuario.user_name = request.POST['user_name']
        #usuario.save(using=request._db)
        usuario.save()
        return HttpResponseRedirect('/login')
    except ObjectDoesNotExist:
        print "Either the entry or blog doesn't exist." 
        return HttpResponseRedirect('/registrar')
    
def guardarRolView(request,usuario_id):
    """Vista de guardado de nuevo usuario relacionado con un correo autorizado en la tabla Permitidos
    que se utiliza en la interfaz devuelta por /registrar """
    try:
        usuario=MyUser.objects.get(id=usuario_id)
        rol_a_crear = rol.objects.create(nombre_rol_id=request.POST['nombre_rol_id'], descripcion=request.POST['descripcion'],usuario_creador=usuario)
        for p in request.POST.getlist('permisos'):
            rol_a_crear.permisos.add(Permission.objects.get(id=p))
        rol_a_crear.save()
        return HttpResponse('El rol se ha creado')
      
    except ObjectDoesNotExist:
        print "Either the entry or blog doesn't exist." 
        return HttpResponseRedirect('/crearRol/')
    
def guardarFlujoView(request):
    """Vista de guardado de nuevo usuario relacionado con un correo autorizado en la tabla Permitidos
    que se utiliza en la interfaz devuelta por /registrar """
    try:
    
        flujo_a_crear = Flujo.objects.create(nombre=request.POST['nombre'], estado=request.POST['estado'])
        for p in request.POST.getlist('actividades'):
            flujo_a_crear.actividades.add(Actividades.objects.get(id=p))
        flujo_a_crear.save()
        return HttpResponse('El flujo se ha creado')  
    except ObjectDoesNotExist:
        print "Either the entry or blog doesn't exist." 
        return HttpResponseRedirect('/crearFlujo/')
    
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
                    return HttpResponse("Las contrasenhas no coinciden, vuelve a la pagina de seteo")
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
        widgets = {
            'permisos': CheckboxSelectMultiple(),
        }
        
def visualizarRolProyectoView(request,usuario_id,proyectoid, rol_id_rec):
    """if request.method == 'POST':
        rol_to_change= rol.objects.get(rol_id=rol_id_rec)
        formulario_loaded = FormularioRolProyecto(request.POST,instance=rol_to_change)
        formulario_loaded.save()"""
    rolproyecto= rol.objects.get(id=rol_id_rec)
    if request.method == 'POST':
        formulario = FormularioRolProyecto(request.POST)
        if formulario.is_valid():
            nombre_rol_id=formulario.cleanned_data['c']
            descripcion=formulario.cleanned_data['descripcion']
            permisos=formulario.cleanned_data['permisos']
            rolproyecto.nombre_rol_id=nombre_rol_id
            rolproyecto.descripcion=descripcion
            rolproyecto.permisos=permisos
            rolproyecto.save() #Guardamos el modelo de manera Editada
            return HttpResponse('El rol ha sido guardado exitosamente')
    else:  
        """asignation= asignacion.objects.get(asignacion_id=request.asignacion)  #asignacion supongo que es lo que me manda kathe
        rolproyecto= rol.objects.get(rol=asignation.rol)""" #me dalta ver si chequear asi nomas o el rol
        
        formulario =  FormularioRolProyecto(initial={
                                                     'nombre_rol_id': rolproyecto.nombre_rol_id,
                                                     'permisos': rolproyecto.permisos,
                                                     'descripcion': rolproyecto.descripcion,
                                                     })      
        return render_to_response('visualizarRol.html',{'formulario':formulario, 'rol':rolproyecto, 'proyectoid':proyectoid,'usuarioid':usuario_id},
                                  context_instance=RequestContext(request))
        
def modificarRol(request, usuario_id, proyectoid, rol_id_rec):
    """Modifica el Rol"""
    f=rol.objects.get(id=rol_id_rec)
    u=MyUser.objects.get(id=usuario_id)
    if request.method == 'POST':
        form = FormularioRolProyecto(request.POST)
        if form.is_valid():
            nombre_rol_id=form.cleaned_data['nombre_rol_id']
            descripcion=form.cleaned_data['descripcion']
            permisos=form.cleaned_data['permisos']
            f.nombre_rol_id=nombre_rol_id
            f.descripcion=descripcion
            f.permisos=permisos
            f.usuario_creador=u
            f.save() #Guardamos el modelo de manera Editada
            return HttpResponse('El rol a sido modificado exitosamente')
    else:
        
        form = FormularioRolProyecto(initial={
                                         'nombre_rol_id': f.nombre_rol_id,
                                         'descripcion': f.descripcion,
                                         'permisos': [t.id for t in f.permisos.all()],
   
                                         })
        ctx = {'form':form, 'rol':f, 'proyectoid':proyectoid,'usuarioid':usuario_id}
        return render_to_response('modificarRol.html', ctx ,context_instance=RequestContext(request))

class FormularioFlujoProyecto(forms.ModelForm):
    
    """ permiso=forms.ModelMultipleChoiceField()
    nombre=forms.CharField()
    descripcion= forms.CharField()"""
    class Meta:
        model= Flujo
        fields=['nombre','estado','actividades']
        widgets = {
            'actividades': CheckboxSelectMultiple(),
        }
        
def visualizarFlujoProyectoView(request,usuario_id, proyectoid, flujo_id_rec):
    flujo_disponible= Flujo.objects.get(id=flujo_id_rec)
    if request.method == 'POST':
        formulario = FormularioFlujoProyecto(request.POST)
        if formulario.is_valid():
            nombre=formulario.cleanned_data['nombre']
            estado=formulario.cleanned_data['estado']
            actividades=formulario.cleanned_data['actividades']
            flujo_disponible.nombre=nombre
            flujo_disponible.estado=estado
            flujo_disponible.actividades=actividades
            flujo_disponible.save() #Guardamos el modelo de manera Editada
            return HttpResponse('El rol ha sido guardado exitosamente')
    else:  
        """asignation= asignacion.objects.get(asignacion_id=request.asignacion)  #asignacion supongo que es lo que me manda kathe
        rolproyecto= rol.objects.get(rol=asignation.rol)""" #me dalta ver si chequear asi nomas o el rol
        
        formulario =  FormularioRolProyecto(initial={
                                                     'nombre': flujo_disponible.nombre,
                                                     'estado': flujo_disponible.estado,
                                                     'actividades': flujo_disponible.actividades,
                                                     })      
        return render_to_response('visualizarFlujo.html',{'formulario':formulario, 'flujo':flujo_disponible, 'proyectoid':proyectoid,'usuarioid':usuario_id},
                                  context_instance=RequestContext(request))

def modificarFlujo(request, usuario_id, proyectoid, flujo_id_rec):
    """Modifica el Flujo"""
    f=Flujo.objects.get(id=flujo_id_rec)
    if request.method == 'POST':
        form = FormularioFlujoProyecto(request.POST)
        if form.is_valid():
            nombre=form.cleaned_data['nombre']
            estado=form.cleaned_data['estado']
            actividades=form.cleaned_data['actividades']
            f.nombre=nombre
            f.estado=estado
            f.actividades=actividades
            f.save() #Guardamos el modelo de manera Editada
            return HttpResponse('El flujo a sido modificado exitosamente')
    else:
        
        form = FormularioFlujoProyecto(initial={
                                         'nombre': f.nombre,
                                         'estado': f.estado,
                                         'actividades': [t.id for t in f.actividades.all()],
   
                                         })
        ctx = {'form':form, 'flujo':f, 'proyectoid':proyectoid,'usuarioid':usuario_id}
        return render_to_response('modificarFlujo.html', ctx ,context_instance=RequestContext(request))
    
def crearRol(request,usuario_id,proyectoid):
    if request.method == 'GET':
        permisos=Permission.objects.all().exclude(name='Can add group').exclude(name='Can change group') 
        permisos=permisos.exclude(name='Can delete group').exclude(name='Can delete permission') 
        permisos=permisos.exclude(name='Can add my user').exclude(name='Can change my user') 
        permisos=permisos.exclude(name='Can delete my user').exclude(name='Can delete rol sistema') 
        permisos=permisos.exclude(name='Can add permission').exclude(name='Can change permission') 
        permisos=permisos.exclude(name='Can add rol sistema').exclude(name='Can change rol sistema') 
        permisos=permisos.exclude(name='Can add proyecto').exclude(name='Can change proyecto') 
        permisos=permisos.exclude(name='Can delete proyecto') 
        permisos=permisos.exclude(name='Can add asigna sistema').exclude(name='Can change asigna sistema') 
        permisos=permisos.exclude(name='Can delete asigna sistema') 
        permisos=permisos.exclude(name='Can add permitido').exclude(name='Can change permitido') 
        permisos=permisos.exclude(name='Can delete permitido')
        permisos=permisos.exclude(name='Can add log entry').exclude(name='Can delete log entry').exclude(name='Can change log entry')
        permisos=permisos.exclude(name='Can add content type').exclude(name='Can delete content type').exclude(name='Can change content type')
        return render(request, 'crearRol.html',{'permissions':permisos,'usuarioid':usuario_id,'proyectoid':proyectoid})
    
def crearFlujo(request,usuario_id,proyectoid):
    if request.method == 'GET':
        return render(request, 'crearFlujo.html',{'actividades':Actividades.objects.all(),'usuarioid':usuario_id,'proyectoid':proyectoid})

class proyectoFrom(forms.ModelForm):
    """Clase meta de un ModelForm donde se indica el Modelo relacionado y los campos a mostrar"""
    class Meta:
        model = proyecto
        fields = ['nombre_corto', 'nombre_largo', 'descripcion','estado','fecha_inicio','fecha_fin']

def modificarProyecto(request, usuario_id, proyecto_id_rec):
    """Modifica el proyecto"""
    p=proyecto.objects.get(id=proyecto_id_rec)
    if request.method == 'POST':
        form = proyectoFrom(request.POST)
        if form.is_valid():
            nombre_corto=form.cleaned_data['nombre_corto']
            nombre_largo=form.cleaned_data['nombre_largo']
            descripcion=form.cleaned_data['descripcion']
            estado=form.cleaned_data['estado']
            fecha_inicio=form.cleaned_data['fecha_inicio']
            fecha_fin=form.cleaned_data['fecha_fin']
            p.nombre_corto=nombre_corto
            p.nombre_largo=nombre_largo
            p.descripcion=descripcion
            p.estado=estado
            p.fecha_inicio=fecha_inicio
            p.fecha_fin=fecha_fin
            p.save() #Guardamos el modelo de manera Editada
            return HttpResponse('Tu proyecto a sido guardado exitosamente')
    else:
        
        form = proyectoFrom(initial={
                                         'nombre_corto': p.nombre_corto,
                                         'nombre_largo': p.nombre_largo,
                                         'descripcion': p.descripcion,
                                         'estado':p.estado,
                                         'fecha_inicio': p.fecha_inicio,
                                         'fecha_fin': p.fecha_fin,
                                     
                                         })
        ctx = {'form':form, 'proyecto':p,'usuarioid':usuario_id}
        return render_to_response('modificarProyecto.html', ctx ,context_instance=RequestContext(request))
    
def visualizarProyectoView(request,usuario_id, proyecto_id_rec):
    """if request.method == 'POST':
        rol_to_change= rol.objects.get(rol_id=rol_id_rec)
        formulario_loaded = FormularioRolProyecto(request.POST,instance=rol_to_change)
        formulario_loaded.save()"""
    proyecto_enc= proyecto.objects.get(id=proyecto_id_rec)
    return render_to_response('visualizarProyecto.html',{'proyecto':proyecto_enc,'usuarioid':usuario_id},
                                  context_instance=RequestContext(request))

        

    
def crearActividadView(request,usuario_id,proyectoid):
    """
    Vista que se obitene del regex /registrar solicitado al precionar el boton
    registrar en el Flujo, devuelve un formulario html para crear una nueva actividad
    """
    
    if request.method == 'GET':
        #si no es una peticion post, aignamos a form
        #el form que hemos creado sin datos
        form = formularioActividad()
        return render_to_response("crearActividad.html",{"form":form,'usuarioid':usuario_id,'proyectoid':proyectoid}, context_instance = RequestContext(request))
    
    else:#request.method == 'POST'
        form = formularioActividad(request.POST)
        if form.is_valid():
            nombre=form.cleaned_data['nombre']
            descripcion=form.cleaned_data['descripcion']
            #flujo=form.cleaned_data['flujo']
            form.nombre=nombre
            form.descripcion=descripcion
            #form.flujo=flujo
            form.save()
            return HttpResponse('Ha sido guardado exitosamente')       
 
class formularioActividad(forms.ModelForm):
    class Meta:
        model=Actividades
        fields = ('nombre', 'descripcion')
        
def seleccionarFlujoModificar(request,usuario_id,proyectoid):
    return render(request,'seleccionarActividad.html',{'actividades':Actividades.objects.all(),'usuarioid':usuario_id,'proyectoid':proyectoid})

def modificarActividad(request,usuario_id,proyectoid,actividad_id_rec):
    p=Actividades.objects.get(id=actividad_id_rec)
    if request.method == 'POST':
        form = formularioActividad(request.POST)
        if form.is_valid():
            nombre=form.cleaned_data['nombre']
            descripcion=form.cleaned_data['descripcion']
            #flujo=form.cleaned_data['flujo']
            p.nombre=nombre
            p.descripcion=descripcion
            #p.flujo=flujo
            p.save() #Guardamos el modelo de manera Editada
            return HttpResponse('Se ha guardado exitosamente')
    else:
        
        form = formularioActividad(initial={
                                         'nombre': p.nombre,
                                         'descripcion': p.descripcion,
                                         #'flujo': p.flujo,
                                     
                                         })
        ctx = {'form':form, 'Actividad':p,'usuarioid':usuario_id,'proyectoid':proyectoid}
        return render_to_response('modificarActividad.html', ctx ,context_instance=RequestContext(request)) 
 
    
def asignarRol(request,rolid,proyectoid,usuario_id):
    proyectox=proyecto.objects.get(id=proyectoid)
    rolx = rol.objects.get(id=rolid)
    usuario = MyUser.objects.get(id=usuario_id)
    if request.method=='POST':
        try:
            for p in request.POST.getlist('usuarios'):
                asignacion_a_crear = asignacion.objects.create(usuario=MyUser.objects.get(id=p),rol=rolx, proyecto=proyectox)
                asignacion_a_crear.save()
<<<<<<< HEAD
                return HttpResponse('La asignacion se ha realizado exitosamente')
=======
                usuario=MyUser.objects.get(id=usuario_id)
                return render(request,'rol-flujo-para-scrum.html',{'roles':rol.objects.all(), 'flujos':Flujo.objects.all(),'proyecto':proyectox,'usuario':usuario})
>>>>>>> branch 'master' of https://github.com/JanKeunSuk/CNBLUE.git
        except ObjectDoesNotExist:
            print "Either the entry or blog doesn't exist." 
            return HttpResponseRedirect('/crearFlujo/')
    else:
        return render_to_response('asignaRolProyecto.html',{'proyecto':proyectox,'usuarios':MyUser.objects.all().exclude(id=usuario_id),'proyectoid':proyectoid,'usuarioid':usuario_id})
    """proyectox=proyecto.objects.get(id=proyectoid)
    rolx = rol.objects.get(id=rolid)
    if request.method=='POST':
        #necesito obtener el usuario
        form=asignaForm_web(request.POST)
        if form.is_valid():
            u=form.cleaned_data['usuario']#aca nose si obtener el user o si con esto es suficiente
            #tengo que crear una asignacion con los datos que ya tengo
            usuario=MyUser.objects.get(username=u)
            formx=asignaForm_view(usuario,rolx,proyectox)
            formx.save()
            
            #Volver a la vista de scrum redirigiendo al mismo template con las mismas variables
           
            return render(request,'rol-flujo-para-scrum.html',{'roles':rol.objects.all(), 'flujos':Flujo.objects.all(),'proyecto':proyectox})
            
    else:
        form= asignaForm_web()
        return render_to_response('asignaRolProyecto.html',{'formulario':form,'proyecto':proyectox,'usuarios':MyUser.objects.all()},context_instance=RequestContext(request))
    
    """
    
