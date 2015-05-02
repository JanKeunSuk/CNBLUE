#coding: utf-8
import django
django.setup()
import datetime

#from django.db import models

from gestor.models import Permitido, MyUser, HU, proyecto,rol_sistema, rol, asigna_sistema,asignacion, Actividades,Flujo,delegacion,Sprint, HU_descripcion,asignaHU_actividad_flujo

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

"""Creacion de correos electronicos asociados a usuarios"""
perm4=Permitido.objects.create(email='gsebacatt@gmail.com')
perm3=Permitido.objects.create(email='katherine@gmail.com')
perm2=Permitido.objects.create(email='desly@gmail.com')
perm1=Permitido.objects.create(email='admin@gmail.com')
perm5=Permitido.objects.create(email='gabriela@gmail.com')
perm6=Permitido.objects.create(email='vanessa@gmail.com')
perm7=Permitido.objects.create(email='valeria@gmail.com')

"""Creacion de usuarios usando los email permitidos creados anteriormente"""
admin=MyUser.objects.create(password='pbkdf2_sha256$15000$5PUgdTbag7Cm$kbLmrEL+pT+iWKraH4+8Kq6aVL9bA5wDHkFFYiRlogI=',username='admin',user_name='Administrador',last_name='Administrador',direccion='Padre Cardozo',is_active=True,is_admin=True,email=perm1)
kathe=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='katherine',user_name='Katherine',last_name='Vera',direccion='Lambare',is_active=True,is_admin=False,email=perm3)
delsy=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='delsy',user_name='Delsy',last_name='Denis',direccion='San Lorenzo',is_active=True,is_admin=False,email=perm2)
sebas=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='sebas',user_name='Sebastian',last_name='Cattaneo',direccion='Asuncion',is_active=True,is_admin=False,email=perm4)
gabriela=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='gabriela',user_name='Gabriela',last_name='Gabriela',direccion='Lambare',is_active=True,is_admin=False,email=perm5)
vanessa=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='vanessa',user_name='Vanessa',last_name='Vanessa',direccion='Lambare',is_active=True,is_admin=False,email=perm6)
valeria=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='valeria',user_name='Valeria',last_name='Valeria',direccion='Lambare',is_active=True,is_admin=False,email=perm7)

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
p1=proyecto.objects.create(nombre_corto='p1',nombre_largo='proyecto1',descripcion='proyecto1',fecha_inicio=str(datetime.date.today()),fecha_fin=str(str(datetime.date.today())),estado='PEN')
p2=proyecto.objects.create(nombre_corto='p2',nombre_largo='proyecto2',descripcion='proyecto2',fecha_inicio=str(datetime.date.today()),fecha_fin=str(str(datetime.date.today())),estado='PEN')
p3=proyecto.objects.create(nombre_corto='p3',nombre_largo='proyecto3',descripcion='proyecto3',fecha_inicio=str(datetime.date.today()),fecha_fin=str(str(datetime.date.today())),estado='PEN')
p4=proyecto.objects.create(nombre_corto='p4',nombre_largo='proyecto4',descripcion='proyecto4',fecha_inicio=str(datetime.date.today()),fecha_fin=str(str(datetime.date.today())),estado='PEN')


"""Creacion de rol admin y relacionamiento a todos los permisos existentes"""

rol_admin=rol_sistema.objects.create(nombre_rol_id='admin',descripcion='admin tiene todos los permisos')


"""Creacion de roles predefinidos a nivel proyecto Scrum,Owner, etc, y uno hecho por un Scrum para probar que tal"""
rol_scrum=rol.objects.create(nombre_rol_id='Scrum Master',descripcion='Permisos adquiridos por el ScrumMaster',usuario_creador=admin,estado='ACT')
rol_owner=rol.objects.create(nombre_rol_id='Product Owner',descripcion='Permisos adquiridos por el Product Owner',usuario_creador=admin,estado='ACT')
rol_equipo=rol.objects.create(nombre_rol_id='Equipo',descripcion='Permisos adquiridos por el Equipo',usuario_creador=admin,estado='ACT')
rol_cliente=rol.objects.create(nombre_rol_id='Cliente',descripcion='Permisos adquiridos por el Cliente',usuario_creador=admin,estado='ACT')
rol_deScrum=rol.objects.create(nombre_rol_id='Rol creado por Scrum',descripcion='Permisos designados por el Scrum',usuario_creador=delsy,estado='ACT')
#en uno de los proyectos delsy(scrum1) va a ser usuario creador y ella podra ver este rol como suyo(modificable)

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
asignacion.objects.create(usuario=delsy,rol=rol_scrum,proyecto=p1) #Scrum
asignacion.objects.create(usuario=kathe,rol=rol_owner,proyecto=p1) #Product Owner
asignacion.objects.create(usuario=sebas,rol=rol_equipo,proyecto=p1) #Equipo
asignacion.objects.create(usuario=gabriela,rol=rol_equipo,proyecto=p1) #Equipo
asignacion.objects.create(usuario=vanessa,rol=rol_equipo,proyecto=p1) #Equipo
asignacion.objects.create(usuario=valeria,rol=rol_cliente,proyecto=p1) #Cliente
asignacion.objects.create(usuario=sebas,rol=rol_scrum,proyecto=p2)
asignacion.objects.create(usuario=kathe,rol=rol_equipo,proyecto=p2)
asignacion.objects.create(usuario=kathe,rol=rol_scrum,proyecto=p3)
asignacion.objects.create(usuario=sebas,rol=rol_owner,proyecto=p3)
asignacion.objects.create(usuario=delsy,rol=rol_equipo,proyecto=p3)


"""Creacion de actividades para el flujo 1"""
act1=Actividades.objects.create(nombre='Analisis',descripcion='analisis')
act2=Actividades.objects.create(nombre='Diseño',descripcion='diseño')
act3=Actividades.objects.create(nombre='Despliegue',descripcion='Despliegue')
act4=Actividades.objects.create(nombre='Desarrollo',descripcion='desarrollo')
act5=Actividades.objects.create(nombre='Prueba',descripcion='prueba')

"""Creacion de actividades para el flujo 2"""
act6=Actividades.objects.create(nombre='Relevamiento',descripcion='relevamiento')
act7=Actividades.objects.create(nombre='Implementacion',descripcion='implementacion')
act8=Actividades.objects.create(nombre='Control',descripcion='control de tareas')


"""Cargar los primeros flujos"""
f1=Flujo.objects.create(nombre='Flujo1',estado='ACT',orden_actividades='[1,2,3,4,5]')
f2=Flujo.objects.create(nombre='Flujo2',estado='ACT',orden_actividades='[6,7,8]')
#Flujo 3, una combinacion de los flujos anteriores
f3=Flujo.objects.create(nombre='Flujo3',estado='ACT',orden_actividades='[6,2,4,8]')


"""Cargar las actividades del flujo1"""
f1.actividades.add(act1,act2,act3,act4,act5)

"""Cargar las actividades del flujo2"""
f2.actividades.add(act6,act7,act8)


"""Cargar las actividades del flujo3"""
f3.actividades.add(act6,act2,act4,act8)


"""Creacion de HU"""
hu1=HU.objects.create(descripcion='HU1',valor_negocio=3,valor_tecnico=5,prioridad=95,duracion=15,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1)

hu2=HU.objects.create(descripcion='HU2',valor_negocio=5,valor_tecnico=7,prioridad=90,duracion=5,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1)

hu3=HU.objects.create(descripcion='HU3',valor_negocio=8,valor_tecnico=6,prioridad=85,duracion=20,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1)

hu4=HU.objects.create(descripcion='HU4',valor_negocio=2,valor_tecnico=5,prioridad=80,duracion=8,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1)

hu5=HU.objects.create(descripcion='HU5',valor_negocio=9,valor_tecnico=7,prioridad=75,duracion=5,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1)

hu6=HU.objects.create(descripcion='HU6',valor_negocio=8,valor_tecnico=6,prioridad=70,duracion=20,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1)

hu7=HU.objects.create(descripcion='HU7',valor_negocio=10,valor_tecnico=4,prioridad=68,duracion=30,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1)

hu8=HU.objects.create(descripcion='HU8',valor_negocio=5,valor_tecnico=7,prioridad=60,duracion=5,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1)

hu9=HU.objects.create(descripcion='HU9',valor_negocio=8,valor_tecnico=6,prioridad=45,duracion=20,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1)

hu10=HU.objects.create(descripcion='HU10',valor_negocio=2,valor_tecnico=5,prioridad=40,duracion=8,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1)

hu11=HU.objects.create(descripcion='HU11',valor_negocio=9,valor_tecnico=7,prioridad=35,duracion=5,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1)

hu12=HU.objects.create(descripcion='HU12',valor_negocio=10,valor_tecnico=0,prioridad=0,duracion=0,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=False,proyecto=p1)


"""Creacion de un Sprint"""
sp1=Sprint.objects.create(descripcion='sprint1',fecha_inicio=str(datetime.date.today()),duracion=10,estado='ACT',proyecto=p1)
sp2=Sprint.objects.create(descripcion='sprint2',fecha_inicio=str(datetime.date.today()),duracion=0,estado='ACT',proyecto=p1)
sp3=Sprint.objects.create(descripcion='sprint3',fecha_inicio=str(datetime.date.today()),duracion=0,estado='ACT',proyecto=p1)

"""Agregar hus a los sprint creados"""
sp1.hu.add(hu1,hu2,hu3,hu4,hu5,hu6,hu7,hu8)

"""Agregar hus a los sprint creados"""
sp1.flujo.add(f1,f2)

"""Clasificar esas hus seleccionadas en flujos"""
#hu1 y hu2 estan en el flujo 1
hu1Flujo1=asignaHU_actividad_flujo.objects.create(flujo_al_que_pertenece=f1)
hu1Flujo1.lista_de_HU.add(hu1,hu2,hu3,hu4,hu5)
#hu3 esta en el flujo 2
hu3flujo2=asignaHU_actividad_flujo.objects.create(flujo_al_que_pertenece=f2)
hu3flujo2.lista_de_HU.add(hu6,hu7,hu8)

"""
Agregar las actividades iniciales de las hu de acuerdo al flujo que fueron designados
"""
hu1.actividad=act1
hu1.save()

hu2.actividad=act1
hu2.save()

hu3.actividad=act1
hu3.save()

hu4.actividad=act1
hu4.save()

hu5.actividad=act1
hu5.save()

hu6.actividad=act6
hu6.save()

hu7.actividad=act6
hu7.save()

hu8.actividad=act6
hu8.save()

"""Delegacion de HU a un usuario"""
delegacion.objects.create(usuario=sebas,hu=hu1)
delegacion.objects.create(usuario=sebas,hu=hu2)
delegacion.objects.create(usuario=sebas,hu=hu3)
delegacion.objects.create(usuario=sebas,hu=hu4)
delegacion.objects.create(usuario=sebas,hu=hu5)

delegacion.objects.create(usuario=gabriela,hu=hu6)
delegacion.objects.create(usuario=gabriela,hu=hu7)
delegacion.objects.create(usuario=gabriela,hu=hu8)

"""Creacion de descripciones para la HU1 Mensaje Finalizada a Tiempo"""
dhu1=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Analisis",estado='PRO')
dhu2=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea2',fecha=str(datetime.date.today()),actividad="Analisis",estado='FIN')
dhu3=HU_descripcion.objects.create(horas_trabajadas=4,descripcion_horas_trabajadas='Tarea3',fecha=str(datetime.date.today() + datetime.timedelta(1)),actividad="Diseño",estado='PRO')
dhu4=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea4',fecha=str(datetime.date.today() + datetime.timedelta(2)),actividad="Diseño",estado='FIN')
dhu5=HU_descripcion.objects.create(horas_trabajadas=0.2,descripcion_horas_trabajadas='Tarea5',fecha=str(datetime.date.today() + datetime.timedelta(3)),actividad="Despliegue",estado='FIN')
dhu6=HU_descripcion.objects.create(horas_trabajadas=1.8,descripcion_horas_trabajadas='Tarea6',fecha=str(datetime.date.today() + datetime.timedelta(4)),actividad="Desarrollo",estado='FIN')
dhu7=HU_descripcion.objects.create(horas_trabajadas=1,descripcion_horas_trabajadas='Tarea7',fecha=str(datetime.date.today() + datetime.timedelta(5)),actividad="Prueba",estado='FIN')

"""Asociar la hu con una descripcion para HU1"""
hu1.hu_descripcion.add(dhu1)
hu1.hu_descripcion.add(dhu2)
hu1.hu_descripcion.add(dhu3)
hu1.hu_descripcion.add(dhu4)
hu1.hu_descripcion.add(dhu5)
hu1.hu_descripcion.add(dhu6)
hu1.hu_descripcion.add(dhu7)

"""Coloco en los campos estado y actividad de la HU a la que cargamos las descripciones los datos correctos segun la descripcion agregada"""
hu1.estado_en_actividad='FIN'
hu1.actividad=act5
hu1.acumulador_horas=15
hu1.save()

"""Creacion de descripciones para la HU2 Mensaje No finalizo. Contactar con Scrum"""
dhu1=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Analisis",estado='PRO')
dhu2=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea2',fecha=str(datetime.date.today() + datetime.timedelta(2)),actividad="Analisis",estado='FIN')
dhu3=HU_descripcion.objects.create(horas_trabajadas=1,descripcion_horas_trabajadas='Tarea3',fecha=str(datetime.date.today() + datetime.timedelta(3)),actividad="Diseño",estado='PRO')

"""Asociar la hu con una descripcion para HU2, mismo que el anterior, estan en el mismo Flujo"""
hu2.hu_descripcion.add(dhu1)
hu2.hu_descripcion.add(dhu2)
hu2.hu_descripcion.add(dhu3)

hu2.estado_en_actividad='PRO'
hu2.actividad=act2
hu2.acumulador_horas=5
hu2.save()

"""Creacion de descripciones para la HU3 Mensaje Finalizado antes de tiempo"""
dhu1=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Analisis",estado='FIN')
dhu2=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea2',fecha=str(datetime.date.today()),actividad="Diseño",estado='FIN')
dhu3=HU_descripcion.objects.create(horas_trabajadas=4,descripcion_horas_trabajadas='Tarea3',fecha=str(datetime.date.today() + datetime.timedelta(1)),actividad="Despliegue",estado='FIN')
dhu4=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea4',fecha=str(datetime.date.today() + datetime.timedelta(1)),actividad="Desarrollo",estado='FIN')
dhu5=HU_descripcion.objects.create(horas_trabajadas=0.2,descripcion_horas_trabajadas='Tarea5',fecha=str(datetime.date.today() + datetime.timedelta(2)),actividad="Prueba",estado='FIN')

"""Asociar la hu con una descripcion para HU2, mismo que el anterior, estan en el mismo Flujo"""
hu3.hu_descripcion.add(dhu1)
hu3.hu_descripcion.add(dhu2)
hu3.hu_descripcion.add(dhu3)
hu3.hu_descripcion.add(dhu4)
hu3.hu_descripcion.add(dhu5)

hu3.estado_en_actividad='FIN'
hu3.actividad=act5
hu3.acumulador_horas=18
hu3.save()

"""Ya que se comenzo la primera HU de mas alta prioridad del sprint cambiamos su estado de ACT a CON"""
sp1.estado='CON'
sp1.save()
