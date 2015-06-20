#coding: utf-8
"""Archivo que contiene los metodos que responden a las peticiones de las URL que se filtran por medio de las
expresiones regulares en el archivo urls.py, manipula y gestiona la respuesta que se van a enviar a los clientes.
Cada vista obtiene del request que se le envio la informacion necesaria para el funcionamiento de los metodos,
"""
import os
from django.shortcuts import render, render_to_response
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from gestor.models import MyUser, asignacion, proyecto, rol, Flujo, Actividades, HU, Sprint, delegacion, HU_descripcion, archivoadjunto, asignaHU_actividad_flujo, historial_notificacion, HU_version,\
    adjuntoVersion
from django import forms
from django.core.mail.message import EmailMessage
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.models import Permission
from datetime import datetime, timedelta
import math
import json
from django.utils import timezone
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from supergestor.settings import WORKSPACE
from djutils.decorators import async
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from io import BytesIO
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm

# Create your views and forms here.
@async
def send_email(to, subj, body):
    # this will be executed in a separate thread
    mail = EmailMessage(subj, body, to=[to])
    mail.send()
    
@login_required
def holaView(request):
    """
    Vista que redirige a la pagina principal de administracion tanto a usuarios como a
    superusuarios, los superusuarios son redirigidos a la aplicacion admin mientras que los 
    usuarios obtienen una respuesta con el template hola.html
        :param func: request
        :returns: 'hola.html'
    """
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
                    if p.estado != 'FIN' and p.estado != 'ANU':
                        p.cantidad_dias_transcurridos=int(str((datetime.today().date()-p.fecha_inicio.date()).days))
                        p.save()
                    Sprint_consulta=Sprint.objects.filter(proyecto=p).filter(estado='CON')
                    if Sprint_consulta:
                        for s in Sprint_consulta:
                            if int(s.duracion) <= int(str((datetime.today().date()-s.fecha_inicio.date()).days)):
                                s.estado = 'FIN'
                                s.save()
                    Sprint_activo=Sprint.objects.filter(proyecto=p).filter(estado='ACT')    
                    if Sprint_activo and not Sprint_consulta:
                        for s in Sprint_activo:
                            if s.fecha_inicio.date() <= datetime.today().date():
                                s.estado = 'CON'
                                s.save()
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
        :param func: request
        :param args: usuario_id,proyectoid,rol_id
        :returns: 'rol-flujo-para-scrum.html'
    """
    proyectox=proyecto.objects.get(id=proyectoid)
    usuario=MyUser.objects.get(id=usuario_id)
    rolx=rol.objects.get(id=rol_id)
    enlaces=[]
    HUs=[]
    HUsm=[]
    HUs_add_horas=[]
    HUsm_horas_agotadas=[]
    HUsm_no_desarrolladas=[]
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
    kanban=0
    class enlacex:
        """
        La clase  permite enviar al html solo las url que se corresponden con los permisos contenidos
        en el rol del usuario.
        """
        def __init__(self,urlx,nombrex):
            self.url=urlx
            self.nombre=nombrex
    class usu_hs:
        """Guarda el usuario y las horas acumualadas"""
        def __init__(self,usuario, hs, cont_hu, list_hu):
            self.usuario=usuario
            self.hs=hs
            self.cont_hu=cont_hu
            self.list_hu=list_hu
    
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
        for flujo in flujosm:
            for s in Sprint.objects.all():
                if s.estado == 'CON':
                    for f in s.flujo.all():
                        if f == flujo:
                            flujosm=flujosm.exclude(id=f.id)
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
        for h in HUsm:
            if h.sprint():
                if h.sprint().estado != 'ACT' and h.sprint().estado != 'CAN':
                    HUs=HUs.exclude(id=h.id)
            if h.estado_en_actividad != "FIN" and h.estado_en_actividad !='APR' and h.duracion == h.acumulador_horas and h.acumulador_horas !=0:
                HUsm_horas_agotadas.append(h)
        hus_desarrollandose=[]
        for s in Sprint.objects.all():
            if s.estado == 'CON':
                hus_desarrollandose=s.hu.all()
        for h in HUsm:
            x=0
            for hu in hus_desarrollandose:
                if h == hu:
                    x=1
            if x == 0:
                HUsm_no_desarrolladas.append(h)
        
        enlaceHUm.append(enlacex(usuario_id+'/'+proyectoid+'/'+rol_id,'Modificar'))
        is_Scrum=1
    
    if rolx.tiene_permiso('Can add hu') or rolx.tiene_permiso('Can change hu') or rolx.tiene_permiso('Can change hu nivel Scrum'):
        enlaceHUv.append(enlacex(usuario_id+'/'+proyectoid+'/'+rol_id,'Visualizar'))
        
    agregar_horas=[]
    if rolx.tiene_permiso('Agregar horas trabajadas'):
        for d in delegacion.objects.all():
            if d.hu.proyecto == proyectox and str(d.usuario.id) == usuario_id:
                if d.hu.estado == 'ACT':
                    HUs_add_horas.append(d.hu)
        #HU ordenada por prioridad
        HUs_add_horas=sorted(HUs_add_horas,key=lambda x: x.prioridad, reverse=True)
        enlaceHU_agregar.append(enlacex(usuario_id+'/'+proyectoid+'/'+rol_id,'Agregar horas'))
        i=0
        for p in HUs_add_horas:
            if p.acumulador_horas != p.duracion and p.estado_en_actividad != 'FIN' and p.sprint().fecha_inicio.date() <= datetime.today().date():
                agregar_horas=HUs_add_horas[i]             
                break
            i=i+1
        is_Scrum=2
    HUv=[]
    reporte=0
    if rolx.tiene_permiso('Generar Reporte'):
        HUv=HU.objects.filter(proyecto=proyectox).filter(estado="ACT")
        HUv=sorted(HUv,key=lambda x: x.prioridad, reverse=True)
        reporte=1
        sprintReporte=Sprint.objects.filter(proyecto=proyectox).filter(estado="CON")
        #1-
        equipo_hu={}
        for s in sprintReporte:
            for h in s.hu.all():
                if equipo_hu.has_key(h.saber_usuario()):
                    equipo_hu[h.saber_usuario()].append(h)
                else:
                    equipo_hu[h.saber_usuario()]=[]
                    equipo_hu[h.saber_usuario()].append(h)
        #2-
        estado_hu={}
        for h in HUv:
            if estado_hu.has_key(h.estado_en_actividad):
                estado_hu[h.estado_en_actividad].append(h)
            else:
                estado_hu[h.estado_en_actividad]=[]
                estado_hu[h.estado_en_actividad].append(h)
    else:
        sprintReporte=[]
        equipo_hu={}
        estado_hu={}
                
    if rolx.tiene_permiso('Can add sprint'):
        if len(Sprint.objects.filter(proyecto=proyectox).filter(estado='ACT')) < 1:
            enlaceSprint.append(enlacex('/crearSprint/'+usuario_id+'/'+proyectoid+'/'+rol_id,'Agregar Sprint'))
    else:
        sprints = []#lista vacia si no tiene permiso de ver flujos
    if rolx.tiene_permiso('Can change sprint'):
        """Tiene permiso de modificar flujo, obtengo todos los flujos para enviar al rol-flujo-para-scrum.html"""
        sprintsm=Sprint.objects.filter(proyecto=proyectox)
        for s in sprintsm:
            if s.estado == 'FIN' or s.estado == 'CON':
                sprintsm=sprintsm.exclude(id=s.id)
        sprints=Sprint.objects.filter(proyecto=proyectox)
        enlaceSprintm.append(enlacex(usuario_id+'/'+proyectoid+'/'+rol_id,'Modificar Sprint'))
    else:
        sprintsm = []#lista vacia si no tiene permiso de ver flujos
        
    if rolx.tiene_permiso('Can add sprint') or rolx.tiene_permiso('Can change sprint'):
        enlaceSprintv.append(enlacex(usuario_id+'/'+proyectoid+'/'+rol_id,'Visualizar'))
    existe=0
    if Sprint.objects.filter(proyecto=proyectox).filter(estado='CON'):
        existe=1
    #Chequeo de permiso para visaulizar chart, mando un bolean true si tiene permiso y hay grafico que mostrar, false si no
    if(rolx.tiene_permiso('Visualizar Chart')):
        if Sprint.objects.filter(estado='CON').filter(proyecto=proyectox):
            verburn=True
        else:
            verburn=False
    else:
        verburn=False
    
    finalizar=0
    if proyectox.estado == 'ACT':
        finalizar=1
        for h in HU.objects.filter(proyecto=proyectox).filter(valido=True):
            if h.estado_en_actividad != 'APR':
                finalizar=0
    return render(request,'rol-flujo-para-scrum.html',{'finalizar':finalizar,'fecha_inicio':str(proyectox.fecha_inicio)[:10],'existe':existe,'verburn':verburn,'sprintReporte':sprintReporte,'proyecto':proyectox,'HUsm_no_desarrolladas':HUsm_no_desarrolladas,'HUsm_horas_agotadas':HUsm_horas_agotadas,'roles_inmodificables':roles_inmodificables,'roles_modificables':roles_modificables,'HUv':HUv,'reporte':reporte,'sprints':sprints,'enlaceSprint':enlaceSprint,'sprintsm':sprintsm,'enlaceSprintm':enlaceSprintm,'enlaceSprintv':enlaceSprintv,'enlaceHUa':enlaceHUa,'HUsa':HUsa,'is_Scrum':is_Scrum,'HUs_add_horas':HUs_add_horas, 'enlaceHU_agregar':enlaceHU_agregar,'enlaceHUm':enlaceHUm,'HUsm':HUsm,'enlaceHUv':enlaceHUv,'HUs':HUs,'enlaceHU':enlaceHU,'enlacefv':enlacefv,'enlacefm':enlacefm,'enlacef':enlacef,'enlaces':enlaces,'roles':roles,'flujosm':flujosm, 'flujos':flujos,'proyecto':proyectox,'usuario':usuario,'rolid':rol_id, 'HU_asignada_owner':HU_asignada_owner, 'HU_no_asignada_owner':HU_no_asignada_owner, 'HU_cargar':agregar_horas, 'kanban':kanban,'equipo_hu':equipo_hu,'estado_hu':estado_hu})

    #ahora voy a checkear si el usuario tiene permiso de agregar rol y en base a eso va ver la interfaz de administracion de rol

def registrarUsuarioView(request):
    """
    Vista que se obtiene del regex /registrar solicitado al precionar el boton
    registrar en el login, devuelve un formulario html para crear un nuevo usuario
    con un correo existente
        :param func: request
        :returns: 'crearusuario.html'
    """
    if request.method == 'GET':
        return render(request, 'crearusuario.html')

def guardarUsuarioView(request):
    """
    Vista de guardado de nuevo usuario relacionado con un correo autorizado en la tabla Permitidos
    que se utiliza en la interfaz devuelta por /registrar 
        :param func: request
        :returns: '/login/'
    """
    try:
    
        usuario = MyUser.objects.create_user(username=request.POST['username'], password=request.POST['password1'],email=request.POST['email'])
        usuario.is_admin=False
        usuario.direccion = request.POST['direccion']
        usuario.last_name = request.POST['last_name']
        usuario.user_name = request.POST['user_name']
        usuario.frecuencia_notificaciones=request.POST['notificacion']
        #usuario.save(using=request._db)
        usuario.save()
        #agregar su correo y username en el crontab para que reciba las notificaciones o activar las notificaciones instantaneas
        if usuario.frecuencia_notificaciones == 'dia':
            cmd="sh "+WORKSPACE+"/notificaciones/notificar.sh "+WORKSPACE+" "+request.POST['username']+" "+request.POST['email']+" 1"
            os.system(cmd)
        elif usuario.frecuencia_notificaciones == 'semana':
            cmd="sh "+WORKSPACE+"/notificaciones/notificar.sh "+WORKSPACE+" "+request.POST['username']+" "+request.POST['email']+" 7"
            os.system(cmd)
        elif usuario.frecuencia_notificaciones == 'mes':
            cmd="sh "+WORKSPACE+"/notificaciones/notificar.sh "+WORKSPACE+" "+request.POST['username']+" "+request.POST['email']+" 30"
            os.system(cmd)
        return HttpResponseRedirect('/login/')
    except ObjectDoesNotExist:
        print "Either the entry or blog doesn't exist." 
        return HttpResponse('El correo no se encuentra aprobado. Contactar con el Administrador')
    
def modificarCuenta(request, usuario_id):
    """
    Vista que permite a los usuarios activos modificar sus datos personales como
    el su nombre, apellido y direccion.
    El correo y su nombre identificador del usuario solo lo podra modificar el admin.
        :param func: request
        :param args: usuario_id 
        :returns: 'modificarUsuario.html'
        :rtype: user_name, last_name, direccion
    
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
    
def guardarRolView(request,usuario_id, proyectoid, rolid):
    """
    Vista de guardado de un nuevo rol en la base de datos
    que se utiliza en la interfaz devuelta por /crearRol/ 
        :param func: request
        :param args: usuario_id 
        :returns: 'El rol se ha creado'
        :rtype: nombre_rol_id, descripcion, usuario_creador, estado
    """
    try:
        usuario_e=MyUser.objects.get(id=usuario_id)
        rol_a_crear = rol.objects.create(nombre_rol_id=request.POST['nombre_rol_id'], descripcion=request.POST['descripcion'],usuario_creador=usuario_e, estado='ACT')
        for p in request.POST.getlist('permisos'):
            rol_a_crear.permisos.add(Permission.objects.get(id=p))
        rol_a_crear.save()
        evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"ROL+"+"C+"+"Se ha creado un nuevo rol de nombre: '"+rol_a_crear.nombre_rol_id+"' con una descripcion '"+request.POST['descripcion']+"' con los permisos '"+str([t.codename for t in rol_a_crear.permisos.all()])+"' con fecha y hora: "+str(timezone.now())
        email_e=str(usuario_e.email)
        historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=rol_a_crear.nombre_rol_id,  evento=evento_e)
        if usuario_e.frecuencia_notificaciones == 'instante':
            send_email(str(email_e), 'Notificacion', evento_e)
        #return HttpResponseRedirect('/crearRol/')
        return HttpResponse('El rol se ha creado')
      
    except ObjectDoesNotExist:
        print "Either the entry or blog doesn't exist." 
        return HttpResponseRedirect('/crearRol/')
    
def guardarFlujoView(request, usuario_id, proyectoid, rolid):
    """
    Vista de guardado de un nuevo flujo en la base de datos
    que se utiliza en la interfaz devuelta por /crearFlujo/ 
        :param func: request
        :param args: usuario_id, proyectoid, rolid 
        :returns: 'crearFlujo.html'
        :rtype: nombre, estado
    """
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
        evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"FLUJO+"+"C+"+"Se ha creado un nuevo flujo de nombre: '"+request.POST['nombre']+"' con fecha y hora: "+str(timezone.now())
        usuario_e=MyUser.objects.get(id=usuario_id)
        email_e=str(usuario_e.email)
        historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=flujo_a_crear.nombre, evento=evento_e)
        if usuario_e.frecuencia_notificaciones == 'instante':
            send_email(str(email_e), 'Notificacion', evento_e)
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

    
def guardarHUView(request,usuario_id, proyectoid, rolid):
    """
    Vista de guardado de una nueva HU en la base de datos creada por el Product Owner
    que se utiliza en la interfaz devuelta por /crearHU/
        :param func: request
        :param args: proyectoid 
        :returns: 'La HU se ha creado y relacionado con el proyecto'
        :rtype: descripcion, valor_negocio
    """
    try:
        proyectox = proyecto.objects.get(id=proyectoid)
        HU_a_crear = HU.objects.create(descripcion=request.POST['descripcion'],estado="ACT",valor_negocio=request.POST['valor_negocio'], valor_tecnico=0, prioridad=0, duracion=0, acumulador_horas=0, estado_en_actividad='PEN',proyecto=proyectox,valido=False,version=1.0)
        huv1=HU_version.objects.create(descripcion=HU_a_crear.descripcion,valor_negocio=HU_a_crear.valor_negocio,hu=HU_a_crear,version=HU_a_crear.version)
        HU_a_crear.save()
        huv1.save()
        usuario_e=MyUser.objects.get(id=usuario_id)
        correo_e=usuario_e.email
        evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"HU+"+"C+"+"Se ha creado un nuevo HU de nombre: '"+request.POST['descripcion']+"' con valor de negocio '"+request.POST['valor_negocio']+"' con fecha y hora: "+str(timezone.now())
        historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=HU_a_crear.descripcion, evento=evento_e)
        if usuario_e.frecuencia_notificaciones == 'instante':
            send_email(str(correo_e), 'Notificacion', evento_e)
        return HttpResponse('La HU se ha creado y relacionado con el proyecto')  
    except ObjectDoesNotExist:
        print "Either the entry or blog doesn't exist." 
        return HttpResponseRedirect('/crearHU/')

def guardarSprintFlujos(request,usuario_id,proyectoid,rolid):
    """Tengo que sacar el guardado de flujos del metodo guardarSprintView y ponerlo aqui y desde 
    aqui redirijir hacia asignaHUActividad_Flujo"""
    """en guardarSprintView tengo que redirigir hacia un html donde se muestren los flujos y des ese dirijirme a este metodo"""
    
    
    sprint_id =  request.POST['sprint']
    
    Sprint_a_crear= Sprint.objects.get(id=sprint_id)
    
    for f in request.POST.getlist('Flujos'):
            Sprint_a_crear.flujo.add(Flujo.objects.get(id=f))
    Sprint_a_crear.save()
    
    return HttpResponseRedirect('/asignarHUFlujo/'+usuario_id+'/'+proyectoid+'/'+rolid+'/'+sprint_id)
    
def guardarSprintView(request, usuario_id, proyectoid, rolid):
    """
    Vista de guardado de un nuevo Sprint en la Base de datos
    que se utiliza en la interfaz devuelta por /crearSprint/
        :param func: request
        :param args: usuario_id, proyectoid, rolid 
        :returns: 'El Sprint se ha creado'
        :rtype: descripcion, fecha_inicio, duracion
    
    """
    guardar=0
    for g in request.POST.getlist('_save'):
        if g == 'Guardar':
            guardar=1
    if guardar == 1:
        try:
            HUs=[]
            HUs_pendientes=[]
            Sprint_a_crear = Sprint.objects.create(descripcion=request.POST['descripcion'],estado="ACT",fecha_inicio=request.POST['fecha_inicio'], duracion=request.POST['duracion'], proyecto=proyecto.objects.get(id=proyectoid))
            for p in request.POST.getlist('HUs'):
                h=HU.objects.get(id=p)
                Sprint_a_crear.hu.add(h)
                HUs.append(h)#ahora HUs tienen todas las seleccionadas incluso las pendientes
                Sprint_a_crear.save()
            for f in request.POST.getlist('Flujos'):
                Sprint_a_crear.flujo.add(Flujo.objects.get(id=f))
            for u in request.POST.getlist('usuarios'):
                Sprint_a_crear.equipo.add(MyUser.objects.get(id=u))
            Sprint_a_crear.save()
            evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"SPRINT+"+"C+"+"Se ha creado un nuevo Sprint de nombre: '"+request.POST['descripcion']+"' con una fecha de inicio '"+str(request.POST['fecha_inicio'])+"' ,duracion '"+str(request.POST['duracion'])+ "' en la fecha y hora: "+str(timezone.now())
            usuario_e=MyUser.objects.get(id=usuario_id)
            historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=Sprint_a_crear.descripcion, evento=evento_e)
            if usuario_e.frecuencia_notificaciones == 'instante':
                send_email(str(usuario_e.email), 'Notificacion', evento_e)

            flujos=Flujo.objects.all()
            flujos_pen=[]

            for h in HUs:#por cada hu seleccionada
                if h.estado_en_actividad!='APR':
                    if h not in HUs_pendientes:
                        HUs_pendientes.append(h)
                    HUs.remove(h)#HUs es una lista porque se definio asi pero flujos se obtuvo con un query
                    if h.flujo() not in flujos_pen:
                        flujos_pen.append(h.flujo())
                    if h.flujo() in flujos:   
                        flujos=flujos.exclude(id=h.flujo().id)
            #asi HU tiene todas las HU no pendientes 
            #y HU_pendientes tiene las HU pendientes
            HUs_pendientes=set(HUs_pendientes)
                            
            return render(request,"eleccionFlujo.html",{'sprint':Sprint_a_crear,'HUs_pendientes':HUs_pendientes,'HUs':HUs,'flujo_pen':flujos_pen,'flujos':flujos,'usuarioid':usuario_id,'proyectoid':proyectoid,'rolid':rolid})
        except ObjectDoesNotExist:
            print "Either the entry or blog doesn't exist." 
            return HttpResponseRedirect('/crearSprint/')
    else:
        if request.POST['boton'] == 'Calcular':
            proyectox = proyecto.objects.get(id=proyectoid)
            HUs = HU.objects.filter(proyecto=proyectox).filter(valido=True)
            flujos=Flujo.objects.all()#le mando todos los flujos para que elija los que quiere
            HUs_pendientes=[]
            for x in Sprint.objects.filter(proyecto=proyectox):
                if x.estado != 'FIN':
                    for h in x.hu.all():
                        HUs=HUs.exclude(id=h.id)
                elif x.estado != 'CON':
                    for h in x.hu.all():
                        if h.estado_en_actividad == 'FIN' or h.estado_en_actividad == 'APR':
                            HUs=HUs.exclude(id=h.id)
                        else:
                            HUs_pendientes.append(h)
                            HUs=HUs.exclude(id=h.id)
            sum=0
            hus_seleccionadas=[]
            HUs_no_seleccionadas=HUs
            HUs_pendientes_no_seleccionadas=HUs_pendientes
            HUs_pendientes=[]
            flujos_pen=[]
            for h in request.POST.getlist('HUs'):
                x=0
                for hp in HUs_pendientes_no_seleccionadas:
                    if hp == HU.objects.get(id=h):
                        x=1
                if x == 1:
                    HUs_pendientes_no_seleccionadas.remove(HU.objects.get(id=h))
                    HUs_pendientes.append(HU.objects.get(id=h))
                    flujos_pen.append((HU.objects.get(id=h)).flujo())
                else:
                    hus_seleccionadas.append(HU.objects.get(id=h))
                    HUs_no_seleccionadas=HUs_no_seleccionadas.exclude(id=h)
                sum=sum+HU.objects.get(id=h).duracion
            flujos_pen=set(flujos_pen)
            for f in flujos_pen:
                for flu in flujos:
                    if flu == f:
                        flujos=flujos.exclude(id=f.id)
                
            equipo_seleccionado=[]
            equipo_no_seleccionado=[]
            asignaciones= asignacion.objects.filter(proyecto=proyectox)#obtuve todas las asignaciones para este proyecto
            for a in asignaciones:
                rola = a.rol
                if rola.tiene_permiso('Agregar horas trabajadas'):
                    equipo_no_seleccionado.append(a.usuario)
            horas=0
            for u in request.POST.getlist('usuarios'):
                horas=horas+8
                equipo_seleccionado.append(MyUser.objects.get(id=u))
                equipo_no_seleccionado.remove(MyUser.objects.get(id=u))
            
            fecha_fin=datetime.strptime(request.POST['fecha_inicio'],"%Y-%m-%d").date() + timedelta(days=math.ceil(sum/horas))
            
        return render(request, 'crearSprint.html',{'fecha_fin':fecha_fin,'equipo_pen':equipo_seleccionado,'equipo':equipo_no_seleccionado,'flujos_pen':flujos_pen,'HUs_pendientes_no_seleccionadas':HUs_pendientes_no_seleccionadas,'HUs_pendientes':HUs_pendientes,'nombre':request.POST['descripcion'],'duracion':math.ceil(sum/horas),'flujos':flujos,'HUs':HUs,'HUs_seleccionadas':hus_seleccionadas,'HUs_no_seleccionadas':HUs_no_seleccionadas,'fecha_ahora':request.POST['fecha_inicio'],'usuarioid':usuario_id,'proyectoid':proyectoid,'rolid':rolid})
      

def elegirVersionHU(request,hv_id,hu_id):
    """
    Esta vista responde al boton elegir al elegir una version anterior de hu, ya que si vuelvo a hacer un simple modificar
    pordria volver a crear una version que ya existe, por lo tanto esta vista modifica con datos preexistenes sin
    crear una nueva version
    Primero obtengo la huversion saco los datos los meto en la hu que tambien tengo que obtener y le doy hu.save()
        :param func: request
        :param args: hv_id, hu_id 
        :returns: 'Se ha cambiado de version correctamente'
    """
    huv=HU_version.objects.get(id=hv_id)
    hu=HU.objects.get(id=hu_id)
    
    hu.descripcion=huv.descripcion
    hu.valor_negocio=huv.valor_negocio
    hu.version=huv.version
    hu.save()
    return HttpResponse('Se ha cambiado de version correctamente')
       
def guardarHUProdOwnerView(request,usuario_id, proyectoid, rolid, HU_id_rec,is_Scrum):
    """
    Vista de guardado de la modificacion de una HU existente modificada por el Product Owner
    que se utiliza en la interfaz devuelta por /modificarHU/ 
    0 corresponde a la modificaci[on realizada por el Product Owner
        :param func: request
        :param args: usuario_id, proyectoid, rolid, HU_id_rec,is_Scrum 
        :returns: 'La descripcion y valor de negocio de la HU a sido modificado exitosamente'
        :rtype: descripcion, valor_negocio, estado 
    1 coresponde a la modificaci[on realizada por el Scrum
        :param func: request
        :param args: usuario_id, proyectoid, rolid, HU_id_rec,is_Scrum 
    2 corresponde a la modificaci[on realizada por el Equipo
        :param func: request
        :param args: usuario_id, proyectoid, rolid, HU_id_rec,is_Scrum 
        :returns: 'modificarHU.html'
        :rtype: agregar_horas, descripcion_horas    
    """
          
    h=HU.objects.get(id=HU_id_rec)
    if request.method == 'POST':
        if is_Scrum == '0':
            hvs=HU_version.objects.filter(hu__id=HU_id_rec)
            lastx=len(hvs.all())
            if lastx>0:
                x=hvs.last().version
            else:
                x=1.0
            
            
            if(not h.descripcion==request.POST['descripcion'] and not h.valor_negocio==request.POST['valor_negocio']):
                x=math.floor(x)
                x+=1.0
            else:
                x+=0.1
            
            valor_negocio=request.POST['valor_negocio']
            descripcion=request.POST['descripcion']
            estado=request.POST['estado']
            h.valor_negocio=valor_negocio
            h.descripcion=descripcion
            h.estado=estado
            h.version=x
            h.save() #Guardamos el modelo de manera Editada
                        
            
            """aca tengo que crear una HU version con los datos anteriores (esta es la parte que se hace para el owner)  """
            hv=HU_version.objects.create(descripcion=h.descripcion,valor_negocio=h.valor_negocio,hu=h,version=x)
            hv.save()
            """esto guarda una version nomas pero no el valor flotante correcto de la version"""
            """para cargar el valor version primero tengo que saber si es una version o una subversion"""
            """        para saber esto necesito ver los campos cargados ahora con los de la hu actual y ver cuantos cambiaron"""
            """luego tengo que saber cual fue la ultima version o subversion cargada y aumentarle 1 o 0,1"""
            """        para saber esto tengo que obtener la ultima hu_version creada de esta hu, si no hay se empieza con 1"""
            

            evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"HU+"+"M+"+"Se ha modificado '"+request.POST['descripcion']+"' con valor de negocio '"+request.POST['valor_negocio']+"' y estado '"+request.POST['estado']+" con fecha y hora: "+str(timezone.now())
            usuario_e=MyUser.objects.get(id=usuario_id)
            historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=h.descripcion, evento=evento_e)
            if usuario_e.frecuencia_notificaciones == 'instante':
                send_email(str(usuario_e.email), 'Notificacion', evento_e)
            
            return HttpResponse('La descripcion y valor de negocio de la HU a sido modificado exitosamente')
        else:
            acumulador=0
            prueba=request.POST['horas_agregar']
            acumulador=acumulador + float(prueba)
            y=str(timezone.now())
            for horas in h.hu_descripcion.all():
                x=str(horas.fecha)
                if x[:10] == y[:10]:
                    acumulador=horas.horas_trabajadas + acumulador
            if acumulador<9:
                s=h.sprint()
                if s is not None and s.termino_Sprint():
                    s.estado='FIN'
                guardar=0
                for g in request.POST.getlist('_save'):
                    if g == 'Guardar':
                        guardar=1
                if guardar == 1:
                    try:
                        proyectox=proyecto.objects.get(id=h.proyecto.id)
                        horas_a_agregar = request.POST['horas_agregar']
                        descripcion_horas=request.POST['descripcion_horas']
                        acumulador_horas = float(horas_a_agregar)+h.acumulador_horas
                        if h.duracion >= acumulador_horas:
                            h.acumulador_horas=acumulador_horas
                            h.estado_en_actividad='PRO'
                            h.save()
                            if proyectox.estado == 'PEN' and acumulador_horas > 0:
                                proyectox.estado='ACT'
                                proyectox.save()
                            if s is not None:
                                if s.estado == 'ACT' and acumulador_horas >0:
                                    s.estado='CON'
                                    s.save()
                            evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"HU+"+"A+"+"Se ha agregado '"+str(request.POST['horas_agregar'])+"' horas a la '"+str(h.descripcion)+"' con una descripcion '"+request.POST['descripcion_horas']+"' estando en la actividad '"+ str(h.actividad)+ "' con el estado '"+str(h.estado_en_actividad)+"' con fecha y hora: "+str(timezone.now())
                            usuario_e=MyUser.objects.get(id=usuario_id)
                            historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=h.descripcion, evento=evento_e)
                            if usuario_e.frecuencia_notificaciones == 'instante':
                                send_email(str(usuario_e.email), 'Notificacion', evento_e)                       
                            hd=HU_descripcion.objects.create(horas_trabajadas=horas_a_agregar,descripcion_horas_trabajadas=descripcion_horas,fecha=datetime.now(), actividad=str(h.actividad), estado=str(h.estado_en_actividad))
                            h.hu_descripcion.add(HU_descripcion.objects.get(id=hd.id))
                            hd.save()
                            return render(request,'modificarHU.html', {'HU':h, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid,'is_Scrum':2})
                        else:
                            return HttpResponse('Contactar con el Scrum para aumentar la duracion de la HU, ya que ha sobrepasado el tiempo de realizacion de HU')
                    except ObjectDoesNotExist:
                        print "Either the entry or blog doesn't exist." 
                        return HttpResponseRedirect('/crearHU/')
                else:
                    if request.POST['boton'] == 'Finalizar':
                        for a in asignaHU_actividad_flujo.objects.all():
                            for hu in a.lista_de_HU.all():
                                if hu==h:
                                    flujo=a.flujo_al_que_pertenece
                                    break
                        jsonDec = json.decoder.JSONDecoder()
                        orden=jsonDec.decode(flujo.orden_actividades)
                         
                        proyectox=proyecto.objects.get(id=h.proyecto.id)
                        horas_a_agregar = request.POST['horas_agregar']
                        descripcion_horas=request.POST['descripcion_horas']
                        fecha=timezone.now()

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
                            hd=HU_descripcion.objects.create(horas_trabajadas=horas_a_agregar,descripcion_horas_trabajadas=descripcion_horas, fecha=fecha, actividad=str(h.actividad), estado=str(h.estado_en_actividad))
                            h.hu_descripcion.add(HU_descripcion.objects.get(id=hd.id))
                            hd.save()
                            evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"HU+"+"A+"+"Se ha agregado '"+request.POST['horas_agregar']+"' horas a la '"+HU.descripcion+"' con una descripcion '"+request.POST['descripcion_horas']+"' quedando asi finalizadas las actividades con fecha y hora: "+str(timezone.now())
                            usuario_e=MyUser.objects.get(id=usuario_id)
                            historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=h.descripcion, evento=evento_e)
                            if usuario_e.frecuencia_notificaciones == 'instante':
                                send_email(str(usuario_e.email), 'Notificacion', evento_e)                        
                            return HttpResponse("Todas las actividades de HU finalizadas")
                        elif x < len(orden) and h.acumulador_horas == h.duracion:
                            h.estado_en_actividad='PEN'
                            h.save()
                            estadoP='PRO'
                            hd=HU_descripcion.objects.create(horas_trabajadas=horas_a_agregar,descripcion_horas_trabajadas=descripcion_horas, fecha=fecha, actividad=str(h.actividad), estado=estadoP)
                            h.hu_descripcion.add(HU_descripcion.objects.get(id=hd.id))
                            hd.save()
                            evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"HU+"+"A+"+"Se ha agregado '"+request.POST['horas_agregar']+"' horas a la '"+HU.descripcion+"' con una descripcion '"+request.POST['descripcion_horas']+"' ,completando la duracion sin terminar todas las actividades con fecha y hora: "+str(timezone.now())
                            usuario_e=MyUser.objects.get(id=usuario_id)
                            historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=h.descripcion, evento=evento_e)
                            if usuario_e.frecuencia_notificaciones == 'instante':
                                send_email(str(usuario_e.email), 'Notificacion', evento_e)
                            return HttpResponse("Duracion de HU finalizada sin terminar todas las actividades. Contactar con el Scrum")
                        else:
                            h.actividad=Actividades.objects.get(id=orden[x])
                            h.estado_en_actividad='PEN'
                            h.save()
                            estadoP='PRO'
                            hd=HU_descripcion.objects.create(horas_trabajadas=horas_a_agregar,descripcion_horas_trabajadas=descripcion_horas, fecha=fecha, actividad=str(h.actividad), estado=estadoP)
                            h.hu_descripcion.add(HU_descripcion.objects.get(id=hd.id))
                            hd.save()
                            evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"HU+"+"A+"+"Se ha agregado '"+str(request.POST['horas_agregar'])+"' horas a la '"+str(h.descripcion)+"' con una descripcion '"+str(request.POST['descripcion_horas'])+"' estando en la actividad '"+ str(h.actividad)+ "' con el estado '"+str(h.estado_en_actividad)+"' con fecha y hora: "+str(timezone.now())
                            usuario_e=MyUser.objects.get(id=usuario_id)
                            historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=h.descripcion, evento=evento_e)
                            if usuario_e.frecuencia_notificaciones == 'instante':
                                send_email(str(usuario_e.email), 'Notificacion', evento_e)
                            return render(request,'modificarHU.html', {'HU':h, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid,'is_Scrum':2})
            else:
                return HttpResponse('Las Horas cargadas ya superan las 8 Horas diarias que deben cargarse por dia. Ya ha cargado '+str(acumulador-int(prueba))+' horas en este dia') 
                
class FormularioContacto(forms.Form):
    """
    Clase utilizada para obtener el formulario de peticion de seteo de contrasenha.
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
        :param func: request 
        :returns: '/login/'
        :rtype: usuario, correo    
    """
    if request.method == 'POST':
        formulario = FormularioContacto(request.POST)
        if formulario.is_valid():
            asunto = 'RECUPERACION DE CONTRASENA'
            username_cargado = formulario.cleaned_data['usuario']
            usuario = MyUser.objects.get(username = username_cargado)
            if (str(usuario.email) == formulario.cleaned_data['correo']):
                mensaje = 'Puedes dirigirte a esta URL de seteo de tu password:  djangoserver/seteoPassword/' + str(usuario.id) + '/'
                send_email(request.POST['correo'], asunto, mensaje)
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
        :param func: request
        :param args: usuario_id
        :returns: 'seteoPassword.html'
        :rtype: password_nueva1, password_nueva2
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
    en el Rol que se quiere visualizar
        :param func: request
        :param args: usuario_id,proyectoid, rolid, rol_id_rec
        :returns: 'visualizarRol.html'
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
        :param func: request
        :param args: usuario_id, proyectoid, rolid, rol_id_rec
        :returns: modificarRol.html
        :rtype: nombre_rol_id, descripcion, permisos, estado
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
            evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"ROL+"+"M+"+"El rol '"+f.descripcion+"' con descripcion '"+form.cleaned_data['descripcion']+"' con los permisos '"+str([t.codename for t in f.permisos.all()])+"' en el estado '"+form.cleaned_data['estado']+"' ha sido modificado exitosamente en la fecha y hora: "+str(timezone.now())
            usuario_e=MyUser.objects.get(id=usuario_id)
            historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=f.nombre_rol_id, evento=evento_e)
            if usuario_e.frecuencia_notificaciones == 'instante':
                send_email(str(usuario_e.email), 'Notificacion', evento_e)
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
        permisos=permisos.exclude(name='Can add queue message').exclude(name='Can change queue message').exclude(name='Can delete queue message')
        permisos=permisos.exclude(name='Can add adjunto version').exclude(name='Can change adjunto version').exclude(name='Can delete adjunto version')
        permisos=permisos.exclude(name='Can add h u_descripcion').exclude(name='Can change h u_descripcion').exclude(name='Can delete h u_descripcion')
        permisos=permisos.exclude(name='Can add h u_version').exclude(name='Can change h u_version').exclude(name='Can delete h u_version')
        permisos=permisos.exclude(name='Can add historial_notificacion').exclude(name='Can change historial_notificacion').exclude(name='Can delete historial_notificacion')
        permisos=permisos.exclude(name='Can add session').exclude(name='Can change session').exclude(name='Can delete session')
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
        :param func: request
        :param args: usuario_id, proyectoid, rolid, flujo_id_rec 
        :returns: visualizarFlujo.html
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
        :param func: request
        :param args: usuario_id, proyectoid, rolid, flujo_id_rec
        :returns: modificarFlujo.html
        :rtype: nombre, estado
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
                evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"FLUJO+"+"C+"+"El flujo '"+request.POST['nombre']+"' con estado '"+request.POST['estado']+"' ha sido creado exitosamente en la fecha y hora: "+str(timezone.now())
                usuario_e=MyUser.objects.get(id=usuario_id)
                historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=flujo_a_crear.nombre,evento=evento_e)
                if usuario_e.frecuencia_notificaciones == 'instante':
                    send_email(str(usuario_e.email), 'Notificacion', evento_e)
                return HttpResponse('El flujo nuevo se ha creado')  
            except ObjectDoesNotExist:
                print "No se ha podido crear el nuevo flujo"
            evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"FLUJO+"+"C+"+"El flujo '"+request.POST['nombre']+"' ha sido creado exitosamente en la fecha y hora: "+str(timezone.now())
            usuario_e=MyUser.objects.get(id=usuario_id)
            historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=flujo_a_crear.nombre,evento=evento_e)
            if usuario_e.frecuencia_notificaciones == 'instante':
                send_email(str(usuario_e.email), 'Notificacion', evento_e)
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
            evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"FLUJO+"+"M+"+"El flujo '"+request.POST['nombre']+"' con estado '"+request.POST['estado']+"' ha sido modificado exitosamente en la fecha y hora: "+str(timezone.now())
            usuario_e=MyUser.objects.get(id=usuario_id)
            historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=f.nombre, evento=evento_e)
            if usuario_e.frecuencia_notificaciones == 'instante':
                send_email(str(usuario_e.email), 'Notificacion', evento_e)
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
        fields=['descripcion','fecha_inicio','duracion','estado','hu','flujo','equipo']
        
def visualizarSprintProyectoView(request,usuario_id, proyectoid, rolid, Sprint_id_rec):
    """
    Vista que utiliza el formulario SprintProyecto para desplegar los datos almacenados
    en el Sprint que se quiere visualizar.
        :param func: request
        :param args: usuario_id, proyectoid, rolid, Sprint_id_rec
        :returns: visualizarSprint.html
    
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
        :param func: request
        :param args: usuario_id, proyectoid, rolid, Sprint_id_rec
        :returns: 'modificarSprint.html'
        :rtype: descripcion, estado, fecha_inicio, duracion, hu, flujo

    """
    estados=['ACT','CAN']
    proyectox=proyecto.objects.get(id=proyectoid)
    s=Sprint.objects.get(id=Sprint_id_rec)
    if request.method == 'POST':
        guardar=0
        for g in request.POST.getlist('Submit'):
            if g == 'Guardar':
                guardar=1
        if guardar == 1:
            descripcion=request.POST['descripcion']
            estado=request.POST['estado']
            fecha_inicio=request.POST['fecha_inicio']
            duracion=request.POST['duracion']
            hu=request.POST.getlist('hu')
            flujo=request.POST.getlist('flujo')
            usuarios=request.POST.getlist('equipo')
            s.descripcion=descripcion
            s.estado=estado
            s.fecha_inicio=fecha_inicio
            s.duracion=duracion
            for h in hu:
                s.hu.add(HU.objects.get(id=h))
            for h in flujo:
                s.flujo.add(Flujo.objects.get(id=h))
            for h in usuarios:
                s.equipo.add(MyUser.objects.get(id=h))
            s.save() #Guardamos el modelo de manera Editada
            evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"SPRINT+"+"M+"+"El Sprint '"+descripcion+"' con estado '"+estado+"' con una fecha de inicio '"+str(fecha_inicio)+"' ,duracion '"+duracion+"' ,hu '"+str([t.descripcion for t in s.hu.all()])+"' y flujo '"+str([t.nombre for t in s.flujo.all()])+"' ha sido modificado exitosamente en la fecha y hora: "+str(timezone.now())
            usuario_e=MyUser.objects.get(id=usuario_id)
            historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=s.descripcion,evento=evento_e)
            if usuario_e.frecuencia_notificaciones == 'instante':
                send_email(str(usuario_e.email), 'Notificacion', evento_e)
            return HttpResponse('El Sprint ha sido modificado exitosamente')

        else:
            if request.POST['boton'] == 'Calcular':
                sum=0
                for h in s.hu.all():
                    sum=sum+h.duracion
                hus_seleccionadas=[]
                HUs_no_seleccionadas=[]
                for h in HU.objects.filter(estado="ACT").filter(proyecto=proyectox).filter(valido=True):
                    if h not in s.hu.all():
                        if not h.sprint():
                            HUs_no_seleccionadas.append(h)
                        else:
                            if h.sprint().estado == 'FIN' and h.estado_en_actividad != 'APR':
                                HUs_no_seleccionadas.append(h)
                    
                flujos_seleccionados=[]
                flujos_no_seleccionados=[]
                for f in Flujo.objects.all():
                    if f not in s.flujo.all():
                        flujos_no_seleccionados.append(f)
                        
                for h in request.POST.getlist('hu'):
                    hus_seleccionadas.append(HU.objects.get(id=h))
                    sum=sum+HU.objects.get(id=h).duracion
                    if HU.objects.get(id=h) in HUs_no_seleccionadas:
                        HUs_no_seleccionadas.remove(HU.objects.get(id=h))
                
                for f in request.POST.getlist('flujo'):
                    flujos_seleccionados.append(Flujo.objects.get(id=f))
                    if Flujo.objects.get(id=f) in flujos_no_seleccionados:
                        flujos_no_seleccionados.remove(Flujo.objects.get(id=f))
                
                equipo_seleccionado=[]
                equipo_no_seleccionado=[]
                horas=len(s.equipo.all())*8
                asignaciones= asignacion.objects.filter(proyecto=proyectox)#obtuve todas las asignaciones para este proyecto
                for a in asignaciones:
                    rola = a.rol
                    if rola.tiene_permiso('Agregar horas trabajadas'):
                        equipo_no_seleccionado.append(a.usuario)
                for e in s.equipo.all():
                    if e in equipo_no_seleccionado:
                        equipo_no_seleccionado.remove(e)
                        
                for u in request.POST.getlist('equipo'):
                    horas=horas+8
                    equipo_seleccionado.append(MyUser.objects.get(id=u))
                    equipo_no_seleccionado.remove(MyUser.objects.get(id=u))
                fecha = str(s.fecha_inicio)
                ctx = {'estimacion':math.ceil(sum/horas),'equipo':equipo_no_seleccionado,'equipo_sel':equipo_seleccionado,'flujos':flujos_no_seleccionados,'flujos_sel':flujos_seleccionados,'estados':estados, 'fecha':fecha[0:10],'lista_HU_sin_asignar':HUs_no_seleccionadas,'HUs_sel':hus_seleccionadas,'Sprint':s, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid}
                return render_to_response('modificarSprint.html', ctx ,context_instance=RequestContext(request))

    else:    
        
        proyectox=proyecto.objects.get(id=proyectoid)
        HUs = HU.objects.filter(proyecto=proyectox).filter(valido=True)
        flujos=Flujo.objects.all()
        users=[]
        asignaciones= asignacion.objects.filter(proyecto=proyectox)#obtuve todas las asignaciones para este proyecto
        for a in asignaciones:
            rola = a.rol
            if rola.tiene_permiso('Agregar horas trabajadas'):
                users.append(a.usuario)
        HUs_pendientes=[]
        for x in Sprint.objects.filter(proyecto=proyectox):
            if x.estado != 'FIN':
                for h in x.hu.all():
                    HUs=HUs.exclude(id=h.id)
            else:
                for h in x.hu.all():
                    if h.estado_en_actividad != 'APR' and h.sprint() == x:
                        HUs_pendientes.append(h)
                        HUs=HUs.exclude(id=h.id)
                    else:
                        HUs=HUs.exclude(id=h.id)
                
        lista_restante=[]
        for permitido in HUs:
            x=0
            for perm_hu in s.hu.all():
                if permitido.id==perm_hu.id:
                    x=1
            if x==0:
                lista_restante.append(permitido)
        for h in s.hu.all():
            for hp in HUs_pendientes:
                if h == hp:
                    HUs_pendientes.remove(h)
                    
        fecha = str(s.fecha_inicio)
        
        ctx = {'estimacion':s.duracion,'equipo':users,'HUs_pendientes':HUs_pendientes,'flujos':flujos,'estados':estados, 'fecha':fecha[0:10],'HUs':HUs,'lista_HU_sin_asignar':lista_restante,'Sprint':s, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid}
        return render_to_response('modificarSprint.html', ctx ,context_instance=RequestContext(request))
    
class FormularioHU(forms.ModelForm):
    """
    Clase que obtiene el formulario para la creacion, visualizacion y modificacion
    de HU's del proyecto desde la vista del Scrum y del Product Owner.
    """
    class Meta:
        model= HU
        fields=['valor_tecnico','prioridad','duracion']
        
def visualizarHUView(request,usuario_id, proyectoid, rolid, HU_id_rec,is_Scrum, kanban):
    """
    Vista que utiliza el formulario HU para desplegar los datos almacenados
    en la HU que se quiere visualizar.
        :param func: request
        :param args: usuario_id, proyectoid, rolid, HU_id_rec,is_Scrum, kanban
        :returns: 'visualizarHU.html'
    """
    HU_disponible= HU.objects.get(id=HU_id_rec)
    usuario_asignado = HU_disponible.saber_usuario() 
    flujo_al_que_pertenece=HU_disponible.flujo()
    sprint_al_que_pertenece=HU_disponible.sprint()
    adjuntos=archivoadjunto.objects.filter(hU=HU_disponible)
    formulario =  FormularioHU(initial={
                                                     'descripcion': HU_disponible.descripcion,
                                                     'valor_negocio': HU_disponible.valor_negocio,
                                                     })      
    return render_to_response('visualizarHU.html',{'formulario':formulario,'version':HU_disponible.version,'usuario_asignado':usuario_asignado,'HU':HU_disponible, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid,'adjuntos':adjuntos,'is_Scrum':is_Scrum, 'sprint':sprint_al_que_pertenece, 'flujo':flujo_al_que_pertenece, 'kanban':kanban},
                                  context_instance=RequestContext(request))

def modificarHU(request, usuario_id, proyectoid, rolid, HU_id_rec,is_Scrum):
    """
    Vista que utiliza el formulario HU para desplegar los datos editables
    de la HU en tres niveles de modificacion.
    Esta vista corresponde a la modificacion del nivel 1, es decir, a nivell Scrum Master
        :param func: request
        :param args: usuario_id, proyectoid, rolid, HU_id_rec,is_Scrum
        :returns: modificarHU.html
        :rtype: valor_tecnico, prioridad, duracion
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
                evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"HU+"+"M+"+"La HU '"+str(h.descripcion)+"' valor de negocio  '"+str(form.cleaned_data['valor_tecnico'])+"'  prioridad '"+str(form.cleaned_data['prioridad'])+"' y duracion  '"+str(form.cleaned_data['duracion'])+"' ha sido modificado exitosamente en la fecha y hora: "+str(timezone.now())
                usuario_e=MyUser.objects.get(id=usuario_id)
                historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=h.descripcion,evento=evento_e)
                if usuario_e.frecuencia_notificaciones == 'instante':
                    send_email(str(usuario_e.email), 'Notificacion', evento_e)

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
            ctx = {'version':h.version,'valores':VALORES10_CHOICES,'form':form, 'HU':h, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid,'is_Scrum':is_Scrum}
            return render_to_response('modificarHU.html', ctx ,context_instance=RequestContext(request))
    else:
        return render(request,'modificarHU.html', {'version':h.version,'estados':estados, 'valores':VALORES10_CHOICES,'HU':h, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid,'is_Scrum':is_Scrum})

def crearRol(request,usuario_id,proyectoid,rolid):
    """
    Vista que realiza la creacion de roles de proyecto desde la vista del Scrum, excluyendo aquellos permisos que no corresponde
    ser vistos por el usuario Scrum.
        :param func: request
        :param args: usuario_id,proyectoid,rolid
        :returns: crearRol.html
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
        permisos=permisos.exclude(name='Can add queue message').exclude(name='Can change queue message').exclude(name='Can delete queue message')
        permisos=permisos.exclude(name='Can add adjunto version').exclude(name='Can change adjunto version').exclude(name='Can delete adjunto version')
        permisos=permisos.exclude(name='Can add h u_descripcion').exclude(name='Can change h u_descripcion').exclude(name='Can delete h u_descripcion')
        permisos=permisos.exclude(name='Can add h u_version').exclude(name='Can change h u_version').exclude(name='Can delete h u_version')
        permisos=permisos.exclude(name='Can add historial_notificacion').exclude(name='Can change historial_notificacion').exclude(name='Can delete historial_notificacion')
        permisos=permisos.exclude(name='Can add session').exclude(name='Can change session').exclude(name='Can delete session')
        return render(request, 'crearRol.html',{'permissions':permisos,'usuarioid':usuario_id,'proyectoid':proyectoid,'rolid':rolid})
    
def crearFlujo(request,usuario_id,proyectoid,rolid):
    """
    Vista que realiza la creacion de flujos de proyecto desde la vista del Scrum.
        :param func: request
        :param args: usuario_id,proyectoid,rolid
        :returns: crearFlujo.html
    """
    actividades_asignadas=[]
    actividades_disponibles=Actividades.objects.all()
    if request.method == 'GET':
        return render(request, 'crearFlujo.html',{'actividades_asignadas':actividades_asignadas,'actividades':actividades_disponibles,'usuarioid':usuario_id,'proyectoid':proyectoid,'rolid':rolid})
        
def crearSprint(request,usuario_id,proyectoid,rolid):
    """
    Vista que realiza la creacion de flujos de proyecto desde la vista del Scrum.
        :param func: request
        :param args: usuario_id,proyectoid,rolid
        :returns: crearSprint.html
    """
    proyectox = proyecto.objects.get(id=proyectoid)
    HUs = HU.objects.filter(proyecto=proyectox).filter(valido=True)
    flujos=Flujo.objects.all()#le mando todos los flujos para que elija los que quiere
    flujos_pen=[]
    HUs_pendientes=[]
    for x in Sprint.objects.filter(proyecto=proyectox):#se podria chequear solo los sprint del proyecto para hacer menos trabajo!
        if x.estado == 'FIN':
            for h in x.hu.all():
                if h.estado_en_actividad != 'APR':
                    HUs_pendientes.append(h)
                    HUs=HUs.exclude(id=h.id)
                    flujos_pen.append(h.flujo())
                else:
                    HUs=HUs.exclude(id=h.id)
    for x in Sprint.objects.filter(proyecto=proyectox):#este super for es para analizae el contenido de los sprint que no hayan terminado 
        if x.estado != 'FIN' and x.estado != 'CAN':#se busca sacar los hu que se pueden continuar todavia que esteen entre los pendientes
            for h in x.hu.all():
                HUs=HUs.exclude(id=h.id)
                for hp in HUs_pendientes:
                    if h == hp:
                        HUs_pendientes.remove(h)  
                for f in flujos_pen:#tambien se busca sacar los flujos que pueden continuar todavia que esteen en entre pendientes de hus pen.
                    if f == h.flujo():
                        flujos_pen.remove(h.flujo())
    flujos_pen=set(flujos_pen)
    for f in flujos_pen:
        for flu in flujos:
            if flu == f:
                flujos=flujos.exclude(id=f.id)
    HUs=sorted(HUs,key=lambda x: x.prioridad, reverse=True)
    users=[]
    asignaciones= asignacion.objects.filter(proyecto=proyectox)#obtuve todas las asignaciones para este proyecto
    for a in asignaciones:
        rola = a.rol
        if rola.tiene_permiso('Agregar horas trabajadas'):
            users.append(a.usuario)
    users_pen=[]
    for h in HUs_pendientes:
        users_pen.append(h.saber_usuario())
    users_pen=set(users_pen)
    for u in users_pen:
        for up in users:
            if u == up:
                users.remove(u)
    fecha_inicio_sugerida=str(datetime.now())[0:10]
    for s in Sprint.objects.filter(proyecto=proyectox).filter(estado='CON'):
        fecha_inicio_sugerida=str(s.fecha_inicio.date() + timedelta(days=math.ceil(s.duracion)))[0:10]
    if request.method == 'GET':
        return render(request, 'crearSprint.html',{'equipo_pen':users_pen,'equipo':users,'flujos_pen':flujos_pen,'HUs_pendientes':HUs_pendientes,'HUs_no_seleccionadas':HUs,'flujos':flujos,'HUs':HUs,'fecha_ahora':fecha_inicio_sugerida,'usuarioid':usuario_id,'proyectoid':proyectoid,'rolid':rolid})

def crearHU(request,usuario_id,proyectoid,rolid):
    """
    Vista que realiza la creacion de flujos de proyecto desde la vista del Scrum.
        :param func: request
        :param args: usuario_id,proyectoid,rolid
        :returns: crearHU.html
    
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
        fields = ['nombre_corto', 'nombre_largo', 'descripcion','duracion']

def modificarProyecto(request, usuario_id, proyecto_id_rec):
    """
    Vista que utiliza el formulario proyectoFrom para desplegar los datos editables
    del Proyecto que se quiere modificar.
        :param func: request
        :param args: usuario_id, proyecto_id_rec
        :returns: modificarProyecto.html
        :rtype: nombre_corto, nombre_largo, descripcion, estado, fecha_inicio, fecha_fin
    """
    p=proyecto.objects.get(id=proyecto_id_rec)
    if request.method == 'POST':
        form = proyectoFrom(request.POST)
        if form.is_valid():
            nombre_corto=form.cleaned_data['nombre_corto']
            nombre_largo=form.cleaned_data['nombre_largo']
            descripcion=form.cleaned_data['descripcion']
            duracion=form.cleaned_data['duracion']
            if p.estado == "PEN":
                fecha_inicio=request.POST['fecha_inicio']
                fecha_fin=datetime.strptime(request.POST['fecha_inicio'],"%Y-%m-%d").date() + timedelta(days=int(duracion))
                p.fecha_inicio=fecha_inicio
                p.fecha_fin=fecha_fin
            p.nombre_corto=nombre_corto
            p.nombre_largo=nombre_largo
            p.descripcion=descripcion
            p.duracion=duracion
            p.save() #Guardamos el modelo de manera Editada
            evento_e=usuario_id+"+"+proyecto_id_rec+"+SCRUM"+"+PROYECTO+"+"M+"+"El proyecto '"+form.cleaned_data['nombre_corto']+"' con nombre largo '"+form.cleaned_data['nombre_largo']+"' descripcion  '"+form.cleaned_data['descripcion']+"' fecha de inicio '"+str(p.fecha_inicio)+"'  fecha fin '"+str(p.fecha_fin)+"' ha sido modificado exitosamente en la fecha y hora: "+str(timezone.now())
            usuario_e=MyUser.objects.get(id=usuario_id)
            historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=p.nombre_corto, evento=evento_e)
            if usuario_e.frecuencia_notificaciones == 'instante':
                send_email(str(usuario_e.email), 'Notificacion', evento_e)

            return HttpResponse('Tu proyecto a sido guardado exitosamente')
    else:
        
        form = proyectoFrom(initial={
                                         'nombre_corto': p.nombre_corto,
                                         'nombre_largo': p.nombre_largo,
                                         'descripcion': p.descripcion,
                                         'duracion':p.duracion,
                                     
                                         })
        ctx = {'form':form, 'fecha_inicio':str(p.fecha_inicio)[:10],'proyecto':p,'usuarioid':usuario_id,'proyecto':p}
        return render_to_response('modificarProyecto.html', ctx ,context_instance=RequestContext(request))
    
def visualizarProyectoView(request,usuario_id, proyecto_id_rec):
    """
    Vista que utiliza el formulario proyectoFrom para desplegar los datos almacenados
    en el Flujo que se quiere visualizar.
        :param func: request
        :param args: usuario_id, proyecto_id_rec
        :returns: visualizarProyecto.html
    """
    proyecto_enc= proyecto.objects.get(id=proyecto_id_rec)
    return render_to_response('visualizarProyecto.html',{'proyecto':proyecto_enc,'usuarioid':usuario_id},
                                  context_instance=RequestContext(request))

def crearActividadView(request,usuario_id,proyectoid):
    """
    Vista que se obtiene del regex al presionar el boton Crear Actividad dentro del formulario
    de creacion o modificacion de Flujos, devolviendo un formulario html para crear una nueva actividad
        :param func: request
        :param args: usuario_id,proyectoid
        :returns: crearActividad.html 
        :rtype: nombre, descripcion
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
            evento_e=usuario_id+"+"+proyectoid+"+SCRUM"+"+ACTIVIDAD+"+"C+"+"La Actividad '"+form.cleaned_data['nombre']+"' con descripcion '"+form.cleaned_data['descripcion']+"' se ha creado exitosamente en la fecha y hora: "+str(timezone.now())
            usuario_e=MyUser.objects.get(id=usuario_id)
            historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(),  objeto=form.nombre,evento=evento_e)
            if usuario_e.frecuencia_notificaciones == 'instante':
                send_email(str(usuario_e.email), 'Notificacion', evento_e)
            return HttpResponse('Ha sido guardado exitosamente')       

def crearActividadAdminView(request):
    """
    Vista que se obtiene del regex al presionar el boton Crear Actividad dentro del formulario
    de creacion o modificacion de Flujos del admin, devolviendo un formulario html para crear una nueva actividad
        :param func: request
        :returns: crearActividadAdmin.html
        :rtype: nombre, descripcion
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
    Al presionar el boton Modificar Actividad, esta vista despliega una lista de todas las actividades seleccionables por el usuario
    para su modificacion.
        :param func: request 
        :returns: seleccionarActividad.html
    """
    return render(request,'seleccionarActividadAdmin.html',{'actividades':Actividades.objects.all(),})

def modificarActividadAdmin(request,actividad_id_rec):
    """
    Vista que utiliza el formulario formularioActividad para desplegar los datos editables en el admin
    de la Actividad que se quiere modificar.
        :param func: request
        :param args: actividad_id_rec
        :returns: modificarActividadAdmin.html
        :rtype: nombre, descripcion, 
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
        :param func: request
        :param args: usuario_id,proyectoid
        :returns: seleccionarActividad.html
    """
    return render(request,'seleccionarActividad.html',{'actividades':Actividades.objects.all(),'usuarioid':usuario_id,'proyectoid':proyectoid})

def modificarActividad(request,usuario_id,proyectoid,actividad_id_rec):
    """
    Vista que utiliza el formulario formularioActividad para desplegar los datos editables
    de la Actividad que se quiere modificar.
        :param func: request
        :param args: usuario_id,proyectoid,actividad_id_rec
        :returns: modificarActividad.html
        :rtype: nombre, descripcion
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
            evento_e=usuario_id+"+"+proyectoid+"+SCRUM"+"+ACTIVIDAD+"+"M+"+"La actividad '"+form.cleaned_data['nombre']+"' con descripcion '"+form.cleaned_data['descripcion']+"' ha sido modificado exitosamente en la fecha y hora: "+str(timezone.now())
            usuario_e=MyUser.objects.get(id=usuario_id)
            historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=p.nombre, evento=evento_e)
            if usuario_e.frecuencia_notificaciones == 'instante':
                send_email(str(usuario_e.email), 'Notificacion', evento_e)

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
    los id's del rol , proyecto y el usuario creador.
        :param func: request
        :param args: usuario_id, proyectoid,rolid, rol_id_rec
        :returns: asignaRolProyecto.html
        :rtype: usuarios
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
    """
    Esta vista debe obtener los datos de los usuarios que han sido asignados a un rol en el proyecto,el parametro
    usuario_id se necesita simplemente para el render para poder retornar a rol-flujo-para-scrum
        :param func: request
        :param args: proyecto_id_rec,usuario_id
        :returns: formarEquipo.html 
    """
    lista={}
    proyectox=proyecto.objects.get(id=proyecto_id_rec)
    for a in asignacion.objects.all():
        if a.proyecto.id == proyectox.id:#si el proyecto relacionado a una asignacion es el que se esta viendo ahora
            rol_a=rol.objects.get(id=a.rol.id)
            usuario_a=MyUser.objects.get(id=a.usuario.id)
            lista[usuario_a]=rol_a#agregar el usuario de esa asignacion a la vista, y mandarlo al template
    return render(request,'formarEquipo.html',{'roles':rol.objects.all(),'lista_asigna':lista, 'flujos':Flujo.objects.all(),'proyecto':proyectox,'usuario_id':usuario_id})

def delegarHU(request,usuario_id,proyectoid,rolid,hu_id,reasignar):
    """
    Delega o asigna una HU a un usuario miembro del proyecto, y en caso de ser necesario, reasignar la HU
    a otro usuario evitando duplicaciones en la Base de Datos
        :param func: request
        :param args: 
        :returns: asignaHU.html
        :rtype: usuarios
    """
    proyectox=proyecto.objects.get(id=proyectoid)
    hu=HU.objects.get(id=hu_id)
    if request.method=='POST' :
        if reasignar == '0':
            try:
                delegacionx= delegacion.objects.create(usuario=MyUser.objects.get(id=request.POST['usuario']),hu=hu)
                delegacionx.save()
                evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"HU+"+"AS+"+"Se ha asignado una HU '"+hu.descripcion+"' al usuario '"+str(delegacionx.usuario)+"' en la fecha y hora: "+str(timezone.now())
                usuario_e=MyUser.objects.get(id=usuario_id)
                historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=hu.descripcion, evento=evento_e)
                if usuario_e.frecuencia_notificaciones == 'instante':
                    send_email(str(usuario_e.email), 'Notificacion', evento_e)

                return HttpResponse('La asignacion se realizo correctamente')
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/crearFlujo/') #redirijir a rol flujo para scrum despues
        else:
            for d in delegacion.objects.all():
                if d.hu == hu:
                    d.usuario=MyUser.objects.get(id=request.POST['usuario'])
                    d.save()
                    usuario_e=MyUser.objects.get(id=usuario_id)
                    evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"HU+"+"AS+"+"Se ha asignado una HU '"+hu.descripcion+"' al usuario '"+str(d.usuario)+"' en la fecha y hora: "+str(timezone.now())
                    historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=hu.descripcion, evento=evento_e)
                    if usuario_e.frecuencia_notificaciones == 'instante':
                        send_email(str(usuario_e.email), 'Notificacion', evento_e)
                    return HttpResponse('Se ha reasignado la HU exitosamente')
    else:
        users=hu.sprint().equipo.all()
        usuario_asignado=[]
        if reasignar == '1':
            for d in delegacion.objects.all():
                if d.hu == hu:
                    usuario_asignado = d.usuario
        
        return render(request,'asignaHU.html',{'sprint':hu.sprint(),'usuario_asignado':usuario_asignado, 'proyecto':proyectox,'usuarios':users,'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid})
    
def validarHU(request, usuario_id, proyectoid, rolid, HU_id_rec,is_Scrum):
    """
    Controla la validacion de una HU creada por el product owner
        :param func: request
        :param args: usuario_id, proyectoid, rolid, HU_id_rec,is_Scrum
        :returns: validarHU.html
    """
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
        :param func: request
        :param args: usuario_id, proyectoid, rolid
        :returns: visualizarBacklog.html
    """
    proyectox=proyecto.objects.get(id=proyectoid)
    huss=HU.objects.all().filter(proyecto=proyectox).filter(estado='ACT').filter(valido=True).filter(sprint__hu__isnull=True)
    hu=sorted(huss,key=lambda x: x.prioridad, reverse=True)
    HUs_pendientes=[]
    for x in Sprint.objects.filter(proyecto=proyectox):
        if x.estado == 'FIN':
            for h in x.hu.all():
                if h.estado_en_actividad != 'APR':
                    HUs_pendientes.append(h)
    for x in Sprint.objects.filter(proyecto=proyectox):
        if x.estado != 'FIN':
            for h in x.hu.all():
                for hp in HUs_pendientes:
                    if h == hp:
                        HUs_pendientes.remove(h)  
    return render(request,'visualizarBacklog.html',{'HUs_pendientes':HUs_pendientes,'huss':hu, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid})

def reactivar(request, usuario_id, proyectoid, rolid, tipo, id_tipo):
    """
    Vista que permite reactivar un flujo, HU o Sprint cancelado por el usuario,
    para su correspondiente uso o modificacion, ya que los objetos cancelados
    solo estan disponibles para su visualizacion, no para su asignacion o modificacion.
    Recibe un tipo en la url que le permite distinguir de que tipo de objeto se trata.
        :param func: request
        :param args: usuario_id, proyectoid, rolid, tipo, id_tipo
        :returns: '/scrum/'+usuario_id+'/'+proyectoid+'/'+rolid+'/'
    """
    usuario_e=MyUser.objects.get(id=usuario_id)
    if tipo == '1': #se trata de un flujo
        f=Flujo.objects.get(id=id_tipo)
        f.estado='ACT'
        f.save()
        evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"FLUJO+"+"R+"+"El flujo '"+f.nombre+"' se ha reactivado exitosamente en la fecha y hora: "+str(timezone.now())
        historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=f.nombre,evento=evento_e)
        if usuario_e.frecuencia_notificaciones == 'instante':
            send_email(str(usuario_e.email), 'Notificacion', evento_e)
            
    if tipo == '2': #se trata de una HU
        h=HU.objects.get(id=id_tipo)
        h.estado='ACT'
        h.save()
        evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"HU+"+"R+"+"La HU '"+h.descripcion+"' se ha reactivado exitosamente en la fecha y hora: "+str(timezone.now())
        historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=h.descripcion, evento=evento_e)
        if usuario_e.frecuencia_notificaciones == 'instante':
            send_email(str(usuario_e.email), 'Notificacion', evento_e)

    if tipo == '3': #se trata de un sprint
        s=Sprint.objects.get(id=id_tipo)
        s.estado='ACT'
        s.save()
        evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"SPRINT+"+"R+"+"El sprint '"+s.descripcion+"' se ha reactivado exitosamente en la fecha y hora: "+str(timezone.now())
        historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=s.descripcion,evento=evento_e)
        if usuario_e.frecuencia_notificaciones == 'instante':
            send_email(str(usuario_e.email), 'Notificacion', evento_e)

    if tipo == '4': #se trata de un rol
        s=rol.objects.get(id=id_tipo)
        s.estado='ACT'
        s.save()
        evento_e=usuario_id+"+"+proyectoid+"+"+rolid+"+"+"ROL+"+"R+"+"El rol '"+s.nombre_rol_id+"' se ha reactivado exitosamente en la fecha y hora: "+str(timezone.now())
        historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=s.nombre_rol_id,evento=evento_e)
        if usuario_e.frecuencia_notificaciones == 'instante':
            send_email(str(usuario_e.email), 'Notificacion', evento_e)
    
    if tipo == '5': #se trata de un proyecto
        s=proyecto.objects.get(id=id_tipo)
        s.estado='ACT'
        s.save()
        evento_e=usuario_id+"+"+proyectoid+"+SCRUM+"+"PROYECTO+"+"R+"+"El proyecto '"+s.nombre_corto+"' se ha reactivado exitosamente en la fecha y hora: "+str(timezone.now())
        historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=s.nombre_corto,evento=evento_e)
        if usuario_e.frecuencia_notificaciones == 'instante':
            send_email(str(usuario_e.email), 'Notificacion', evento_e)
            
        return HttpResponseRedirect('/hola/')
    return HttpResponseRedirect('/scrum/'+usuario_id+'/'+proyectoid+'/'+rolid+'/')


def adminAdjunto(request, usuario_id, proyectoid, rolid, HU_id_rec):
    """
    Vista que gestiona el guardado de archivos adjuntos a HUs    
        :param func: request
        :param args: usuario_id, proyectoid, rolid, HU_id_rec
        :returns: adjuntos.html
    """
    if request.method=='GET':
        hux=HU.objects.get(id=HU_id_rec)
        adjuntos=[]
        try: 
            adjuntos=archivoadjunto.objects.filter(hU=hux).filter(estado='ACT')
        except ObjectDoesNotExist:
            adjuntos = []
        return render(request,'adjuntos.html',{'HU':hux,'adjuntos':adjuntos,'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid})
    else:
        archivox = request.FILES['archivo']
        file=bytearray()
        for d in archivox.chunks():
            file.extend(d)
        n=0
        split=archivox.name.split('.')
        cambiar=split[0]
        while archivoadjunto.objects.filter(nombre=cambiar).filter(estado='ACT'):
            n=n+1
            split=archivox.name.split('.')
            cambiar=split[0]+"("+str(n)+")"
            
        filex=archivoadjunto.objects.create(nombre=cambiar,content=archivox.content_type,tamanho=archivox.size,archivo=file,hU_id=HU_id_rec,estado='ACT',version=1.0)
        filex.save()
        version=adjuntoVersion.objects.create(archivo_original=filex,version=1.0,nombre=cambiar,content=archivox.content_type,tamanho=archivox.size,archivo=file,estado='ACT',descripcion='Primera version')
        version.save()
        #archivox.save()
        return HttpResponseRedirect('/adminAdjunto/'+usuario_id+'/'+proyectoid+'/'+rolid+'/'+HU_id_rec+'/')
    
def descargar(request, usuario_id, proyectoid, rolid, HU_id_rec,archivo_id):
    """
     Descarga el archivo adjunto seleccionado 
        :param func: request
        :param args: usuario_id, proyectoid, rolid, HU_id_rec,archivo_id
        :returns: response = HttpResponse(content_type=archivox.content)
    """
    archivox=archivoadjunto.objects.get(id=archivo_id)
    response = HttpResponse(content_type=archivox.content)
    response['Content-Disposition'] = 'attachment; filename="%s"' % archivox.nombre
    buffer = BytesIO(archivox.archivo)
    file = buffer.getvalue()
    buffer.close()
    response.write(file)
    return response

def eliminar_adjunto(request, usuario_id, proyectoid, rolid, HU_id_rec,archivo_id):
    """
    Elminar archivo adjunto desde el admin
        :param func: request
        :param args: usuario_id, proyectoid, rolid, HU_id_rec,archivo_id
        :returns: '/adminAdjunto/'+usuario_id+'/'+proyectoid+'/'+rolid+'/'+HU_id_rec+'/'
    """
    archivox=archivoadjunto.objects.get(id=archivo_id)
    archivox.estado='CAN'
    archivox.save()
    return HttpResponseRedirect('/adminAdjunto/'+usuario_id+'/'+proyectoid+'/'+rolid+'/'+HU_id_rec+'/')

def cambiarVersionAdjunto(request, usuario_id, proyectoid, rolid, HU_id_rec,archivo_id):
    adjunto=archivoadjunto.objects.get(id=archivo_id)
    versiones=adjuntoVersion.objects.filter(archivo_original=adjunto).filter(estado='ACT')
    if request.method=='GET':
        versiones=versiones.exclude(version=adjunto.version)
        return render(request,'versionesAdjunto.html',{'adjunto':adjunto,'versiones':versiones,'usuarioid':usuario_id,'proyectoid':proyectoid,'rolid':rolid,'huid':HU_id_rec,'archivoid':archivo_id})
    else:
        x=0.0
        lastx=len(versiones.all())
        ultima_version= adjunto
        if lastx>0:
            x=versiones.last().version
            ultima_version=versiones.last()

        archivox = request.FILES['archivo']
        desc = request.POST['descripcion']
        name = request.POST['name']

        if name == ultima_version.nombre and archivox.content_type == ultima_version.content:
            x=x+0.1
        else:
            x=math.floor(x)+1.0
        file=bytearray()
        for d in archivox.chunks():
            file.extend(d)

        version=adjuntoVersion.objects.create(archivo_original=adjunto,version=x,nombre=name,content=archivox.content_type,tamanho=archivox.size,archivo=file,estado='ACT',descripcion=desc)
        version.save()
        #archivox.save()
        return HttpResponseRedirect('/cambiarAdjunto/'+usuario_id+'/'+proyectoid+'/'+rolid+'/'+HU_id_rec+'/'+archivo_id+'/')
    
def elegirVersionAdjunto(request,archivo_id,version_id):
    """
    Esta vista responde al boton elegir al elegir una version anterior de hu, ya que si vuelvo a hacer un simple modificar
    pordria volver a crear una version que ya existe, por lo tanto esta vista modifica con datos preexistenes sin
    crear una nueva version
    Primero obtengo la huversion saco los datos los meto en la hu que tambien tengo que obtener y le doy hu.save()
        :param func: request
        :param args: hv_id, hu_id 
        :returns: 'Se ha cambiado de version correctamente'
    """
    version=adjuntoVersion.objects.get(id=version_id)
    adjunto=archivoadjunto.objects.get(id=archivo_id)
    
    adjunto.nombre=version.nombre
    adjunto.content=version.content
    adjunto.tamanho=version.tamanho
    adjunto.estado=version.estado
    adjunto.archivo=version.archivo
    adjunto.version=version.version
    adjunto.save()
    return HttpResponse('Se ha cambiado de version correctamente')

def visualizarSprintBacklog(request, usuario_id, proyectoid, rolid):
    """
    El sprint backlog es una lista de las tareas identificadas por el equipo de Scrum
    Los equipos estiman el numero de horas para cada tarea que se corresponde a alguien del equipo para completar.
        :param func: request
        :param args: usuario_id, proyectoid, rolid
        :returns: visualizarSprintBacklog.html
    """
    class descripcionHU:
        """Obtiene toda la informacion de una hu"""
        def __init__(self,dias, duracionhu, pendiente, p):
            self.dias=dias
            self.duracionhu=duracionhu
            self.pendiente=pendiente
            self.p=p
    
    class usu_estado:
        """Guarda el usuario y el estado en actividad de una HU dentro de un Sprint"""
        def __init__(self,usuario, estado):
            self.usuario=usuario
            self.estado=estado
    class sprint_acu_fecha:
        """Guarda el fecha fin e Inicio y el acumulado de todas las HU dentro de un Sprint"""
        def __init__(self,fecha_f, fecha_i):
            self.fecha_f=fecha_f
            self.fecha_i=fecha_i
    class acu_color:
        """Guarda el acumulado y el color"""
        def __init__(self, acum, color):
            self.acum=acum
            self.color=color        
            
   

    dias=0
    hux=HU.objects.filter(proyecto=proyecto.objects.get(id=proyectoid))
    sprint=Sprint.objects.filter(proyecto=proyecto.objects.get(id=proyectoid))
    s=sorted(sprint,key=lambda x: x.estado, reverse=False)
    
    #obtengo las fechas
    lista_fecha=[]
    for sp in sprint:
        if sp.estado == 'CON':
            dias=sp.duracion-1
            contador=-1
            while dias > contador:
                lista_fecha.append(((sp.fecha_inicio)+timedelta(days=contador)).strftime('%Y-%m-%d'))
                contador += 1
    #obtengo las dias
    lista_dias=[]
    for sp in sprint:
        if sp.estado == 'CON':
            dias=sp.duracion
            contador=1
            while dias >= contador:
                lista_dias.append(contador)
                contador += 1
                
    hu_x=sorted(hux,key=lambda x: x.prioridad, reverse=True)   

    longitud_para_tabla={}
    for i in sprint:
        longitud_para_tabla[i]=len(i.hu.all())+1
        
    usuario_hu={}
    for h in hu_x:
        for d in delegacion.objects.all():
            if h.id == d.hu.id:
                usuario=d.usuario
                estado=h.estado_en_actividad
                usuario_hu[h]=usu_estado(usuario, estado)#hu-usuario-estado
    
    longitud_equipo=[]
    usu=""
    for i, u in usuario_hu.items():
            if usu=="":
                usu=u.usuario
                #longitud_equipo[i]=usu
                longitud_equipo.append(usu)
            elif usu != u.usuario:
                usu=u.usuario
                #longitud_equipo[i]=usu
                longitud_equipo.append(usu)#los usuarios
        
    fecha_fin_sprint=0
    fecha_inicio=0
    lista_sprint={}
    for hu in hu_x:
        for sp in sprint:
                    for h in sp.hu.all():
                        if h == hu:
                            if sp.estado == 'CON':    
                                fecha_fin_sprint=(sp.fecha_inicio+timedelta(days=(sp.duracion-1))).strftime('%Y-%m-%d')
                                fecha_inicio=(sp.fecha_inicio+timedelta(days=0)).strftime('%Y-%m-%d')
        lista_sprint[sp]=sprint_acu_fecha(fecha_fin_sprint,fecha_inicio )
    #La duracion en horas de un Sprint
    sprint_acu_fecha=0
    lista_sprint_acu_fecha={}
    for sp in sprint:
        for hu in hu_x:
                for h in sp.hu.all():
                    if h == hu:
                        sprint_acu_fecha=sprint_acu_fecha+hu.duracion     
        lista_sprint_acu_fecha[sp]=sprint_acu_fecha
        
    lista_hu_horas={}
    descripcion_hu={}
    lista_horas=[]
    cont2=0        
    fecha_x=[]
    pendiente=0
    dura=0
    aux=1
    hasta=1
    desde=0
    nuevo_usu=""
    #for hu in hu_x:
    for hu, u in usuario_hu.items():
        lista_horas=[]
        acumulador=0
        
        hasta+=hu.dias_hu(hu.duracion)#cantidad de dias
        aux=1
        usu=u.usuario
        
        for fecha_x in lista_fecha:
            cont2=0
            for h in hu.hu_descripcion.all():
                x=str((h.fecha+timedelta(days=-1)).strftime('%Y-%m-%d'))
                if str(fecha_x) == x[:10]:
                    cont2=cont2+h.horas_trabajadas
                    
            if nuevo_usu != usu:
                nuevo_usu=usu
                desde=1
                hasta=hu.dias_hu(hu.duracion)#cantidad de dias
                
            if aux>=desde and aux<=hasta:
                    lista_horas.append(acu_color(cont2, 1))
            else:
                lista_horas.append(acu_color(cont2, 0))
            aux+=1
                        
            acumulador=acumulador+cont2#el acumulado optiene el total de horas que realizo en varios dias de trabajo
            
            lista_hu_horas[hu]=lista_horas
            
            pendiente=hu.duracion
            pendiente=pendiente-acumulador#Lo que le resta de la duracion para terminar la HU

        dias=hu.dias_hu(hu.duracion) #retorna la cantidad de dias de la HU
        desde=hasta+1
        dura=hu.duracion#cuantas horas dura
        if pendiente==0:
            p=1
        else:
            p=0                
        descripcion_hu[hu]=descripcionHU(dias, dura, pendiente, p)
            
    return render(request,'visualizarSprintBacklog.html',{'len':longitud_para_tabla,'sprint':s, 'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid, 'HUx':hu_x, 'lista':lista_hu_horas, 'usuario_hu':usuario_hu, 'descripcionHU':descripcion_hu, 'fecha_fin_s':fecha_fin_sprint, 'lista_sprint':lista_sprint, 'fechas':lista_fecha, 'dura_sprint':lista_sprint_acu_fecha, 'dias':lista_dias, 'hu_x':hu_x, 'lep':usuario_hu})

def asignarHU_Usuario_FLujo(request,usuario_id,proyectoid,rolid,sprintid):
    """ 
    Vista de asignacion de una HU a un usuario y en un flujo
        :param func: request
        :param args: usuario_id,proyectoid,rolid,sprintid
        :returns: asignarHU_Usuario_Flujo.html 
    """
    proyectox=proyecto.objects.get(id=proyectoid)
    sprintx=Sprint.objects.get(id=sprintid)
    hus=HU.objects.filter(proyecto=proyectox,estado='ACT',valido=True).filter(sprint=sprintx)
    hu_en_flujo={}
    
    fin=1
    for h in sprintx.hu.all():
        if h.estado_en_actividad != 'APR':
            fin=0
    if fin == 1:
        sprintx.estado='FIN'
        sprintx.save()
        
    for f in Flujo.objects.filter(sprint=Sprint.objects.get(id=sprintid)):
        for a in asignaHU_actividad_flujo.objects.all():
            if f == a.flujo_al_que_pertenece:
                for h in a.lista_de_HU.all():
                    if h.proyecto == proyectox and h.sprint() == sprintx:
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
    flujos_aprobados=[]
    for f in Flujo.objects.filter(sprint=Sprint.objects.get(id=sprintid)):
        x=0
        if hu_en_flujo.has_key(f):
            for h in hu_en_flujo[f]:
                if h.estado_en_actividad != 'APR':
                    x=1
            if x == 0:
                flujos_aprobados.append(f)
    return render(request,"asignarHU_Usuario_Flujo.html",{'flujos_aprobados':flujos_aprobados,'hu_en_flujo':hu_en_flujo,'flujos':Flujo.objects.filter(sprint=Sprint.objects.get(id=sprintid)),'HU_no_asignada':HU_no_asignada,'HU_asignada':HU_asignada,'hus':hus,'sprint':sprintx,'proyecto':proyectox,'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid})

def asignarHU_a_FLujo(request,usuario_id,proyectoid,rolid,sprintid,flujo_id):
    """
    Vista donde se asignan las HU a un flujo dentro del spring y a un usuario del proyecto
        :param func: request
        :param args: usuario_id,proyectoid,rolid,sprintid,flujo_id
        :returns: asignarHUFlujo.html
    """
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
        return render(request,"asignarHUFlujo.html",{'flujo':flujo,'hus':hus,'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid,'sprint':sprintx,'flujo_id':flujo_id})

def verKanban(request,usuario_id,proyectoid,rolid,sprintid):
    """
    Vista que permite acceder al template de visualizacion de un flujo graficamente en el kanban
        :param func: request
        :param args: usuario_id,proyectoid,rolid,sprintid
        :returns: verKanban.html
    """
    sprintx=Sprint.objects.get(id=sprintid)
    flujos_hu={}
    flujos_actividades={}
    kanban=1
    proyectox=proyecto.objects.get(id=proyectoid)
    lista_hu=[]
    for f in sprintx.flujo.all():
        for a in asignaHU_actividad_flujo.objects.filter(flujo_al_que_pertenece=f):
            lista_hu=[]
            x=0
            for h in a.lista_de_HU.all():
                if h.sprint() == sprintx and h.proyecto == proyectox:
                    x=1
                    lista_hu.append(h)
            if x == 1:
                flujos_hu[f]=lista_hu
                break
    for f in sprintx.flujo.all():
        jsonDec = json.decoder.JSONDecoder()
        orden=jsonDec.decode(f.orden_actividades)
        actividades=[]
        for o in orden:
            actividades.append(Actividades.objects.get(id=o))
        flujos_actividades[f]=actividades
    flujos_aprobados=[]
    for f in sprintx.flujo.all():
        x=0
        if flujos_hu.has_key(f):
            for h in flujos_hu[f]:
                if h.estado_en_actividad != 'APR':
                    x=1
            if x == 0:
                flujos_aprobados.append(f)
                   
    return render(request,"verKanban.html",{'flujos_aprobados':flujos_aprobados,'sprint':sprintx, 'flujos_hu':flujos_hu,'flujos_actividades':flujos_actividades,'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid, 'kanban':kanban})

def aprobarHU(request, usuario_id, proyectoid, rolid, sprintid, HU_id_rec):
    """
    Vista que permite al Scrum aprobar una HU o volver a un estado anterior del flujo.
        :param func: request
        :param args: usuario_id, proyectoid, rolid, sprintid, HU_id_rec
        :returns: aprobar_finalizacion_Flujo.html
        :rtype: actividad, estado, duracion, descripcion
    """
    HU_tratada=HU.objects.get(id=HU_id_rec)
    usuario_asignado=HU_tratada.saber_usuario()
    if request.method == 'GET':
        f=HU_tratada.flujo()
        estados=['PEN','PRO']
        jsonDec = json.decoder.JSONDecoder()
        orden=jsonDec.decode(f.orden_actividades)
        actividades=[]
        for o in orden:
            actividades.append(Actividades.objects.get(id=o))
        return render(request,"aprobar_finalizacion_Flujo.html",{'usuario_asignado':usuario_asignado,'HU':HU_tratada,'flujo':f,'estados':estados,'actividades':actividades,'sprintid':sprintid,'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid})
    else:
        guardar=0
        for g in request.POST.getlist('_save'):
            if g == 'Aprobar':
                guardar=1
        if guardar == 1:
            HU_tratada.estado_en_actividad='APR'
            HU_tratada.save()
            hd=HU_descripcion.objects.create(horas_trabajadas=0,descripcion_horas_trabajadas='HU aprobada por SCRUM',fecha=datetime.now(), actividad=str(HU_tratada.actividad), estado=str(HU_tratada.estado_en_actividad))
            HU_tratada.hu_descripcion.add(HU_descripcion.objects.get(id=hd.id))
            hd.save()
            return HttpResponseRedirect('/verKanban/'+usuario_id+'/'+proyectoid+'/'+rolid+'/'+sprintid+'/')
        else:
            actividad=Actividades.objects.get(id=request.POST['actividad'])
            estado=request.POST['estado']
            duracion=float(request.POST['duracion'])
            if duracion >= HU_tratada.duracion:
                HU_tratada.actividad=actividad
                HU_tratada.estado_en_actividad=estado
                HU_tratada.duracion=duracion
                HU_tratada.save()
                descripcion=request.POST['descripcion']
                hd=HU_descripcion.objects.create(horas_trabajadas=0,descripcion_horas_trabajadas=descripcion,fecha=datetime.now(), actividad=str(HU_tratada.actividad), estado=str(HU_tratada.estado_en_actividad))
                HU_tratada.hu_descripcion.add(HU_descripcion.objects.get(id=hd.id))
                hd.save()
                return HttpResponseRedirect('/verKanban/'+usuario_id+'/'+proyectoid+'/'+rolid+'/'+sprintid+'/')
            else:
                return HttpResponse('La duracion no puede ser menor a las horas ya acumuladas, que son: '+str(HU_tratada.acumulador_horas))


def cambiarVersionHU(request,usuario_id, proyectoid,rolid,hu_id):
    """
    Obtener primero todas las HUversion que no sean la actual y enviarlas al template para que el user pueda elegirlas 
    y cambiar por la version deseada 
        :param func: request
        :param args: usuario_id, proyectoid,rolid,hu_id
        :returns: listarVersionesHU.html
    """
    #obtener primero todas las HUversion que no sean la actual y enviarlas al template para que el user pueda elegirlas
    hu_now=HU.objects.get(id=hu_id)
    huv=HU_version.objects.filter(hu__id=hu_id) 
    huv=huv.exclude(version=hu_now.version)#tengo que excluir la version actual de la lista
    return render(request,"listarVersionesHU.html",{'hu_actual':hu_now,'huv':huv,'usuarioid':usuario_id,'proyectoid':proyectoid,'rolid':rolid,'huid':hu_id})

def reasignarhuFlujo(request,usuario_id, proyectoid,rolid,sprintid,huid,kanban):
    """
    Vista que permita reasignar una hu con tiempo agotado a otro flujo y agregar horas a su duracion prevismente establecida para
    porder continuar desarrollandola el tiempo que sea requerido
    En el template el usuario podra elegir de una lista de flujos, parecido a delegarHU la que prefiera para continuar la hu, ademas tendra un campo para aumentar
    el numero de horas de duracion de la hu, ya que necesitaba mas, la misma empezara en la actividad de orden 1 del flujo nuevo
        :param func: request
        :param args: usuario_id, proyectoid,rolid,sprintid,huid,kanban
        :returns: reasignarhuflujo.html
        :rtype: duracionmas
    """
    #Primero obtener la hu  y el sprint
    hu_now=HU.objects.get(id=huid)
    sprint_now=Sprint.objects.get(id=sprintid)
    #y tambien el proyecto por las dudas
    proyecto_now=proyecto.objects.get(id=proyectoid)
    #y todos los flujos de este proyecto
    if request.method=='GET' :
    
        
        flujos=sprint_now.flujo.all().exclude(id=hu_now.flujo().id)
        #Necesito mandarle tambien la duracion de la hu, pero eso puede ser accedido desde hu_now
        return render(request,'reasignarhuflujo.html',{'flujo_actual':hu_now.flujo(),'kanban':kanban,'hu':hu_now,'sprint':sprint_now,'proyecto':proyecto_now,'flujos':flujos,'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid})
    else:
        """Cuando sea post se tienen que hacer ciertos cambios con los datos"""
        for a in request.POST.getlist('flujos'):
        #uno solo es lo que hay en a
            flujox=Flujo.objects.get(id=a)
            jsonDec = json.decoder.JSONDecoder()
            orden=jsonDec.decode(flujox.orden_actividades)
            hu_now.actividad=Actividades.objects.get(id=orden[0])
            hu_now.estado_en_actividad='PEN'
            hu_now.save()
            
            #remuevo el manytomany de la hu al flujo anterior
            asig=asignaHU_actividad_flujo.objects.filter(flujo_al_que_pertenece=hu_now.flujo())
            if asig:
                for f in asig:
                    for h in f.lista_de_HU.filter(proyecto=proyecto_now):
                        if h == hu_now:
                            f.lista_de_HU.remove(h)
                            f.save()
            
            #agrego el nuevo flujo relacionado a la HU
            asig=asignaHU_actividad_flujo.objects.filter(flujo_al_que_pertenece=flujox)
            if asig:
                for f in asig:
                    f.lista_de_HU.add(hu_now)
                    f.save()
                            
        hu_now.duracion+= float(request.POST['duracionmas'])
        hu_now.save()
        
        return HttpResponse('Se ha cambiado de flujo correctamente a'+hu_now.flujo().nombre)

def desplegar_historial(request,usuario_id,proyectoid,rolid):
    """
    Desplegar el historial de las actividades que se han realizado
        :param func: request
        :param args: usuario_id,proyectoid,rolid
        :returns: 'historial.html'
    """
    sprint_c=[]
    sprint_m=[]
    sprint_r=[]
    sprint=0
    flujo_c=[]
    flujo_m=[]
    flujo_r=[]
    flujo=0
    rol_c=[]
    rol_m=[]
    rol_r=[]
    rol=0
    actividad_c=[]
    actividad_m=[]
    actividad=0
    hu_c=[]
    hu_m=[]
    hu_a=[]
    hu_as=[]
    hu_r=[]
    hu=0
    proyecto_m=[]
    proyecto_r=[]
    proyecto_a=[]
    proyecto_f=[]
    proyecto=0
    usuario_rec=MyUser.objects.get(id=usuario_id)
    if rolid == str(1):
        h=historial_notificacion.objects.all()
    else:
        h=historial_notificacion.objects.filter(usuario=usuario_rec.username)
    for n in h:
        obtenerStrings=n.evento.split('+')
        proyecto=obtenerStrings[1]
        rol=obtenerStrings[2]
        objeto=obtenerStrings[3]
        tipo_evento=obtenerStrings[4]
        evento=obtenerStrings[5]
        if proyecto == proyectoid and (rol == rolid or rolid == str(1)):
            if objeto == 'ROL':
                rol=1
                if tipo_evento == 'C':
                    rol_c.append(evento)
                elif tipo_evento == 'M':
                    rol_m.append(evento)
                elif tipo_evento == 'R':
                    rol_r.append(evento)
            elif objeto == 'FLUJO':
                flujo=1
                if tipo_evento == 'C':
                    flujo_c.append(evento)
                elif tipo_evento == 'M':
                    flujo_m.append(evento)
                elif tipo_evento == 'R':
                    flujo_r.append(evento)
            elif objeto == 'SPRINT':
                sprint=1
                if tipo_evento == 'C':
                    sprint_c.append(evento)
                elif tipo_evento == 'M':
                    sprint_m.append(evento)
                elif tipo_evento == 'R':
                    sprint_r.append(evento)
            elif objeto == 'HU':
                hu=1
                if tipo_evento == 'C':
                    if rolid == str(1): hu_c.append("Usuario: "+n.usuario+"- Evento: "+evento)
                    else: hu_c.append(evento)
                elif tipo_evento == 'M':
                    if rolid == str(1): hu_m.append("Usuario: "+n.usuario+"- Evento: "+evento)
                    else: hu_m.append(evento)
                elif tipo_evento == 'A':
                    if rolid == str(1): hu_a.append("Usuario: "+n.usuario+"- Evento: "+evento)
                    else: hu_a.append(evento)
                elif tipo_evento == 'AS':
                    hu_as.append(evento)
                elif tipo_evento == 'R':
                    if rolid == str(1): hu_r.append("Usuario: "+n.usuario+"- Evento: "+evento)
                    else: hu_r.append(evento)
        if proyecto == proyectoid and rol == 'SCRUM':   
            if objeto == 'ACTIVIDAD':
                actividad=1
                if tipo_evento == 'C':
                    actividad_c.append(evento)
                elif tipo_evento == 'M':
                    actividad_m.append(evento)
            if objeto == 'PROYECTO':
                proyecto=1
                if tipo_evento == 'A':
                    proyecto_a.append(evento)
                elif tipo_evento == 'M':
                    proyecto_m.append(evento)
                elif tipo_evento == 'R':
                    proyecto_r.append(evento)
                elif tipo_evento == 'F':
                    proyecto_f.append(evento)

    return render(request,'historial.html',{'sprint':sprint,'flujo':flujo,'actividad':actividad,'hu':hu,'proyecto':proyecto,'rol':rol,'proyecto_m':proyecto_m,'proyecto_a':proyecto_a,'proyecto_r':proyecto_r,'proyecto_f':proyecto_f,'sprint_c':sprint_c,'sprint_m':sprint_m,'sprint_r':sprint_r,'flujo_c':flujo_c,'flujo_m':flujo_m,'flujo_r':flujo_r,'rol_c':rol_c,'rol_m':rol_m,'rol_r':rol_r,'actividad_c':actividad_c,'actividad_m':actividad_m,'hu_c':hu_c,'hu_m':hu_m,'hu_a':hu_a,'hu_as':hu_as,'hu_r':hu_r,'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid})



def visualizarBurnDownChart(request,usuario_id,proyectoid,rolid):
    """
    Genera los datos para mostrar en el BurndownChart que son las horas restantes del spint que quedan por hacer luego del progreso 
    total que se haya obtenido en un dia dado
        :param func: request
        :param args: usuario_id,proyectoid,rolid
        :returns: burndown.htm
    """
    sprint= Sprint.objects.get(estado='CON').filter(proyecto__id=proyectoid)#esto es un quiryset....que sea un elemento nomas!!!!!!!!
    #sprint ahora tiene el Sprint que se va mostrar en el burndown de este proyecto...el actual nose si hay que mostrar de todos?
    duracionsp=range(int(sprint.duracion))
    hus=HU.objects.all().filter(proyecto__id=proyectoid)
    #tengo todas las hu de este proyecto ahora, necesito solo las de este sprint
    hux=[]
    for u in hus:
        if u.sprint()==sprint:
            hux.append(u)
            
    #ahora ya tengo todas las hu del sprint en hux
    #tengo que sumar sus duraciones para saber el maximo del backlog
    sumx=0
    for ux in hux:
        sumx+=ux.duracion
    #ahora tengo que trabajar con el acumulador de horas diario que seria una lista por dia de todas las hu del dia
    #parecido al de abajo pero en vez de lista_hu_horas seria lista fecha horas
    #supongo que antes deberia saber cuantas fechas tener en cuenta...no estoy seguro                                                         
    lista_fechas=[]
    lista_horas=[]
    lista_fechas.append(str((sprint.fecha_inicio+timedelta(days=-1)).strftime('%Y-%m-%d'))[:10])
    lista_horas.append(0)
    #el primer elemento del diccionario va a ser la duracion total de todas las hu osea la primera barra del burndown
    for hu in hux:
        for d in hu.hu_descripcion.all().order_by('fecha'):
            f=str((d.fecha+timedelta(days=-1)).strftime('%Y-%m-%d'))[:10] 
            if f in lista_fechas:
                lista_horas[lista_fechas.index(f)]=lista_horas[lista_fechas.index(f)]+d.horas_trabajadas
            else:
                lista_fechas.append(f)
                lista_horas.insert(lista_fechas.index(f),d.horas_trabajadas)
                
        
    #tengo la lista correcta pero con fechas mal colocadas 
            
    
    # Un diccionario puede tener elementos repetidos(keys), pero la programacion anterior va a impedirlo 
    #bueno ahora ya tengo el diccionario con el total de horas por dia cargadas me convendria disponer de la longitud del diccionario
    cant_days=len(lista_fechas)
    # ahora voy a crear y cargar el diccionario que se va mandar al template
    
    tot_restante=sumx
    horas_restantes=[]
    #tot_restante es la que va disminuir, sum quiero mantener por las dudas
    
    
    for i in lista_fechas:
        horas_restantes.insert(lista_fechas.index(i),tot_restante-lista_horas[lista_fechas.index(i)])
        tot_restante=tot_restante-lista_horas[lista_fechas.index(i)]
    horas_restantes.insert(0,sumx)
    
    
    pordia=sumx/sprint.duracion
    estimacion=[]
    tot_again=sumx
    for x in duracionsp:
        estimacion.insert(duracionsp.index(x),tot_again-pordia)
        tot_again=tot_again-pordia
        
    estimacion.insert(0,sumx)  

    #AHora utilizando la lista lista_horas deberia calcular el resto del grafo, osea lista_horas debe ser mas largo o al menos 
    #tener otra lista igual a lista horas que dibuje la linea negra en el burndown
    
    #estimacion nueva deberia tener una lista propia con lista_horas como primeros elementos mas nuevos elementos
    #correspondientes a la estimacion actual calculada
    
    nueva_estimacion=list(horas_restantes)
    #calcular aqui el promedio de horas por dia en lista_horas
    suma_cargadas=0
    for x in lista_horas: 
        suma_cargadas=suma_cargadas+x
        pass
    prome=suma_cargadas/len(lista_horas)
    
    remain=tot_restante#continua con las horas que quedaron sin hacerse
    #prome es lo que se supone que debe avanzar en los dias restantes...meter eso en nueva_estimacion
    while(remain>=0):
        if(remain-prome>0):
            nueva_estimacion.append(remain-prome)
        else:
            nueva_estimacion.append(0)
        remain=remain-prome
    
    ncategorias= len(nueva_estimacion)
    catgria=[]
    for i in range(ncategorias):
        catgria.append(i)

    return render(request,'burndown2.html',{'categorias':catgria,'nuevaestima':nueva_estimacion,'suma':sumx,'estima':estimacion,'duracion':duracionsp,'horas':lista_horas,'fechas':lista_fechas,'restantes':horas_restantes,'cat_dias':cant_days,'sprint':sprint,'proyectoid':proyectoid,'usuarioid':usuario_id, 'rolid':rolid})

mod_vars = {
    'PDF_TITLE': 'Reporte General de su proyecto',
    'PDF_PROJECT': None,
}

def pdf_first_page(my_c, doc):
    """
    Adding title, header and footer to first page
    :param my_c: Canvas
    :param doc: SimpleDocTemplate
    :return: None
    """
    my_c.saveState()
    title = Paragraph(mod_vars['PDF_TITLE'], ParagraphStyle(
        'Heading1', fontSize=16, alignment=TA_CENTER))
    title.wrap(doc.width, 10*mm)
    title.drawOn(my_c, doc.leftMargin, doc.height + doc.bottomMargin - 5*mm)
    my_c.restoreState()
    pdf_header_and_footer(my_c, doc)


def pdf_later_pages(my_c, doc):
    """
    Adding header and footer to every page other than the first page
    :param my_c: Canvas
    :param doc: SimpleDocTemplate
    :return: None
    """
    pdf_header_and_footer(my_c, doc)


def pdf_header_and_footer(my_c, doc):
    """
    Auxiliary function that adds header and footer to pages
    :param my_c: Canvas
    :param doc: SimpleDocTemplate
    :return: None
    """
    my_c.saveState()

    # Header
    header = Paragraph("Consultora De Software - " + mod_vars['PDF_PROJECT'].nombre_largo, ParagraphStyle('Normal'))
    header.wrap(doc.width, doc.topMargin)
    header.drawOn(my_c, doc.leftMargin, doc.height + doc.bottomMargin + 3*mm)

    now1 = timezone.now()
    header = Paragraph('{} - {}'.format(now1.strftime('%d / %m / %Y'),
                       now1.strftime('%H:%M')),
                       ParagraphStyle('Normal', alignment=TA_RIGHT))
    header.wrap(doc.width, doc.topMargin)
    header.drawOn(my_c, doc.leftMargin, doc.height + doc.bottomMargin + 3*mm)
    my_c.line(60,773,540,773) # Para hacer una linea horizontal
    my_c.line(60,776,540,776) # Para hacer una linea horizontal

    # Footer
    footer = Paragraph('Página {}'.format(doc.page),
                       ParagraphStyle('Normal', alignment=TA_CENTER))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(my_c, doc.leftMargin, doc.bottomMargin - 5*mm)

    my_c.restoreState()
    
def make_pdf(proyecto, sprint):
    """
    Make the requested PDF report.
    :param proyecto:
    :param report_id:
    :param sprint: used in some reports
    :return: pdf and filename
    """
    # report does not exist
    filename = "reporte.pdf"
    mod_vars['PDF_TITLE'] = "Reporte General de su proyecto"
    mod_vars['PDF_PROJECT'] = proyecto
    p_style1 = ParagraphStyle('Normal')
    styles = getSampleStyleSheet()
    styleH = styles['Heading3']
    story = list()                      # list of flowables with the content
    story.append(Spacer(1, 15*mm))      # so to not override the title

    HUv=HU.objects.filter(proyecto=proyecto).filter(estado='ACT')
    HUv=sorted(HUv,key=lambda x: x.prioridad, reverse=True)
    
    us_set = HUv
    story.append(Paragraph("Informacion sobre su proyecto", styleH))
    story.append(Spacer(1, mm))
    # first add the table header
    table_col_widths = [65*mm, 65*mm]
    table_data = [
                  ['Nombre Corto', proyecto.nombre_corto],
                  ['Nombre Largo', proyecto.nombre_largo],
                  ['Descripcion', proyecto.descripcion],
                  ['Fecha de inicio', str(proyecto.fecha_inicio)[:10]],
                  ['Fecha de fin', str(proyecto.fecha_fin)[:10]],
                  ['Duracion total', proyecto.duracion],
                  ['Cantidad de dias transcurridos', proyecto.cantidad_dias_transcurridos],
                  ['Estado', proyecto.estado],
                  ]
    table_style1 = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.gainsboro),
        ])
    story.append(Table(table_data, colWidths=table_col_widths,
                           style=table_style1, repeatRows=1))
    story.append(Spacer(1, 5*mm))
    
    story.append(Paragraph("Sprints definidos en el proyecto: ", styleH))
    story.append(Spacer(1, mm))
    i=1
    flujos_utilizados=[]
    for s in Sprint.objects.filter(proyecto=proyecto):
        nombre= str(i)+". "+s.descripcion
        i=i+1
        story.append(Paragraph(nombre, styleH))
        story.append(Spacer(1, mm))
        # first add the table header
        flujos=""
        equipo=""
        for f in s.flujo.all():
            flujos=flujos + f.nombre + " - "
            flujos_utilizados.append(f)
        for u in s.equipo.all():
            equipo=equipo + u.username + " - "
        table_col_widths = [65*mm, 65*mm]
        table_data = [
                      ['Fecha de inicio', str(s.fecha_inicio)[:10]],
                      ['Duracion estimada', s.duracion],
                      ['Flujos utilizados', flujos],
                      ['Equipo a cargo', equipo],
                      ['Cantidad total de HU', str(len(s.hu.all()))],
                      ['Estado', s.estado],
                      ]
        table_style1 = TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('BACKGROUND', (0, 0), (0, -1), colors.gainsboro),
            ])
        story.append(Table(table_data, colWidths=table_col_widths,
                               style=table_style1, repeatRows=1))
        story.append(Spacer(1, 5*mm))
        
    story.append(Paragraph("Flujos utilizados en el proyecto: ", styleH))
    story.append(Spacer(1, 0.5*mm))
    i=1
    flujos_utilizados=set(flujos_utilizados) # eliminar repeticiones
    for f in flujos_utilizados:
        nombre= str(i)+". "+f.nombre + "- Actividades por las que pasan las HU"
        i=i+1
        story.append(Paragraph(nombre, styles['Heading4']))
        story.append(Spacer(1, mm))

        j=1
        jsonDec = json.decoder.JSONDecoder()
        orden=jsonDec.decode(f.orden_actividades)
        for a in orden:
            act= str(j)+". "+ Actividades.objects.get(id=a).nombre
            story.append(Paragraph(act, p_style1))
            story.append(Spacer(1, 0.2*mm))
            j=j+1
            
        story.append(Spacer(1, 5*mm))
    
    if not sprint:
        # if no sprint came as param, check if there is an active one
        sprint = Sprint.objects.filter(proyecto=proyecto).filter(estado="CON")

    if sprint:
        for s in sprint:
            # update the file name and PDF title
            filename = filename[:-6] + '{}'.format(s.descripcion)
            sprint_dsc = 'Sprint {} (estado: {})'.format(
                    s.descripcion, s.estado)
    else:
        sprint_dsc = 'No hay sprint desarrollandose'
            
    for s in sprint:
        for h in us_set:
            if h.sprint() != s:
                us_set.remove(h)
    story.append(Paragraph(sprint_dsc, styleH))
    story.append(Spacer(1, 5*mm))
    
    story.append(Paragraph("1. Cantidad de trabajos en curso por equipo", styles['Heading5']))
    story.append(Spacer(1, mm))
    if not sprint:
        story.append(Paragraph("No hay trabajos realizandose", p_style1))
        story.append(Spacer(1, 1*mm))
    equipo_hu={}
    for s in sprint:
        for h in s.hu.all():
            if equipo_hu.has_key(h.saber_usuario()):
                equipo_hu[h.saber_usuario()].append(h)
            else:
                equipo_hu[h.saber_usuario()]=[]
                equipo_hu[h.saber_usuario()].append(h)
    
    table_style1 = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.gainsboro),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
            ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
        ])
    
    if len(sprint) == 0:
        table_data.append(['', 'No hay historias de usuario para mostrar',
                               '', '', '','', '', ''])
    else:
        for usuario, hus in equipo_hu.items():
            table_col_widths = [10*mm, 20*mm, 15*mm, 15*mm, 20*mm, 20*mm, 30*mm, 20*mm]
            table_data = [[
                    '#',
                    'Descripción',
                    'Prioridad',
                    'Hs. trab.',
                    'Duracion',
                    'Flujo',
                    'Actividad',
                    'Estado',
            ], ]
            if usuario:
                story.append(Paragraph(" - " + usuario.username + " - Total de HUs a cargo: " + str(len(hus)), styles['Heading5']))
                story.append(Spacer(1, 0.5*mm))
            else:
                story.append(Paragraph(str(j)+". HUs No asignadas: - " + str(len(hus)) , styles['Heading5']))
                story.append(Spacer(1, 0.5*mm))
            for i, us in enumerate(hus):
                table_data.append([
                    i+1,
                    Paragraph(us.descripcion, p_style1),
                    us.prioridad,
                    us.acumulador_horas,
                    us.duracion,
                    us.flujo().nombre if us.flujo() else '',
                    us.actividad.nombre if us.actividad else '',
                    us.estado_en_actividad,
                    ])
            story.append(Table(table_data, colWidths=table_col_widths,
                           style=table_style1, repeatRows=1))

    story.append(Spacer(1, 5*mm))
    
    story.append(Paragraph("2.Cantidad de trabajos por usuario pendiente, en curso, finalizado", styles['Heading4']))
    story.append(Spacer(1, mm))
    table_col_widths = [10*mm, 20*mm, 15*mm, 15*mm, 20*mm, 20*mm,20*mm, 30*mm, 25*mm]
    estado_hu={}
    for h in HU.objects.filter(proyecto=proyecto).filter(estado='ACT'):
        if not estado_hu.has_key(h.estado_en_actividad):
            estado_hu[h.estado_en_actividad]=[]
        estado_hu[h.estado_en_actividad].append(h)
        
    for estado, hus in estado_hu.items():  
        i=1
        story.append(Paragraph("Estado: " + estado + " - Total de HUs: " + str(len(hus)), styles['Heading5']))
        story.append(Spacer(1, 0.5*mm))
        table_data = [[
                    '#',
                    'Descripción',
                    'Prioridad',
                    'Hs. trab.',
                    'Duracion',
                    'Sprint',
                    'Flujo',
                    'Actividad',
                    'Estado',
        ], ]
        for us in hus:
            table_data.append([
                    i,
                    Paragraph(us.descripcion, p_style1),
                    us.prioridad,
                    us.acumulador_horas,
                    us.duracion,
                    us.sprint().descripcion if us.sprint() else ' - ',
                    us.flujo().nombre if us.flujo() else ' - ',
                    us.actividad.nombre if us.actividad else ' - ',
                    us.estado_en_actividad,
                    ])
            i=i+1
        story.append(Table(table_data, colWidths=table_col_widths,
                    style=table_style1, repeatRows=1))
        story.append(Spacer(1, 1*mm))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("3. Lista clasificada por orden de prioridad de las actividades para completar un proyecto.", styles['Heading4']))
    story.append(Spacer(1, mm))
    table_col_widths = [10*mm, 20*mm, 15*mm, 15*mm, 20*mm, 20*mm,20*mm, 30*mm, 25*mm]
    table_data = [[
                    '#',
                    'Descripción',
                    'Prioridad',
                    'Hs. trab.',
                    'Duracion',
                    'Sprint',
                    'Flujo',
                    'Actividad',
                    'Estado',
        ], ]
    i=1
    HUv=HU.objects.filter(proyecto=proyecto).filter(estado='ACT')
    HUv=sorted(HUv,key=lambda x: x.prioridad, reverse=True)
    for us in HUv:
        table_data.append([
                    i,
                    Paragraph(us.descripcion, p_style1),
                    us.prioridad,
                    us.acumulador_horas,
                    us.duracion,
                    us.sprint().descripcion if us.sprint() else ' - ',
                    us.flujo().nombre if us.flujo() else ' - ',
                    us.actividad.nombre if us.actividad else ' - ',
                    us.estado_en_actividad,
                    ])
        i=i+1
    story.append(Table(table_data, colWidths=table_col_widths,
                    style=table_style1, repeatRows=1))
    story.append(Spacer(1, 15*mm))
    
    story.append(Paragraph("4. Lista de Tiempo estimado por proyecto y la ejecución del mismo", styles['Heading4']))
    story.append(Spacer(1, 5*mm))
    if not sprint:
        story.append(Paragraph("No hay trabajos realizandose", p_style1))
        story.append(Spacer(1, 1*mm))
    for s in sprint:
        x_max, ideal_burndown, remaining_hours = s.get_BurdownChart()
        drawing = Drawing(150*mm, 100*mm)
        lc = HorizontalLineChart()
        lc.width = drawing.width
        lc.height = drawing.height
        lc.data = [ideal_burndown, remaining_hours]
        lc.categoryAxis.categoryNames = []
        for i in range(max(len(ideal_burndown), len(remaining_hours))):
            lc.categoryAxis.categoryNames.append(str(i+1))
        lc.categoryAxis.labels.boxAnchor = 'w'
        lc.valueAxis.valueMin = 0
        lc.valueAxis.valueMax = x_max
        lc.valueAxis.valueStep = round((lc.valueAxis.valueMax - lc.valueAxis.valueMin)/10)
        lc.lines[0].strokeWidth = 2
        lc.lines[1].strokeWidth = 1.5
        drawing.add(lc)
        story.append(drawing)
        story.append(Spacer(1, 5*mm))
        
    story.append(Paragraph("5. El backlog del Producto, lista ordenada de HU, en orden que esperamos deben terminarse", styles['Heading4']))
    story.append(Spacer(1, 5*mm))
    
    huss=HU.objects.all().filter(proyecto=proyecto).filter(estado='ACT').filter(valido=True).filter(sprint__hu__isnull=True)
    huss=sorted(huss,key=lambda x: x.prioridad, reverse=True)
    if not huss:
        story.append(Paragraph("No hay trabajos pendientes de realizacion", p_style1))
        story.append(Spacer(1, 1*mm))
    table_data = [[
                    '#',
                    'Descripción',
                    'Prioridad',
                    'Hs. trab.',
                    'Duracion',
                    'Sprint',
                    'Flujo',
                    'Actividad',
                    'Estado',
        ], ]
    i=1
    for us in huss:
        table_data.append([
                    i,
                    Paragraph(us.descripcion, p_style1),
                    us.prioridad,
                    us.acumulador_horas,
                    us.duracion,
                    us.sprint().descripcion if us.sprint() else ' - ',
                    us.flujo().nombre if us.flujo() else ' - ',
                    us.actividad.nombre if us.actividad else ' - ',
                    us.estado_en_actividad,
                    ])
        i=i+1
    story.append(Table(table_data, colWidths=table_col_widths,
                    style=table_style1, repeatRows=1))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("HUs Pendientes de sprints anteriores", styles['Heading5']))
    story.append(Spacer(1, 2*mm))
    #las pendientes de sprints anteriores
    HUs_pendientes=[]
    for x in Sprint.objects.filter(proyecto=proyecto):
        if x.estado == 'FIN':
            for h in x.hu.all():
                if h.estado_en_actividad != 'APR':
                    HUs_pendientes.append(h)
    for x in Sprint.objects.filter(proyecto=proyecto):
        if x.estado != 'FIN':
            for h in x.hu.all():
                for hp in HUs_pendientes:
                    if h == hp:
                        HUs_pendientes.remove(h)
    
    if not huss:
        story.append(Paragraph("No hay trabajos que quedaron pendientes en sprints anteriores", p_style1))
        story.append(Spacer(1, 1*mm))
    table_data = [[
                    '#',
                    'Descripción',
                    'Prioridad',
                    'Hs. trab.',
                    'Duracion',
                    'Sprint',
                    'Flujo',
                    'Actividad',
                    'Estado',
        ], ]
    i=1
    for us in HUs_pendientes:
        table_data.append([
                    i,
                    Paragraph(us.descripcion, p_style1),
                    us.prioridad,
                    us.acumulador_horas,
                    us.duracion,
                    us.sprint().descripcion if us.sprint() else ' - ',
                    us.flujo().nombre if us.flujo() else ' - ',
                    us.actividad.nombre if us.actividad else ' - ',
                    us.estado_en_actividad,
                    ])
        i=i+1
    story.append(Table(table_data, colWidths=table_col_widths,
                    style=table_style1, repeatRows=1))
    story.append(Spacer(1, 5*mm))
                      
    story.append(Paragraph("6. El Backlog del Sprint, lista de los elementos del Backlog del Producto, elegidos para ser desarrollados en el Sprint actual", styles['Heading4']))
    story.append(Spacer(1, 2*mm))
    if not sprint:
        story.append(Paragraph("No hay sprint desarrollandose", p_style1))
        story.append(Spacer(1, 1*mm))
    for s in sprint: # sprint MODO CONSULTA
        table_data = [[
                    '#',
                    'Descripción',
                    'Prioridad',
                    'Hs. trab.',
                    'Duracion',
                    'Usuario',
                    'Flujo',
                    'Actividad',
                    'Estado',
        ], ]
        i=1
        for us in s.hu.all():
            table_data.append([
                        i,
                        Paragraph(us.descripcion, p_style1),
                        us.prioridad,
                        us.acumulador_horas,
                        us.duracion,
                        us.saber_usuario().username if us.saber_usuario() else ' - ',
                        us.flujo().nombre if us.flujo() else ' - ',
                        us.actividad.nombre if us.actividad else ' - ',
                        us.estado_en_actividad,
                        ])
            i=i+1
        story.append(Table(table_data, colWidths=table_col_widths,
                        style=table_style1, repeatRows=1))

    # create PDF from list of flowables, using a temp buffer to assemble PDF
    a_buffer = BytesIO()
    doc = SimpleDocTemplate(a_buffer, pagesize=A4)
    doc.build(story, onFirstPage=pdf_first_page, onLaterPages=pdf_later_pages)
    pdf = a_buffer.getvalue()
    a_buffer.close()
    return pdf, filename

@login_required()
def reporte_view(request, proyectoid, report_id, sprint_id=None):
    """
    Displays the PDF of the requested report.
    :param request: HttpRequest
    :param proyectoid: ID of the requested project
    :param report_id: ID of the requested report
    :param sprint_id: (optional)
    :return: HttpResponse
    """
    proyectox = proyecto.objects.get(id=proyectoid)
    if sprint_id:
        sprint = Sprint.objects.get(id=sprint_id)
    else:
        sprint = None

    pdf, filename = make_pdf(proyectox, sprint)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="{}.pdf"'.format(filename)
    response.write(pdf)
    return response

def anularProyecto(request,usuario_id,proyectoid):
    if request.method=='GET' :
        return render(request,'anularProyecto.html',{'usuarioid':usuario_id,'proyectoid':proyectoid})
    else:
        proyectox=proyecto.objects.get(id=proyectoid)
        usuario_e=MyUser.objects.get(id=usuario_id)
        descripcion=request.POST['descripcion']
        evento_e=usuario_id+"+"+proyectoid+"+SCRUM+"+"PROYECTO+"+"A+"+"Se ha anulado el proyecto: '"+proyectox.nombre_corto+"' por el siguiente motivo: '"+descripcion+"' con fecha y hora: "+str(timezone.now())
        email_e=str(usuario_e.email)
        historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=proyectox.nombre_corto,  evento=evento_e)
        if usuario_e.frecuencia_notificaciones == 'instante':
            send_email(email_e, 'Notificacion', evento_e)
        proyectox.fecha_fin=timezone.now()
        proyectox.estado='ANU'
        proyectox.save()
        return HttpResponseRedirect('/hola/')
    
def finalizarProyecto(request,usuario_id,proyectoid,rol_id):
    if request.method=='GET' :
        return render(request,'finalizarProyecto.html',{'usuarioid':usuario_id,'proyectoid':proyectoid,'rolid':rol_id})
    else:
        proyectox=proyecto.objects.get(id=proyectoid)
        usuario_e=MyUser.objects.get(id=usuario_id)
        descripcion=request.POST['descripcion']
        evento_e=usuario_id+"+"+proyectoid+"+SCRUM+"+"PROYECTO+"+"F+"+"Se ha finalizado el proyecto: '"+proyectox.nombre_corto+"' por el siguiente motivo: '"+descripcion+"' con fecha y hora: "+str(timezone.now())
        email_e=str(usuario_e.email)
        historial_notificacion.objects.create(usuario=usuario_e, fecha_hora=timezone.now(), objeto=proyectox.nombre_corto,  evento=evento_e)
        if usuario_e.frecuencia_notificaciones == 'instante':
            send_email(str(email_e), 'Notificacion', evento_e)
        proyectox.estado='FIN'
        proyectox.fecha_fin=timezone.now()
        proyectox.save()
        return HttpResponseRedirect('/hola/')