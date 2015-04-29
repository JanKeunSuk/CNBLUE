#coding: utf-8
"""Archivo que contiene los metodos que responden a las peticiones de las URL que se filtran por medio de las
expresiones regulares en el archivo urls.py, manipula y gestiona la respuesta que se van a enviar a los clientes.
Cada vista obtiene del request que se le envio la informacion necesaria para el funcionamiento de los metodos,
"""
from django.shortcuts import render, render_to_response
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from gestor.models import MyUser, asignacion, proyecto, rol, Flujo, Actividades, HU, Sprint, delegacion, HU_descripcion, archivoadjunto, asignaHU_actividad_flujo
from django import forms
from django.core.mail.message import EmailMessage
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.models import Permission
from datetime import datetime 
import json
from django.utils import timezone

# Create your views and forms here.
@login_required
def holaView(request):
    """Vista que redirige a la pagina principal de administracion tanto a usuarios como a
    superusuarios, los superusuarios son redirigidos a la aplicacion admin mientras que los 
    usuarios obtienen una respuesta con el template hola.html"""
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))
    else:
        proyecto_cliente=[]
        proyectos_enlace={}
        proyectos_sin_enlace={}
        roles_enlace = []
        roles_sin_enlace = []
        for a in asignacion.objects.all():
            if a.usuario.id == request.user.id:
                rol_lista = rol.objects.get(id = a.rol.id)
                for p in proyecto.objects.all():
                    if p.id == a.proyecto.id:
                        if rol_lista.tiene_permiso('Can change proyecto'):
                            roles_enlace.append(rol_lista)
                        else:
                            roles_sin_enlace.append(rol_lista)
                            if rol_lista.tiene_permiso('Visualizar proyecto') and rol_lista.tiene_permiso('Visualizar equipo'):
                                proyecto_cliente.append(a.proyecto.id)
            if roles_enlace:
                if proyectos_enlace.has_key(a.proyecto):
                    r=list(set(roles_enlace+proyectos_enlace[a.proyecto]))
                    proyectos_enlace[a.proyecto]=r
                else:
                    proyectos_enlace[a.proyecto]=roles_enlace
                roles_enlace=[]
                    
            if roles_sin_enlace:
                if proyectos_sin_enlace.has_key(a.proyecto):
                    r=list(set(roles_sin_enlace+proyectos_sin_enlace[a.proyecto]))
                    proyectos_sin_enlace[a.proyecto]=r
                else:
                    proyectos_sin_enlace[a.proyecto]=roles_sin_enlace
                roles_sin_enlace = []
        proyectos_completo=[]
        for p in proyecto.objects.all():
            if (proyectos_sin_enlace.has_key(p) or proyectos_enlace.has_key(p)):
                proyectos_completo.append(p)
                    
        proyecto_cliente=set(proyecto_cliente)
        return render(request,'hola.html',{'proyectos_completo':proyectos_completo,'proyecto_cliente':proyecto_cliente, 'usuario':request.user, 'proyectos_enlace':proyectos_enlace, 'proyectos_sin_enlace':proyectos_sin_enlace})

def holaScrumView(request,usuario_id,proyectoid,rol_id):
    """
    Vista especial para el usuario scrum en la que le listan los proyectos y los enlaces para la creacion de roles y flujos
    Vista para los usuario comunes, en la que solo se listan los proyectos sin enlaces, ya que no tiene permiso para ello.
    """
    proyectox=proyecto.objects.get(id=proyectoid)
    usuario=MyUser.objects.get(id=usuario_id)
    rolx=rol.objects.get(id=rol_id)
    enlaces=[]
    HUs=[]
    HUsm=[]
    HUs_add_horas=[]
    enlacef=[]
    enlacefm=[]
    enlacefv=[]
    enlaceHU=[]
    enlaceHUv=[]
    enlaceHUm=[]
    enlaceHUa=[]
    enlaceHU_agregar=[]
    enlaceSprint=[]
    enlaceSprintv=[]
    enlaceSprintm=[]
    is_Scrum=0
    HUsa=0
    class enlacex:
        """
        La clase  permite enviar al html solo las url que se corresponden con los permisos contenidos
        en el rol del usuario.
        """
        def __init__(self,urlx,nombrex):
            self.url=urlx
            self.nombre=nombrex
    
    if rolx.tiene_permiso('Can add rol'):
            roles=rol.objects.all()
            enlaces.append(enlacex('/crearRol/'+usuario_id+'/'+proyectoid+'/'+rol_id,'Agregar rol'))
    else:
            roles =[]#lista vacia si no tiene permiso de ver roles
    
    roles_modificables=[]
    roles_inmodificables=[]
    for r in roles:
        x=0
        for a in asignacion.objects.all():
            if a.rol == r:
                x=1
        if x == 0:
            roles_modificables.append(r)
        else:
            roles_inmodificables.append(r)
    if rolx.tiene_permiso('Can add flujo'):
        """Tiene permiso de crear un nuevo flujo, obtengo todos los flujos y enlancef envia el url de crear con el nombre del
        permiso correspondiente al rol-flujo-para-scrum.html"""
        flujos=Flujo.objects.all()
        enlacef.append(enlacex('/crearFlujo/'+usuario_id+'/'+proyectoid+'/'+rol_id,'Agregar Flujo'))
    else:
        flujos = []#lista vacia si no tiene permiso de ver flujos
        
    if rolx.tiene_permiso('Can change flujo'):
        """Tiene permiso de modificar flujo, obtengo todos los flujos para enviar al rol-flujo-para-scrum.html"""
        flujosm=Flujo.objects.all()
        flujos=Flujo.objects.all()
        enlacefm.append(enlacex(usuario_id+'/'+proyectoid+'/'+rol_id,'Modificar Flujo'))
    else:
        flujosm = []#lista vacia si no tiene permiso de ver flujos
        
    if rolx.tiene_permiso('Can add flujo') or rolx.tiene_permiso('Can change flujo'):
        enlacefv.append(enlacex(usuario_id+'/'+proyectoid+'/'+rol_id,'Visualizar'))
    
    if rolx.tiene_permiso('Can add hu'):
        HUs = HU.objects.filter(proyecto=proyectox).filter(estado='ACT')
        enlaceHU.append(enlacex('/crearHU/'+usuario_id+'/'+proyectoid+'/'+rol_id,'Agregar HU'))

    HU_no_asignada_owner=[]
    HU_asignada_owner=[]
    if rolx.tiene_permiso('Can change hu'):
        HUs = HU.objects.filter(proyecto=proyectox)
        HUsm = HU.objects.filter(proyecto=proyectox)
        for HUa in HU.objects.filter(proyecto=proyectox):
            x=0
            for d in delegacion.objects.all():
                if d.hu == HUa:
                    x=1
            if x == 0:
                HU_no_asignada_owner.append(HUa)
            else:
                HU_asignada_owner.append(HUa)
 
        enlaceHUm.append(enlacex(usuario_id+'/'+proyectoid+'/'+rol_id,'Modificar'))
        is_Scrum=0
    elif rolx.tiene_permiso('Can change hu nivel Scrum'):
        HUs = HU.objects.filter(proyecto=proyectox).filter(valido=True)
        HUsm = HU.objects.filter(proyecto=proyectox).filter(valido=True)
        enlaceHUm.append(enlacex(usuario_id+'/'+proyectoid+'/'+rol_id,'Modificar'))
        is_Scrum=1
    
    if rolx.tiene_permiso('Can add hu') or rolx.tiene_permiso('Can change hu') or rolx.tiene_permiso('Can change hu nivel Scrum'):
        enlaceHUv.append(enlacex(usuario_id+'/'+proyectoid+'/'+rol_id,'Visualizar'))
          
    HU_no_asignada=[]
    HU_asignada=[]
    if rolx.tiene_permiso('Can add delegacion'):
        enlaceHUa.append(enlacex(usuario_id+'/'+proyectoid+'/'+rol_id,'Asignar'))
        HUsa=1
        for h in HU.objects.filter(proyecto=proyectox).filter(estado='ACT').filter(valido=True):
                x=0
                for d in delegacion.objects.all():
                    if d.hu == h:
                        x=1
                if x == 0:
                    HU_no_asignada.append(h)
                else:
                    HU_asignada.append(h)
    else:
        HUsa=0
    agregar_horas=[]
    if rolx.tiene_permiso('Agregar horas trabajadas'):
        for d in delegacion.objects.all():
            if d.hu.proyecto == proyectox and str(d.usuario.id) == usuario_id:
                if d.hu.estado == 'ACT':
                    HUs_add_horas.append(d.hu)
        #HU ordenada por prioridad
        HUs_add_horas=sorted(HUs_add_horas,key=lambda x: x.prioridad, reverse=True)
        i=0
        
        for p in HUs_add_horas:
            if p.acumulador_horas != p.duracion:
                agregar_horas=HUs_add_horas[i]             
                enlaceHU_agregar.append(enlacex(usuario_id+'/'+proyectoid+'/'+rol_id,'Agregar horas'))
                break
            i=i+1
        is_Scrum=2
    HUc={}
    HUv=[]
    if rolx.tiene_permiso('Visualizar HU'):
        HUv=HU.objects.filter(proyecto=proyectox).filter(estado='ACT')
        for h in HUv:
            hay=0
            for d in delegacion.objects.all():
                if d.hu == h:
                    HUc[h]=d.usuario
                    hay=1
            if hay == 0:
                HUc[h]=None
                
    if rolx.tiene_permiso('Can add sprint'):
        enlaceSprint.append(enlacex('/crearSprint/'+usuario_id+'/'+proyectoid+'/'+rol_id,'Agregar Sprint'))
    else:
        sprints = []#lista vacia si no tiene permiso de ver flujos
        
    if rolx.tiene_permiso('Can change sprint'):
        """Tiene permiso de modificar flujo, obtengo todos los flujos para enviar al rol-flujo-para-scrum.html"""
        sprintsm=Sprint.objects.filter(proyecto=proyectox)
        sprints=Sprint.objects.filter(proyecto=proyectox)
        enlaceSprintm.append(enlacex(usuario_id+'/'+proyectoid+'/'+rol_id,'Modificar Sprint'))
    else:
        sprintsm = []#lista vacia si no tiene permiso de ver flujos
        
    if rolx.tiene_permiso('Can add sprint') or rolx.tiene_permiso('Can change sprint'):
        enlaceSprintv.append(enlacex(usuario_id+'/'+proyectoid+'/'+rol_id,'Visualizar'))
          
    return render(request,'rol-flujo-para-scrum.html',{'roles_inmodificables':roles_inmodificables,'roles_modificables':roles_modificables,'HU_asignada':HU_asignada, 'HU_no_asignada':HU_no_asignada,'HUv':HUv,'HUc':HUc,'sprints':sprints,'enlaceSprint':enlaceSprint,'sprintsf':sprintsm,'enlaceSprintm':enlaceSprintm,'enlaceSprintv':enlaceSprintv,'enlaceHUa':enlaceHUa,'HUsa':HUsa,'is_Scrum':is_Scrum,'HUs_add_horas':HUs_add_horas, 'enlaceHU_agregar':enlaceHU_agregar,'enlaceHUm':enlaceHUm,'HUsm':HUsm,'enlaceHUv':enlaceHUv,'HUs':HUs,'enlaceHU':enlaceHU,'enlacefv':enlacefv,'enlacefm':enlacefm,'enlacef':enlacef,'enlaces':enlaces,'roles':roles,'flujosm':flujosm, 'flujos':flujos,'proyecto':proyectox,'usuario':usuario,'rolid':rol_id, 'HU_asignada_owner':HU_asignada_owner, 'HU_no_asignada_owner':HU_no_asignada_owner, 'HU_cargar':agregar_horas})
    #ahora voy a checkear si el usuario tiene permiso de agregar rol y en base a eso va ver la interfaz de administracion de rol

def registrarUsuarioView(request):
    """Vista que se obtiene del regex /registrar solicitado al precionar el boton
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
    
def modificarCuenta(request, usuario_id):
    """
    Vista que permite a los usuarios activos modificar sus datos personales como
    el su nombre, apellido y direccion.
    El correo y su nombre identificador del usuario solo lo podra modificar el admin.
    """
    usuario = MyUser.objects.get(id=usuario_id)
    if request.method == 'POST':
        usuario.user_name=request.POST['user_name']
        usuario.last_name=request.POST['last_name']
        usuario.direccion=request.POST['direccion']
        usuario.save()
        return HttpResponse('Su cuenta se ha modificado exitosamente')
    else:
        return render_to_response('modificarUsuario.html', {'usuario': usuario},
                              context_instance=RequestContext(request))
    
def guardarRolView(request,usuario_id):
    """Vista de guardado de un nuevo rol en la base de datos
    que se utiliza en la interfaz devuelta por /crearRol/ """
    try:
        usuario=MyUser.objects.get(id=usuario_id)
        rol_a_crear = rol.objects.create(nombre_rol_id=request.POST['nombre_rol_id'], descripcion=request.POST['descripcion'],usuario_creador=usuario, estado='ACT')
        for p in request.POST.getlist('permisos'):
            rol_a_crear.permisos.add(Permission.objects.get(id=p))
        rol_a_crear.save()
        return HttpResponse('El rol se ha creado')
      
    except ObjectDoesNotExist:
        print "Either the entry or blog doesn't exist." 
        return HttpResponseRedirect('/crearRol/')
    
def guardarFlujoView(request, usuario_id, proyectoid, rolid):
    """Vista de guardado de un nuevo flujo en la base de datos
    que se utiliza en la interfaz devuelta por /crearFlujo/ """
    actividades_disponibles=Actividades.objects.all()
    actividades_asignadas=[]
    guardar=0
    for g in request.POST.getlist('_save'):
        if g == 'Guardar':
            guardar=1
    if guardar == 1:
        flujo_a_crear = Flujo.objects.create(nombre=request.POST['nombre'],estado="ACT")
        orden=[]
        for p in request.POST.getlist('actividades'):
            orden.append(Actividades.objects.get(id=p).id)
            flujo_a_crear.actividades.add(Actividades.objects.get(id=p))
        flujo_a_crear.orden_actividades=json.dumps(orden)
        flujo_a_crear.save()
        return HttpResponse('El flujo se ha creado'+str(request.POST.getlist('actividades')))
    else:
        if request.POST['boton'] == 'Agregar':
            act_asi=request.POST.getlist('actividades_asignadas')
            for a in act_asi:
                actividades_disponibles=actividades_disponibles.exclude(id=a)
                actividades_asignadas.append(Actividades.objects.get(id=a))
            act_dis=request.POST.getlist('actividades_disponibles')
            for a in act_dis:
                actividades_asignadas.append(Actividades.objects.get(id=a))
                actividades_disponibles=actividades_disponibles.exclude(id=a)
            return render(request, 'crearFlujo.html',{'nombre_flujo':request.POST['nombre'],'proyectoid':proyectoid,'usuarioid':usuario_id,'rolid':rolid ,'actividades_asignadas':actividades_asignadas,'actividades':actividades_disponibles})
        elif request.POST['boton'] == 'Eliminar':
            act_asi=request.POST.getlist('actividades_asignadas')
            for a in act_asi:
                actividades_disponibles=actividades_disponibles.exclude(id=a)
                actividades_asignadas.append(Actividades.objects.get(id=a))
            return render(request, 'crearFlujo.html',{'nombre_flujo':request.POST['nombre'],'proyectoid':proyectoid,'usuarioid':usuario_id,'rolid':rolid ,'actividades_asignadas':actividades_asignadas,'actividades':actividades_disponibles})     

    
def guardarHUView(request,proyectoid):
    """Vista de guardado de una nueva HU en la base de datos creada por el Product Owner
    que se utiliza en la interfaz devuelta por /crearHU/"""
    try:
        proyectox = proyecto.objects.get(id=proyectoid)
        HU_a_crear = HU.objects.create(descripcion=request.POST['descripcion'],estado="ACT",valor_negocio=request.POST['valor_negocio'], valor_tecnico=0, prioridad=0, duracion=0, acumulador_horas=0, estado_en_actividad='PEN',proyecto=proyectox,valido=False)
        HU_a_crear.save()
        return HttpResponse('La HU se ha creado y relacionado con el proyecto')  
    except ObjectDoesNotExist:
        print "Either the entry or blog doesn't exist." 
        return HttpResponseRedirect('/crearHU/')

def guardarSprintView(request, usuario_id, proyectoid, rolid):
    """Vista de guardado de un nuevo Sprint en la Base de datos
    que se utiliza en la interfaz devuelta por /crearSprint/"""
    guardar=0
    for g in request.POST.getlist('_save'):
        if g == 'Guardar':
            guardar=1
    if guardar == 1:
        try:
            Sprint_a_crear = Sprint.objects.create(descripcion=request.POST['descripcion'],estado="ACT",fecha_inicio=request.POST['fecha_inicio'], duracion=request.POST['duracion'], proyecto=proyecto.objects.get(id=proyectoid))
            for p in request.POST.getlist('HUs'):
                Sprint_a_crear.hu.add(HU.objects.get(id=p))
            for f in request.POST.getlist('Flujos'):
                Sprint_a_crear.flujo.add(Flujo.objects.get(id=f))
            Sprint_a_crear.save()
            return HttpResponse('El Sprint se ha creado')  
        except ObjectDoesNotExist:
            print "Either the entry or blog doesn't exist." 
            return HttpResponseRedirect('/crearSprint/')
    else:
        if request.POST['boton'] == 'Calcular':
            proyectox = proyecto.objects.get(id=proyectoid)
            HUs = HU.objects.filter(proyecto=proyectox)
            flujos=Flujo.objects.all()#le mando todos los flujos para que elija los que quiere
            for x in Sprint.objects.all():
                for h in x.hu.all():
                    HUs=HUs.exclude(id=h.id)
            max=0
            hus_seleccionadas=[]
            HUs_no_seleccionadas=HUs
            for h in request.POST.getlist('HUs'):
                hus_seleccionadas.append(HU.objects.get(id=h))
                HUs_no_seleccionadas=HUs_no_seleccionadas.exclude(id=h)
                if HU.objects.get(id=h).duracion > max:
                    max=HU.objects.get(id=h).duracion
        return render(request, 'crearSprint.html',{'nombre':request.POST['descripcion'],'duracion':int(max/8),'flujos':flujos,'HUs':HUs,'HUs_seleccionadas':hus_seleccionadas,'HUs_no_seleccionadas':HUs_no_seleccionadas,'fecha_ahora':str(datetime.now()),'usuarioid':usuario_id,'proyectoid':proyectoid,'rolid':rolid})
            
def guardarHUProdOwnerView(request,usuario_id, proyectoid, rolid, HU_id_rec,is_Scrum):
    """Vista de guardado de la modificacion de una HU existente modificada por el Product Owner
    que se utiliza en la interfaz devuelta por /modificarHU/ 
    @0: corresponde a la modificaci[on realizada por el Product Owner
    @1: coresponde a la modificaci[on realizada por el Scrum
    @2: corresponde a la modificaci[on realizada por el Equipo"""
          
    h=HU.objects.get(id=HU_id_rec)
    if request.method == 'POST':
        if is_Scrum == '0':
            valor_negocio=request.POST['valor_negocio']
            descripcion=request.POST['descripcion']
            estado=request.POST['estado']
            h.valor_negocio=valor_negocio
            h.descripcion=descripcion
            h.estado=estado
            h.save() #Guardamos el modelo de manera Editada
            return HttpResponse('La descripcion y valor de negocio de la HU a sido modificado exitosamente')
        else:
            guardar=0
            for g in request.POST.getlist('_save'):
                if g == 'Guardar':
                    guardar=1
            if guardar == 1:
                try:
                    proyectox=proyecto.objects.get(id=h.proyecto.id)
                    horas_a_agregar = request.POST['horas_agregar']
                    descripcion_horas=request.POST['descripcion_horas']
                    hd=HU_descripcion.objects.create(horas_trabajadas=horas_a_agregar,descripcion_horas_trabajadas=descripcion_horas)
                    h.hu_descripcion.add(HU_descripcion.objects.get(id=hd.id))
                    hd.save()
                    acumulador_horas = float(horas_a_agregar)+h.acumulador_horas
                    if h.duracion >= acumulador_horas:
                        h.acumulador_horas=acumulador_horas
                        h.estado_en_actividad='PRO'
                        h.save()
                        if proyectox.estado == 'PEN' and acumulador_horas > 0:
                            proyectox.estado='ACT'
                            proyectox.save()               
                        return render(request,'modificarHU.html', {'HU':h, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid,'is_Scrum':2})
                    else:
                        return HttpResponse('Contactar con el Scrum para aumentar la duracion de la HU, ya que ha sobrepasado el tiempo de realizacion de HU')
                except ObjectDoesNotExist:
                    print "Either the entry or blog doesn't exist." 
                    return HttpResponseRedirect('/crearHU/')
            else:
                acumulador=0
                prueba=request.POST['horas_agregar']
                acumulador=acumulador + float(prueba)
                y=str(timezone.now())
                for horas in h.hu_descripcion.all():
                    x=str(horas.fecha)
                    if x[:10] == y[:10]:
                        acumulador=horas.horas_trabajadas + acumulador
                if request.POST['boton'] == 'Finalizar':
                    for a in asignaHU_actividad_flujo.objects.all():
                        for hu in a.lista_de_HU.all():
                            if hu==h:
                                flujo=a.flujo_al_que_pertenece
                                break
                    jsonDec = json.decoder.JSONDecoder()
                    orden=jsonDec.decode(flujo.orden_actividades)
                    if acumulador<9:     
                        proyectox=proyecto.objects.get(id=h.proyecto.id)
                        horas_a_agregar = request.POST['horas_agregar']
                        descripcion_horas=request.POST['descripcion_horas']
                        fecha=timezone.now()
                        hd=HU_descripcion.objects.create(horas_trabajadas=horas_a_agregar,descripcion_horas_trabajadas=descripcion_horas, fecha=fecha)
                        h.hu_descripcion.add(HU_descripcion.objects.get(id=hd.id))
                        hd.save()
                        acumulador_horas = float(horas_a_agregar)+h.acumulador_horas
                        if h.duracion >= acumulador_horas:
                            h.acumulador_horas=acumulador_horas
                            h.save()
                        x=1
                        for o in orden:
                            if Actividades.objects.get(id=o) == h.actividad:
                                break
                            else:
                                x=x+1
                        if x >= len(orden) and h.acumulador_horas <= h.duracion:
                            h.estado_en_actividad='FIN'
                            h.save()
                            return HttpResponse("Todas las actividades de HU finalizadas")
                        elif x < len(orden) and h.acumulador_horas == h.duracion:
                            h.estado_en_actividad='PEN'
                            h.save()
                            return HttpResponse("Duracion de HU finalizada sin terminar todas las actividades. Contactar con el Scrum")
                        else:
                            h.actividad=Actividades.objects.get(id=orden[x])
                            h.estado_en_actividad='PEN'
                            h.save()
                            return render(request,'modificarHU.html', {'HU':h, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid,'is_Scrum':2})
                    else:
                        return HttpResponse('Las Horas cargadas ya superan las 8 Horas diarias que deben cargarse por dia') 

class FormularioContacto(forms.Form):
    """
    Clase utilizada para obtener el formulario de peticion de seto de contrasenha.
    """
    usuario = forms.CharField()
    correo = forms.EmailField()

class FormularioSeteoContrasenha(forms.Form):
    """
    Clase utilizada para obtener el formulario de seteo de contrasenha.
    """
    password_nueva1 = forms.CharField(widget=forms.PasswordInput)
    password_nueva2 = forms.CharField(widget=forms.PasswordInput)
    
def contactomail(request):
    """
    Vista que obtiene los datos del usuario como su nombre identificador de usuario y correo,
    comprueba que el correo le pertenezca y envia la direccion correspondiente al seteo de su contrasenha
    a su correo. En caso de que su correo no coincida con el que le corresponda, notifica al usuario.
    """
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
    """
    Vista que se despliega al estar en el direccionamiento de configuracion de contrasenha,
    comprueba que ambas contrasenhas intruducidas por el usuario coincidan, en caso de que coincidan
    se almacena la nueva contrasenha en la Base de Datos y en caso de que no coincidan se le notifica al usuario.
    """
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
    """
    Clase que obtiene el formulario para la creacion, visualizacion y modificacion
    de roles de proyecto desde la vista del Scrum.
    """
    class Meta:
        model= rol
        fields=['permisos','nombre_rol_id','descripcion','estado']

def visualizarRolProyectoView(request,usuario_id,proyectoid, rolid, rol_id_rec):
    """
    Vista que utiliza el formulario RolProyecto para desplegar los datos almacenados
    en el Rol que se quiere visualizar.
    """
    rolproyecto= rol.objects.get(id=rol_id_rec)
    formulario =  FormularioRolProyecto(initial={
                                                     'nombre_rol_id': rolproyecto.nombre_rol_id,
                                                     'permisos': rolproyecto.permisos,
                                                     'descripcion': rolproyecto.descripcion,
                                                     'estado':rolproyecto.estado,
                                                     }) 
    return render_to_response('visualizarRol.html',{'formulario':formulario, 'rol':rolproyecto, 'proyectoid':proyectoid,'usuarioid':usuario_id,'rolid':rolid},
                                  context_instance=RequestContext(request))
        
def modificarRol(request, usuario_id, proyectoid, rolid, rol_id_rec):
    """
    Vista que utiliza el formulario RolProyecto para desplegar los datos editables
    del Rol que se quiere modificar.
    """
    f=rol.objects.get(id=rol_id_rec)
    u=MyUser.objects.get(id=usuario_id)
    if request.method == 'POST':
        form = FormularioRolProyecto(request.POST)
        if form.is_valid():
            nombre_rol_id=form.cleaned_data['nombre_rol_id']
            descripcion=form.cleaned_data['descripcion']
            permisos=form.cleaned_data['permisos']
            estado=form.cleaned_data['estado']
            f.nombre_rol_id=nombre_rol_id
            f.descripcion=descripcion
            f.permisos=permisos
            f.usuario_creador=u
            f.estado=estado
            f.save() #Guardamos el modelo de manera Editada
            return HttpResponse('El rol ha sido modificado exitosamente')
        else:
            return HttpResponse('Error'+str(form.errors))
    else:
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
        form = FormularioRolProyecto(initial={
                                         'nombre_rol_id': f.nombre_rol_id,
                                         'descripcion': f.descripcion,
                                         'permisos': f.permisos,
   
                                         })
        lista_restante=[]
        for permitido in permisos.all():
            x=0
            for perm_rol in f.permisos.all():
                if permitido.id==perm_rol.id:
                    x=1
            if x==0:
                lista_restante.append(permitido)
        estados=['ACT','CAN']
        ctx = {'form':form, 'rol':f, 'proyectoid':proyectoid,'usuarioid':usuario_id,'rolid':rolid ,'permisos':lista_restante,'estados':estados}
        return render_to_response('modificarRol.html', ctx ,context_instance=RequestContext(request))

class FormularioFlujoProyecto(forms.ModelForm):
    """
    Clase que obtiene el formulario para la creacion, visualizacion y modificacion
    de flujos de proyecto desde la vista del Scrum.
    """
    class Meta:
        model= Flujo
        fields=['nombre','estado','actividades']
        widgets = {
            'actividades': CheckboxSelectMultiple(),
        }
        
def visualizarFlujoProyectoView(request,usuario_id, proyectoid, rolid, flujo_id_rec):
    """
    Vista que utiliza el formulario FlujoProyecto para desplegar los datos almacenados
    en el Flujo que se quiere visualizar.
    """
    flujo_disponible= Flujo.objects.get(id=flujo_id_rec)
    jsonDec = json.decoder.JSONDecoder()
    orden=jsonDec.decode(flujo_disponible.orden_actividades)
    formulario =  FormularioRolProyecto(initial={
                                                     'nombre': flujo_disponible.nombre,
                                                     'estado': flujo_disponible.estado,
                                                     'actividades': flujo_disponible.actividades,
                                                     })      
    return render_to_response('visualizarFlujo.html',{'formulario':formulario, 'orden':orden,'flujo':flujo_disponible, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid},
                                  context_instance=RequestContext(request))

def modificarFlujo(request, usuario_id, proyectoid, rolid, flujo_id_rec):
    """
    Vista que utiliza el formulario FlujoProyecto para desplegar los datos editables
    del Flujo que se quiere modificar.
    """
    actividades_disponibles=Actividades.objects.all()
    actividades_asignadas=[]
    estados=['ACT','CAN']
    f=Flujo.objects.get(id=flujo_id_rec)
    guardar=0
    for g in request.POST.getlist('_save'):
        if g == 'Guardar':
            guardar=2
        elif g=='Guardar nuevo':
            guardar=1
    if request.method == 'POST':
        if guardar ==0:
            if request.POST['boton'] == 'Agregar':
                act_asi=request.POST.getlist('actividades_asignadas')
                if act_asi:
                    for a in act_asi:
                        actividades_disponibles=actividades_disponibles.exclude(id=a)
                        actividades_asignadas.append(Actividades.objects.get(id=a))
                act_dis=request.POST.getlist('actividades_disponibles')
                for a in act_dis:
                    actividades_asignadas.append(Actividades.objects.get(id=a))
                    actividades_disponibles=actividades_disponibles.exclude(id=a)
                ctx = {'estados':estados,'actividades_asignadas':actividades_asignadas,'actividades':actividades_disponibles,'flujo':f, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid}
                return render(request,'modificarFlujo.html', ctx)
            elif request.POST['boton'] == 'Eliminar':
                act_asi=request.POST.getlist('actividades_asignadas')
                for a in act_asi:
                    actividades_disponibles=actividades_disponibles.exclude(id=a)
                    actividades_asignadas.append(Actividades.objects.get(id=a))
                ctx = {'estados':estados,'actividades_asignadas':actividades_asignadas,'actividades':actividades_disponibles,'flujo':f, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid}
                return render(request,'modificarFlujo.html', ctx)
        elif guardar == 1:
            nombre=request.POST['nombre']
            estado=request.POST['estado']
            try:
                flujo_a_crear = Flujo.objects.create(nombre=nombre,estado="ACT")
                orden=[]
                for p in request.POST.getlist('actividades_asignadas'):
                    orden.append(Actividades.objects.get(id=p).id)
                    flujo_a_crear.actividades.add(Actividades.objects.get(id=p))
                flujo_a_crear.orden_actividades=json.dumps(orden)
                flujo_a_crear.save()
                return HttpResponse('El flujo nuevo se ha creado')  
            except ObjectDoesNotExist:
                print "No se ha podido crear el nuevo flujo" 
            return HttpResponse('El flujo ha sido creado exitosamente')
        elif guardar == 2:
            nombre=request.POST['nombre']
            estado=request.POST['estado']
            f.nombre=nombre
            f.estado=estado
            orden=[]
            f.actividades=[]
            f.orden_actividades=orden
            for p in request.POST.getlist('actividades_asignadas'):
                orden.append(Actividades.objects.get(id=p).id)
                f.actividades.add(Actividades.objects.get(id=p))
            f.orden_actividades=json.dumps(orden)
            f.save() #Guardamos el modelo de manera Editada
            return HttpResponse('El flujo ha sido modificado exitosamente')
    else:
        actividades_asignadas=[]
        actividades_disponibles=[]
        jsonDec = json.decoder.JSONDecoder()
        orden=jsonDec.decode(f.orden_actividades)
        for o in orden:
            for a in f.actividades.all():
                if a.id == o:
                    actividades_asignadas.append(a)
        for a in Actividades.objects.all():
            x=0
            for asig in actividades_asignadas:
                if a == asig:
                    x=1
            if x == 0:
                actividades_disponibles.append(a)
        
        ctx = {'estados':estados,'actividades_asignadas':actividades_asignadas,'actividades':actividades_disponibles,'flujo':f, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid}
        return render_to_response('modificarFlujo.html', ctx ,context_instance=RequestContext(request))

class FormularioSprintProyecto(forms.ModelForm):
    """
    Clase que obtiene el formulario para la creacion, visualizacion y modificacion
    de sprints del proyecto desde la vista del Scrum.
    """
    class Meta:
        model= Sprint
        fields=['descripcion','fecha_inicio','duracion','estado','hu','flujo']
        
def visualizarSprintProyectoView(request,usuario_id, proyectoid, rolid, Sprint_id_rec):
    """
    Vista que utiliza el formulario SprintProyecto para desplegar los datos almacenados
    en el Sprint que se quiere visualizar.
    """
    Sprint_disponible= Sprint.objects.get(id=Sprint_id_rec)
    formulario =  FormularioSprintProyecto(initial={
                                                     'descripcion': Sprint_disponible.descripcion,
                                                     'fecha_inicio': Sprint_disponible.fecha_inicio,
                                                     'duracion': Sprint_disponible.duracion,
                                                     'estado': Sprint_disponible.estado,
                                                     })      
    return render_to_response('visualizarSprint.html',{'formulario':formulario, 'Sprint':Sprint_disponible, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid},
                                  context_instance=RequestContext(request))

def modificarSprint(request, usuario_id, proyectoid, rolid, Sprint_id_rec):
    """
    Vista que utiliza el formulario SprintProyecto para desplegar los datos editables
    del Sprint que se quiere modificar.
    La lista de HU asignables se dividen en dos sublistas: las ya asignadas a algun sprint y las que aun
    no han sido asignadas.
    """
    estados=['ACT','CAN','CON']
    s=Sprint.objects.get(id=Sprint_id_rec)
    if request.method == 'POST':
        form = FormularioSprintProyecto(request.POST)
        if form.is_valid():
            descripcion=form.cleaned_data['descripcion']
            estado=form.cleaned_data['estado']
            fecha_inicio=form.cleaned_data['fecha_inicio']
            duracion=form.cleaned_data['duracion']
            hu=form.cleaned_data['hu']
            flujo=form.cleaned_data['flujo']
            s.descripcion=descripcion
            s.estado=estado
            s.fecha_inicio=fecha_inicio
            s.duracion=duracion
            s.hu=hu
            s.flujo=flujo
            s.save() #Guardamos el modelo de manera Editada
            return HttpResponse('El Sprint ha sido modificado exitosamente')
        else:
            return HttpResponse('El Sprint no es valido'+str(form.errors))
    else:    
        form = FormularioSprintProyecto(initial={
                                         'descripcion': s.descripcion,
                                         'estado': s.estado,
                                         'fecha_inicio': s.fecha_inicio,
                                         'duracion': s.duracion,
                                         'hu':[t.id for t in s.hu.all()],
                                         'flujo':[x.id for x in s.flujo.all()]
   
                                         })
        proyectox=proyecto.objects.get(id=proyectoid)
        HUs = HU.objects.filter(proyecto=proyectox)
        flujos=Flujo.objects.all()
        for x in Sprint.objects.all():
            for h in x.hu.all():
                HUs=HUs.exclude(id=h.id)
                
        lista_restante=[]
        for permitido in HUs:
            x=0
            for perm_hu in s.hu.all():
                if permitido.id==perm_hu.id:
                    x=1
            if x==0:
                lista_restante.append(permitido)
        fecha = str(s.fecha_inicio)
        
        ctx = {'flujos':flujos,'estados':estados, 'fecha':fecha[:-6],'form':form,'HUs':HUs,'lista_HU_sin_asignar':lista_restante,'Sprint':s, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid}
        return render_to_response('modificarSprint.html', ctx ,context_instance=RequestContext(request))
    
class FormularioHU(forms.ModelForm):
    """
    Clase que obtiene el formulario para la creacion, visualizacion y modificacion
    de HU's del proyecto desde la vista del Scrum y del Product Owner.
    """
    class Meta:
        model= HU
        fields=['valor_tecnico','prioridad','duracion']
        
def visualizarHUView(request,usuario_id, proyectoid, rolid, HU_id_rec,is_Scrum):
    """
    Vista que utiliza el formulario HU para desplegar los datos almacenados
    en la HU que se quiere visualizar.
    """
    HU_disponible= HU.objects.get(id=HU_id_rec)
    adjuntos=archivoadjunto.objects.filter(hU=HU_disponible)
    formulario =  FormularioHU(initial={
                                                     'descripcion': HU_disponible.descripcion,
                                                     'valor_negocio': HU_disponible.valor_negocio,
                                                     })      
    return render_to_response('visualizarHU.html',{'formulario':formulario, 'HU':HU_disponible, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid,'adjuntos':adjuntos,'is_Scrum':is_Scrum},
                                  context_instance=RequestContext(request))

def modificarHU(request, usuario_id, proyectoid, rolid, HU_id_rec,is_Scrum):
    """
    Vista que utiliza el formulario HU para desplegar los datos editables
    de la HU en tres niveles de modificacion.
    Esta vista corresponde a la modificacion del nivel 1, es decir, a nivell Scrum Master
    """
    estados=['ACT','CAN']
    VALORES10_CHOICES = range(1,10)
    h=HU.objects.get(id=HU_id_rec)
    if (is_Scrum == '1'):
        if request.method == 'POST':
            form = FormularioHU(request.POST)
            if form.is_valid():
                valor_tecnico=form.cleaned_data['valor_tecnico']
                prioridad=form.cleaned_data['prioridad']
                duracion=form.cleaned_data['duracion']
                #estado=form.cleaned_data['estado']
                h.valor_tecnico=valor_tecnico
                h.prioridad=prioridad
                h.duracion=duracion
                #h.estado=estado
                h.save() #Guardamos el modelo de manera Editada
                return HttpResponse('La HU ha sido modificado exitosamente')
            else:
                return HttpResponse('error'+str(form.errors))
        else:
        
            form = FormularioHU(initial={
                                        'valor_tecnico': h.valor_tecnico,
                                        'prioridad': h.prioridad,
                                        'duracion':h.duracion,
                                        #'estado':h.estado
                                         })
            ctx = {'valores':VALORES10_CHOICES,'form':form, 'HU':h, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid,'is_Scrum':is_Scrum}
            return render_to_response('modificarHU.html', ctx ,context_instance=RequestContext(request))
    else:
        return render(request,'modificarHU.html', {'estados':estados, 'valores':VALORES10_CHOICES,'HU':h, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid,'is_Scrum':is_Scrum})

def crearRol(request,usuario_id,proyectoid,rolid):
    """
    Vista que realiza la creacion de roles de proyecto desde la vista del Scrum, excluyendo aquellos permisos que no corresponde
    ser vistos por el usuario Scrum.
    """
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
        return render(request, 'crearRol.html',{'permissions':permisos,'usuarioid':usuario_id,'proyectoid':proyectoid,'rolid':rolid})
    
def crearFlujo(request,usuario_id,proyectoid,rolid):
    """
    Vista que realiza la creacion de flujos de proyecto desde la vista del Scrum.
    """
    actividades_asignadas=[]
    actividades_disponibles=Actividades.objects.all()
    if request.method == 'GET':
        return render(request, 'crearFlujo.html',{'actividades_asignadas':actividades_asignadas,'actividades':actividades_disponibles,'usuarioid':usuario_id,'proyectoid':proyectoid,'rolid':rolid})
        
def crearSprint(request,usuario_id,proyectoid,rolid):
    """
    Vista que realiza la creacion de flujos de proyecto desde la vista del Scrum.
    """
    proyectox = proyecto.objects.get(id=proyectoid)
    HUs = HU.objects.filter(proyecto=proyectox)
    flujos=Flujo.objects.all()#le mando todos los flujos para que elija los que quiere
    for x in Sprint.objects.all():
        for h in x.hu.all():
            HUs=HUs.exclude(id=h.id)
    if request.method == 'GET':
        return render(request, 'crearSprint.html',{'HUs_no_seleccionadas':HUs,'flujos':flujos,'HUs':HUs,'fecha_ahora':str(datetime.now()),'usuarioid':usuario_id,'proyectoid':proyectoid,'rolid':rolid})

def crearHU(request,usuario_id,proyectoid,rolid):
    """
    Vista que realiza la creacion de flujos de proyecto desde la vista del Scrum.
    """
    VALORES10_CHOICES = range(1,10)
    if request.method == 'GET':
        return render(request, 'crearHU.html',{'usuarioid':usuario_id,'proyectoid':proyectoid,'rolid':rolid,'valores':VALORES10_CHOICES})
    
class proyectoFrom(forms.ModelForm):
    """
    Clase que obtiene el formulario para la visualizacion y modificacion de proyectos desde la vista del Scrum.
    """
    class Meta:
        model = proyecto
        fields = ['nombre_corto', 'nombre_largo', 'descripcion','estado','fecha_inicio','fecha_fin']

def modificarProyecto(request, usuario_id, proyecto_id_rec):
    """
    Vista que utiliza el formulario proyectoFrom para desplegar los datos editables
    del Proyecto que se quiere modificar.
    """
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
    """
    Vista que utiliza el formulario proyectoFrom para desplegar los datos almacenados
    en el Flujo que se quiere visualizar.
    """
    proyecto_enc= proyecto.objects.get(id=proyecto_id_rec)
    return render_to_response('visualizarProyecto.html',{'proyecto':proyecto_enc,'usuarioid':usuario_id},
                                  context_instance=RequestContext(request))

def crearActividadView(request,usuario_id,proyectoid):
    """
    Vista que se obtiene del regex al presionar el boton Crear Actividad dentro del formulario
    de creacion o modificacion de Flujos, devolviendo un formulario html para crear una nueva actividad
    """  
    if request.method == 'GET':
        form = formularioActividad()
        return render_to_response("crearActividad.html",{"form":form,'usuarioid':usuario_id,'proyectoid':proyectoid}, context_instance = RequestContext(request))
    
    else:#request.method == 'POST'
        form = formularioActividad(request.POST)
        if form.is_valid():
            nombre=form.cleaned_data['nombre']
            descripcion=form.cleaned_data['descripcion']
            form.nombre=nombre
            form.descripcion=descripcion
            form.save()
            return HttpResponse('Ha sido guardado exitosamente')       

def crearActividadAdminView(request):
    """
    Vista que se obtiene del regex al presionar el boton Crear Actividad dentro del formulario
    de creacion o modificacion de Flujos del admin, devolviendo un formulario html para crear una nueva actividad
    """  
    if request.method == 'GET':
        form = formularioActividad()
        return render_to_response("crearActividadAdmin.html",{"form":form,}, context_instance = RequestContext(request))
    
    else:#request.method == 'POST'
        form = formularioActividad(request.POST)
        if form.is_valid():
            nombre=form.cleaned_data['nombre']
            descripcion=form.cleaned_data['descripcion']
            form.nombre=nombre
            form.descripcion=descripcion
            form.save()
            return HttpResponse('Ha sido guardado exitosamente')  
        
def seleccionarFlujoModificarAdmin(request):
    """
    Al presionar el boton Modificar Actividad en el admin, esta vista despliega una lista de todas las actividades 
    seleccionables por el usuario para su modificacion.
    """
    return render(request,'seleccionarActividadAdmin.html',{'actividades':Actividades.objects.all(),})

def modificarActividadAdmin(request,actividad_id_rec):
    """
    Vista que utiliza el formulario formularioActividad para desplegar los datos editables en el admin
    de la Actividad que se quiere modificar.
    """
    p=Actividades.objects.get(id=actividad_id_rec)
    if request.method == 'POST':
        form = formularioActividad(request.POST)
        if form.is_valid():
            nombre=form.cleaned_data['nombre']
            descripcion=form.cleaned_data['descripcion']
            p.nombre=nombre
            p.descripcion=descripcion
            p.save() #Guardamos el modelo de manera Editada
            return HttpResponse('Se ha guardado exitosamente')
    else:
        
        form = formularioActividad(initial={
                                         'nombre': p.nombre,
                                         'descripcion': p.descripcion,                                     
                                         })
        ctx = {'form':form, 'Actividad':p,}
        return render_to_response('modificarActividadAdmin.html', ctx ,context_instance=RequestContext(request)) 
 
class formularioActividad(forms.ModelForm):
    """
    Clase que obtiene el formulario para la creacion y modificacion de actividades desde la vista del Scrum y el admin.
    """
    class Meta:
        model=Actividades
        fields = ('nombre', 'descripcion')
        
def seleccionarFlujoModificar(request,usuario_id,proyectoid):
    """
    Al presionar el boton Modificar Actividad, esta vista despliega una lista de todas las actividades seleccionables por el usuario
    para su modificacion.
    """
    return render(request,'seleccionarActividad.html',{'actividades':Actividades.objects.all(),'usuarioid':usuario_id,'proyectoid':proyectoid})

def modificarActividad(request,usuario_id,proyectoid,actividad_id_rec):
    """
    Vista que utiliza el formulario formularioActividad para desplegar los datos editables
    de la Actividad que se quiere modificar.
    """
    p=Actividades.objects.get(id=actividad_id_rec)
    if request.method == 'POST':
        form = formularioActividad(request.POST)
        if form.is_valid():
            nombre=form.cleaned_data['nombre']
            descripcion=form.cleaned_data['descripcion']
            p.nombre=nombre
            p.descripcion=descripcion
            p.save() #Guardamos el modelo de manera Editada
            return HttpResponse('Se ha guardado exitosamente')
    else:
        
        form = formularioActividad(initial={
                                         'nombre': p.nombre,
                                         'descripcion': p.descripcion,                                     
                                         })
        ctx = {'form':form, 'Actividad':p,'usuarioid':usuario_id,'proyectoid':proyectoid}
        return render_to_response('modificarActividad.html', ctx ,context_instance=RequestContext(request)) 
 
    
def asignarRol(request,usuario_id, proyectoid,rolid, rol_id_rec):
    """
    Vista que permite asignar un rol a un usuario dentro de la vista del Scrum, valiendose de la URL para obtener
    los id's del rol , proyecto ye l usuario creador.
    """
    proyectox=proyecto.objects.get(id=proyectoid)
    rolx = rol.objects.get(id=rol_id_rec)
    x=0
    if request.method=='POST':
        try:
            for p in request.POST.getlist('usuarios'):
                u=MyUser.objects.get(id=p)
                for a in asignacion.objects.all():
                    if a.usuario == u and a.rol == rolx and a.proyecto == proyectox:
                        x=1
            if x == 0:
                asignacion_a_crear = asignacion.objects.create(usuario=u,rol=rolx, proyecto=proyectox)
                asignacion_a_crear.save()
            return HttpResponseRedirect('/scrum/'+usuario_id+'/'+proyectoid+'/'+rolid+'/')
        except ObjectDoesNotExist:
            print "Either the entry or blog doesn't exist." 
            return HttpResponseRedirect('/crearFlujo/')
    else:
        usuarios_ya_asignados=[]
        for a in asignacion.objects.all():
            if a.rol == rol.objects.get(id=rol_id_rec) and a.proyecto == proyectox:
                usuarios_ya_asignados.append(a.usuario)
        usuarios_ya_asignados=set(usuarios_ya_asignados)
        
        usuarios_sin_asignar=[]
        for u in MyUser.objects.all().exclude(id=usuario_id).exclude(username='admin'):
            x=0
            for u_asig in usuarios_ya_asignados:
                if u == u_asig:
                    x=1
            if x==0:
                usuarios_sin_asignar.append(u)
        return render(request,'asignaRolProyecto.html',{'usuarios_sin_asignar':usuarios_sin_asignar,'usuarios_ya_asignados':usuarios_ya_asignados,'proyecto':proyectox,'usuarios':MyUser.objects.all().exclude(id=usuario_id),'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid})
    
    
    
def listarEquipo(request,proyecto_id_rec,usuario_id):
    """Esta vista debe obtener los datos de los usuarios que han sido asignados a un rol en el proyecto,el parametro
    usuario_id se necesita simplemente para el render para poder retornar a rol-flujo-para-scrum"""
    lista={}
    proyectox=proyecto.objects.get(id=proyecto_id_rec)
    for a in asignacion.objects.all():
        if a.proyecto.id == proyectox.id:#si el proyecto relacionado a una asignacion es el que se esta viendo ahora
            rol_a=rol.objects.get(id=a.rol.id)
            usuario_a=MyUser.objects.get(id=a.usuario.id)
            lista[usuario_a]=rol_a#agregar el usuario de esa asignacion a la vista, y mandarlo al template
    return render(request,'formarEquipo.html',{'roles':rol.objects.all(),'lista_asigna':lista, 'flujos':Flujo.objects.all(),'proyecto':proyectox,'usuario_id':usuario_id})

def delegarHU(request,usuario_id,proyectoid,rolid,hu_id,reasignar):
    """Delega o asigna una HU a un usuario miembro del proyecto, y en caso de ser necesario, reasignar la HU
    a otro usuario evitando duplicaciones en la Base de Datos"""
    proyectox=proyecto.objects.get(id=proyectoid)
    hu=HU.objects.get(id=hu_id)
    if request.method=='POST' :
        if reasignar == '0':
            try:
                delegacionx= delegacion.objects.create(usuario=MyUser.objects.get(id=request.POST['usuario']),hu=hu)
                delegacionx.save()
                return HttpResponseRedirect('/scrum/'+usuario_id+'/'+proyectoid+'/'+rolid+'/')
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/crearFlujo/') #redirijir a rol flujo para scrum despues
        else:
            for d in delegacion.objects.all():
                if d.hu == hu:
                    d.usuario=MyUser.objects.get(id=request.POST['usuario'])
                    d.save()
                    return HttpResponseRedirect('/scrum/'+usuario_id+'/'+proyectoid+'/'+rolid+'/')
    else:
        users=[]
        asignaciones= asignacion.objects.filter(proyecto=proyectox)#obtuve todas las asignaciones para este proyecto
        for a in asignaciones:
            rola = a.rol
            if rola.tiene_permiso('Agregar horas trabajadas'):
                users.append(a.usuario)
        usuario_asignado=[]
        if reasignar == '1':
            for d in delegacion.objects.all():
                if d.hu == hu:
                    usuario_asignado = d.usuario
        
        return render(request,'asignaHU.html',{'usuario_asignado':usuario_asignado, 'proyecto':proyectox,'usuarios':users,'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid})
    
def validarHU(request, usuario_id, proyectoid, rolid, HU_id_rec,is_Scrum):
    hu_x=HU.objects.get(id=HU_id_rec)
    if request.method == 'GET':       
        return render(request,'validarHU.html',{'hu':HU_id_rec, 'HU':hu_x.valido, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid,'is_Scrum':is_Scrum})
    else:
        if hu_x.valido == False:
            hu_x.valido=True
            hu_x.save()
            return HttpResponse('Se ha validado exitosamente') 
        else:
            hu_x.valido=False
            hu_x.save()
            return HttpResponse('Se ha invalidado exitosamente')
  
def visualizarBacklog(request, usuario_id, proyectoid, rolid):
    """
    Vista disponible para el Scrum y el Product Owner.
    Esta vista contiene la lista de HU pendientes pero ACTIVAS y VALIDADAS ordenadas segun su prioridad
    en orden descendente para la correspondiente asignacion que realizara el Scrum Master.
    A medida que las HU se realizan, estas desapareceran del Product Backlog.
    """
    proyectox=proyecto.objects.get(id=proyectoid)
    huss=HU.objects.all().filter(proyecto=proyectox).filter(estado='ACT').filter(valido=True).filter(sprint__hu__isnull=True)
    h=sorted(huss,key=lambda x: x.prioridad, reverse=True)
    return render(request,'visualizarBacklog.html',{'huss':h, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid})

def reactivar(request, usuario_id, proyectoid, rolid, tipo, id_tipo):
    """
    Vista que permite reactivar un flujo, HU o Sprint cancelado por el usuario,
    para su correspondiente uso o modificacion, ya que los objetos cancelados
    solo estan disponibles para su visualizacion, no para su asignacion o modificacion.
    Recibe un tipo en la url que le permite distinguir de que tipo de objeto se trata.
    """
    if tipo == '1': #se trata de un flujo
        f=Flujo.objects.get(id=id_tipo)
        f.estado='ACT'
        f.save()
    if tipo == '2': #se trata de una HU
        h=HU.objects.get(id=id_tipo)
        h.estado='ACT'
        h.save()
    if tipo == '3': #se trata de un sprint
        s=Sprint.objects.get(id=id_tipo)
        s.estado='ACT'
        s.save()
    if tipo == '4': #se trata de un rol
        s=rol.objects.get(id=id_tipo)
        s.estado='ACT'
        s.save()
    return HttpResponseRedirect('/scrum/'+usuario_id+'/'+proyectoid+'/'+rolid+'/')


def adminAdjunto(request,hu_id):
    if request.method=='GET':
        hux=HU.objects.get(id=hu_id)
        adjuntos=[]
        try: 
            adjuntos=archivoadjunto.objects.filter(hU=hux)
        except ObjectDoesNotExist:
            adjuntos = []
        return render(request,'adjuntos.html',{'HU':hux,'adjuntos':adjuntos})
    else:
        archivox = request.FILES['archivo']
        filex=archivoadjunto.objects.create(archivo=archivox,hU_id=hu_id)
        filex.save()
        #archivox.save()
        return HttpResponseRedirect('/adminAdjunto/'+hu_id+'/')
    
def visualizarSprintBacklog(request, usuario_id, proyectoid, rolid):
    """
    El sprint backlog es una lista de las tareas identificadas por el equipo de Scrum
    Los equipos estiman el número de horas para cada tarea que se corresponde a alguien del equipo para completar. 
    """
    lista=[]
    cont=0
    dias=0
    proyectox=proyecto.objects.get(id=proyectoid)
    hux=HU.objects.all().filter(proyecto=proyectox)
    sprint=Sprint.objects.all().filter(proyecto=proyectox)
    s=sorted(sprint,key=lambda x: x.estado, reverse=True)
    for sp in sprint:
        if sp.duracion>cont:
            cont=sp.duracion
            
    while(dias!=cont):
        dias=dias+1
        lista.append(dias)
    return render(request,'visualizarSprintBacklog.html',{'sprint':s, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid, 'HUx':hux, 'dias':lista})



def asignarHU_Usuario_FLujo(request,usuario_id,proyectoid,rolid,sprintid):
    #Lo que muestra esta vista corresponde al dibujo AsignarHUaUsuarioyClasificarenFlujo.java
    #Primero obtener todas las HUs de este proyecto activas y validadadasy que pertenecen al sprint actual
    proyectox=proyecto.objects.get(id=proyectoid)
    sprintx=Sprint.objects.get(id=sprintid)
    hus=HU.objects.filter(proyecto=proyectox,estado='ACT',valido=True).filter(sprint=sprintx)
    hu_en_flujo={}
    for f in Flujo.objects.filter(sprint=Sprint.objects.get(id=sprintid)):
        for a in asignaHU_actividad_flujo.objects.all():
            if f == a.flujo_al_que_pertenece:
                for h in a.lista_de_HU.all():
                    if h.proyecto == proyectox:
                        hu_en_flujo[f]=a.lista_de_HU.all()
                        break
    HU_no_asignada=[]
    HU_asignada={}
    for HUa in hus:
            x=0
            for d in delegacion.objects.all():
                if d.hu == HUa:
                    x=1
                    HU_asignada[HUa]=d.usuario
            if x == 0:
                HU_no_asignada.append(HUa)

    return render(request,"asignarHU_Usuario_Flujo.html",{'hu_en_flujo':hu_en_flujo,'flujos':Flujo.objects.filter(sprint=Sprint.objects.get(id=sprintid)),'HU_no_asignada':HU_no_asignada,'HU_asignada':HU_asignada,'hus':hus,'sprint':sprintx,'proyecto':proyectox,'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid})

def asignarHU_a_FLujo(request,usuario_id,proyectoid,rolid,sprintid,flujo_id):
    sprintx=Sprint.objects.get(id=sprintid)
    proyectox=proyecto.objects.get(id=proyectoid)
    flujo=Flujo.objects.get(id=flujo_id)
    jsonDec = json.decoder.JSONDecoder()
    orden=jsonDec.decode(flujo.orden_actividades)
    hus=HU.objects.filter(proyecto=proyectox,estado='ACT',valido=True).filter(sprint=sprintx)
    for f in Flujo.objects.filter(sprint=Sprint.objects.get(id=sprintid)):
        for a in asignaHU_actividad_flujo.objects.all():
            if a.flujo_al_que_pertenece == f:
                for h in a.lista_de_HU.all():
                    if h.proyecto == proyectox:
                        hus=hus.exclude(id=h.id)
    if request.method == 'POST':
        for a in request.POST.getlist('hu'):
            h=HU.objects.get(id=a)
            h.actividad=Actividades.objects.get(id=orden[0])
            h.save()
            asig=asignaHU_actividad_flujo.objects.filter(flujo_al_que_pertenece=flujo)
            if asig:
                for f in asig:
                    if f.lista_de_HU.filter(proyecto=proyectox):
                        f.lista_de_HU.add(HU.objects.get(id=a))
                        f.save()
            else:
                asignar=asignaHU_actividad_flujo.objects.create(flujo_al_que_pertenece=Flujo.objects.get(id=flujo_id))
                asignar.lista_de_HU.add(HU.objects.get(id=a))
                asignar.save()
        return HttpResponseRedirect('/asignarHUFlujo/'+str(usuario_id)+'/'+str(proyectoid)+'/'+str(rolid)+'/'+str(sprintid))
    else:
        return render(request,"asignarHUFlujo.html",{'flujo':flujo,'hus':hus,'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid,'sprintid':sprintid,'flujo_id':flujo_id})
