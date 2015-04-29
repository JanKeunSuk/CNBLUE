#coding: utf-8
import django
django.setup()
from datetime import datetime
#from django.db import models

from gestor.models import Permitido, MyUser, HU, proyecto,rol_sistema, rol, asigna_sistema,asignacion, Actividades,Flujo,delegacion,Sprint, HU_descripcion

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

"""Creacion de correos electronicos asociados a usuarios"""
perm4=Permitido.objects.create(email='gsebacatt@gmail.com')
perm3=Permitido.objects.create(email='katherine@gmail.com')
perm2=Permitido.objects.create(email='desly@gmail.com')
perm1=Permitido.objects.create(email='admin@gmail.com')
perm5=Permitido.objects.create(email='valeria@gmail.com')


"""Creacion de usuarios usando los email permitidos creados anteriormente"""
admin=MyUser.objects.create(password='pbkdf2_sha256$15000$5PUgdTbag7Cm$kbLmrEL+pT+iWKraH4+8Kq6aVL9bA5wDHkFFYiRlogI=',username='admin',user_name='Administrador',last_name='Administrador',direccion='Padre Cardozo',is_active=True,is_admin=True,email=perm1)
kathe=scrum1=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='katherine',user_name='Katherine',last_name='Vera',direccion='Lambare',is_active=True,is_admin=False,email=perm3)
delsy=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='desly',user_name='Delsy',last_name='Denis',direccion='San Lorenzo',is_active=True,is_admin=False,email=perm2)
sebas=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='sebas',user_name='Sebastian',last_name='Cattaneo',direccion='Asuncion',is_active=True,is_admin=False,email=perm4)
valeria=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='valeria',user_name='Valeria',last_name='Valeria',direccion='Asuncion',is_active=True,is_admin=False,email=perm5)

"""Creacion de permisos que faltan"""
content_type = ContentType.objects.get_for_model(HU)
permission1 = Permission.objects.create(codename='agregar horas trabajadas',
                                       name='Agregar horas trabajadas',
                                       content_type=content_type)
permission2 = Permission.objects.create(codename='cambiar hu nivel Scrum',
                                       name='Can change hu nivel Scrum',
                                       content_type=content_type)
content_type2 = ContentType.objects.get_for_model(proyecto)
permission3 = Permission.objects.create(codename='Visualizar proyecto',
                                       name='Visualizar proyecto',
                                       content_type=content_type2)
permission4 = Permission.objects.create(codename='Visualizar equipo',
                                       name='Visualizar equipo',
                                       content_type=content_type2)
permission5 = Permission.objects.create(codename='Visualizar HU',
                                       name='Visualizar HU',
                                       content_type=content_type)


"""Creacion de proyectos precargados"""
p1=proyecto.objects.create(nombre_corto='p1',nombre_largo='proyecto1',descripcion='proyecto1',fecha_inicio=str(datetime.now()),fecha_fin=str(str(datetime.now())),estado='PEN')
p2=proyecto.objects.create(nombre_corto='p2',nombre_largo='proyecto2',descripcion='proyecto2',fecha_inicio=str(datetime.now()),fecha_fin=str(str(datetime.now())),estado='PEN')
p3=proyecto.objects.create(nombre_corto='p3',nombre_largo='proyecto3',descripcion='proyecto3',fecha_inicio=str(datetime.now()),fecha_fin=str(str(datetime.now())),estado='PEN')
p4=proyecto.objects.create(nombre_corto='p4',nombre_largo='proyecto4',descripcion='proyecto4',fecha_inicio=str(datetime.now()),fecha_fin=str(str(datetime.now())),estado='PEN')


"""Creacion de rol admin y relacionamiento a todos los permisos existentes"""

rol_admin=rol_sistema.objects.create(nombre_rol_id='admin',descripcion='admin tiene todos los permisos')


"""Creacion de roles predefinidos a nivel proyecto Scrum,Owner, etc, y uno hecho por un Scrum para probar que tal"""
rol_scrum=rol.objects.create(nombre_rol_id='Scrum Master',descripcion='Permisos adquiridos por el ScrumMaster',usuario_creador=admin,estado='ACT')
rol_owner=rol.objects.create(nombre_rol_id='Product Owner',descripcion='Permisos adquiridos por el Product Owner',usuario_creador=admin,estado='ACT')
rol_equipo=rol.objects.create(nombre_rol_id='Equipo',descripcion='Permisos adquiridos por el Equipo',usuario_creador=admin,estado='ACT')
rol_cliente=rol.objects.create(nombre_rol_id='Cliente',descripcion='Permisos adquiridos por el Cliente',usuario_creador=admin,estado='ACT')
rol_deScrum=rol.objects.create(nombre_rol_id='Rol creado por Scrum',descripcion='Permisos designados por el Scrum',usuario_creador=scrum1,estado='ACT')
#en uno de los proyectos katherine(scrum1) va a ser usuario creadory ella podra ver este rol como suyo(modificable)

"""Ahora se cargaran permisos a cada uno de esos roles predefinidos"""
"""Carga para el Scrum Master"""
"""Administracion de rol"""
per_add_rol=Permission.objects.get(name='Can add rol')
per_change_rol=Permission.objects.get(name='Can change rol')
per_delete_rol=Permission.objects.get(name='Can delete rol')

"""Administracion de actividades"""
per_add_act=Permission.objects.get(name='Can add actividades')
per_change_act=Permission.objects.get(name='Can change actividades')
per_delete_act=Permission.objects.get(name='Can delete actividades')


"""Administracion de flujo"""
per_add_flujo=Permission.objects.get(name='Can add flujo')
per_change_flujo=Permission.objects.get(name='Can change flujo')
per_delete_flujo=Permission.objects.get(name='Can delete flujo')


"""Modificacion de proyecto"""
per_change_proyecto=Permission.objects.get(name='Can change proyecto')

"""Administracion de Sprint"""
per_add_sprint=Permission.objects.get(name='Can add sprint')
per_change_sprint=Permission.objects.get(name='Can change sprint')
per_delete_sprint=Permission.objects.get(name='Can delete sprint')


"""Administracion de asignacion"""
per_add_asigna=Permission.objects.get(name='Can add asignacion')
per_change_asigna=Permission.objects.get(name='Can change asignacion')
per_delete_asigna=Permission.objects.get(name='Can delete asignacion')


"""Administracion de delegacion"""
per_add_delega=Permission.objects.get(name='Can add delegacion')
per_change_delega=Permission.objects.get(name='Can change delegacion')
per_delete_delega=Permission.objects.get(name='Can delete delegacion')

"""Administracion asigna hu actividad flujo"""
per_add_asignahu=Permission.objects.get(name='Can add asigna h u_actividad_flujo')
per_change_asignahu=Permission.objects.get(name='Can change asigna h u_actividad_flujo')
per_delete_asignahu=Permission.objects.get(name='Can delete asigna h u_actividad_flujo')

"""Modificacion de hu nivel scrum"""
per_change_hu_scrum=Permission.objects.get(name='Can change hu nivel Scrum')


"""MOMENTO DE LA ASIGNACION DE TODO LO ANTERIOR AL SCRUM"""
rol_scrum.permisos.add(per_add_rol,per_change_rol,per_delete_rol,per_add_act,per_change_act,per_delete_act)
rol_scrum.permisos.add(per_add_flujo,per_change_flujo,per_delete_flujo,per_change_proyecto,per_add_sprint,per_change_sprint,per_delete_sprint)
rol_scrum.permisos.add(per_add_asigna,per_delete_asigna,per_change_asigna,per_add_delega,per_change_delega,per_delete_delega,per_change_hu_scrum)
rol_scrum.permisos.add(per_add_asignahu,per_change_asignahu,per_delete_asignahu)





"""Carga para el Product Owner"""
"""Voy a usar los permisos  ya cargados  y obtener los nuevos que se necesiten, lo mismo para los demas roles"""


per_add_hu=Permission.objects.get(name='Can add hu')
per_change_hu=Permission.objects.get(name='Can change hu')
per_delete_hu=Permission.objects.get(name='Can delete hu')

"""Y aca le asigno solamente esos 3 ultimos permisos obtenidos"""
rol_owner.permisos.add(per_add_hu,per_change_hu,per_delete_hu)


"""Carga para el Equipo"""
rol_equipo.permisos.add(permission1) # se cargo y se obtuvo en la linea 24


"""Carga para el Cliente"""
"""Se le asigna visualizar proyecto, visualizar equipo y visualiazr hu que ya se obtuvieron en lineas 31,34,37"""
rol_cliente.permisos.add(permission3,permission4,permission5)



"""Ahora se le asigna todo al admin(devalde ya que el se va al sistema ADMIN)"""
#rol_admin.permisos.add()


"""Ahora tengo que asignarle el rol_sistema admin al usuario de username admin"""
asigna_sistema.objects.create(usuario=admin,rol=rol_admin)

"""Ahora a los otros usuarios tengo que asignarles los otros roles de proyecto en un proyecto particular"""
asignacion.objects.create(usuario=delsy,rol=rol_scrum,proyecto=p1)
asignacion.objects.create(usuario=kathe,rol=rol_owner,proyecto=p1)
asignacion.objects.create(usuario=sebas,rol=rol_equipo,proyecto=p1)
asignacion.objects.create(usuario=valeria,rol=rol_cliente,proyecto=p1)
asignacion.objects.create(usuario=sebas,rol=rol_scrum,proyecto=p2)
asignacion.objects.create(usuario=kathe,rol=rol_equipo,proyecto=p2)
asignacion.objects.create(usuario=kathe,rol=rol_scrum,proyecto=p3)
asignacion.objects.create(usuario=sebas,rol=rol_owner,proyecto=p3)
asignacion.objects.create(usuario=delsy,rol=rol_equipo,proyecto=p3)


"""Creacion de actividades"""
act1=Actividades.objects.create(nombre='Analisis',descripcion='analisis')
act2=Actividades.objects.create(nombre='Diseño',descripcion='diseño')
act3=Actividades.objects.create(nombre='Despliegue',descripcion='Despliegue')
act4=Actividades.objects.create(nombre='Desarrollo',descripcion='desarrollo')
act5=Actividades.objects.create(nombre='Prueba',descripcion='prueba')

"""Cargar los primeros flujos"""
f1=Flujo.objects.create(nombre='Flujo1',estado='ACT',orden_actividades='[1,3,4]')
f2=Flujo.objects.create(nombre='Flujo2',estado='ACT',orden_actividades='[5,4,3,1]')
f3=Flujo.objects.create(nombre='Flujo3',estado='ACT',orden_actividades='[1,2,5]')


"""Cargar las actividades del flujo1"""
f1.actividades.add(act1,act3,act4)

"""Cargar las actividades del flujo2"""
f2.actividades.add(act5,act4,act3,act1)


"""Cargar las actividades del flujo3"""
f3.actividades.add(act1,act2,act5)



"""Creacion de HU"""
hu1=HU.objects.create(descripcion='HU1',valor_negocio=3,valor_tecnico=5,prioridad=5,duracion=5,acumulador_horas=4,estado='ACT',estado_en_actividad='ACT',valido=True,proyecto=p1)

hu2=HU.objects.create(descripcion='HU2',valor_negocio=5,valor_tecnico=7,prioridad=5,duracion=9,acumulador_horas=4,estado='ACT',estado_en_actividad='ACT',valido=True,proyecto=p1)

hu3=HU.objects.create(descripcion='HU3',valor_negocio=8,valor_tecnico=6,prioridad=3,duracion=8,acumulador_horas=4,estado='ACT',estado_en_actividad='ACT',valido=True,proyecto=p1)

hu4=HU.objects.create(descripcion='HU4',valor_negocio=8,valor_tecnico=0,prioridad=0,duracion=0,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=False,proyecto=p2)


"""Delegacion de HU a un usuario"""
delegacion.objects.create(usuario=sebas,hu=hu1)
delegacion.objects.create(usuario=sebas,hu=hu2)
delegacion.objects.create(usuario=sebas,hu=hu3)



"""Creacion de un Sprint"""
sp1=Sprint.objects.create(descripcion='sprint1',fecha_inicio=str(datetime.now()),duracion=2,estado='ACT',proyecto=p1)
sp2=Sprint.objects.create(descripcion='sprint2',fecha_inicio=str(datetime.now()),duracion=2,estado='ACT',proyecto=p1)
sp3=Sprint.objects.create(descripcion='sprint3',fecha_inicio=str(datetime.now()),duracion=2,estado='ACT',proyecto=p1)

"""Agregar hus a los sprint creados"""
sp1.hu.add(hu1,hu2,hu3)


"""Creacion de descripciones de hu para posterior asociacion con una HU"""
dhu1=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.now()))
dhu2=HU_descripcion.objects.create(horas_trabajadas=1,descripcion_horas_trabajadas='Tarea2',fecha=str(datetime.now()))
dhu3=HU_descripcion.objects.create(horas_trabajadas=1,descripcion_horas_trabajadas='Tarea3',fecha=str(datetime.now()))
dhu4=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.now()))
dhu5=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea2',fecha=str(datetime.now()))
dhu6=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.now()))
dhu7=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea2',fecha=str(datetime.now()))

"""Asociar la hu con una descripcion"""
hu1.hu_descripcion.add(dhu1)
hu1.hu_descripcion.add(dhu2)
hu1.hu_descripcion.add(dhu3)
hu2.hu_descripcion.add(dhu4)
hu2.hu_descripcion.add(dhu5)
hu3.hu_descripcion.add(dhu6)
hu3.hu_descripcion.add(dhu7)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           































