#coding: utf-8
import django
django.setup()
import datetime
#from django.db import models
from gestor.models import Permitido, MyUser, HU, proyecto,rol_sistema, rol, asigna_sistema,asignacion, Actividades,Flujo,delegacion,Sprint, HU_descripcion, asignaHU_actividad_flujo, HU_version, historial_notificacion

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

"""Cambia el codename de permission en español"""

permiso=Permission.objects.get(name='Can add rol')
permiso.codename= 'Agregar Rol'
permiso.save()
permiso=Permission.objects.get(name='Can change rol')
permiso.codename= 'Modificar Rol'
permiso.save()
permiso=Permission.objects.get(name='Can delete rol')
permiso.codename='Eliminar Rol'
permiso.save()
permiso=Permission.objects.get(name='Can add actividades')
permiso.codename='Agregar Actividad'
permiso.save()
permiso=Permission.objects.get(name='Can change actividades')
permiso.codename='Modificar Actividad'
permiso.save()
permiso=Permission.objects.get(name='Can delete actividades')
permiso.codename='Eliminar Actividad'
permiso.save()
permiso=Permission.objects.get(name='Can add flujo')
permiso.codename='Agregar Flujo'
permiso.save()
permiso=Permission.objects.get(name='Can change flujo')
permiso.codename='Modificar Flujo'
permiso.save()
permiso=Permission.objects.get(name='Can delete flujo')
permiso.codename='Eliminar Flujo'
permiso.save()
permiso=Permission.objects.get(name='Can change proyecto')
permiso.codename='Modificar Proyecto'
permiso.save()
permiso=Permission.objects.get(name='Can add sprint')
permiso.codename='Agregar Sprint'
permiso.save()
permiso=Permission.objects.get(name='Can change sprint')
permiso.codename='Modificar Sprint'
permiso.save()
permiso=Permission.objects.get(name='Can delete sprint')
permiso.codename='Eliminar Sprint'
permiso.save()
permiso=Permission.objects.get(name='Can add asignacion')
permiso.codename='Agregar Asignacion'
permiso.save()
permiso=Permission.objects.get(name='Can change asignacion')
permiso.codename='Modificar Asignacion'
permiso.save()
permiso=Permission.objects.get(name='Can delete asignacion')
permiso.codename='Eliminar Asignacion'
permiso.save()
permiso=Permission.objects.get(name='Can add delegacion')
permiso.codename='Agregar Delegacion'
permiso.save()
permiso=Permission.objects.get(name='Can change delegacion')
permiso.codename='Modificar Delegacion'
permiso.save()
permiso=Permission.objects.get(name='Can delete delegacion')
permiso.codename='Eliminar Delegacion'
permiso.save()
permiso=Permission.objects.get(name='Can add asigna h u_actividad_flujo')
permiso.codename='Agregar asigna h u_actividad_flujo'
permiso.save()
permiso=Permission.objects.get(name='Can change asigna h u_actividad_flujo')
permiso.codename='Modifica asigna h u_actividad_flujo'
permiso.save()
permiso=Permission.objects.get(name='Can delete asigna h u_actividad_flujo')
permiso.codename='Elminar asigna h u_actividad_flujo'
permiso.save()
permiso=Permission.objects.get(name='Can add archivoadjunto')
permiso.codename='Agregar Archivo Adjunto'
permiso.save()
permiso=Permission.objects.get(name='Can change archivoadjunto')
permiso.codename='Modificar Archivo Adjunto'
permiso.save()
permiso=Permission.objects.get(name='Can delete archivoadjunto')
permiso.codename='Eliminar Archivo Adjunto'
permiso.save()
permiso=Permission.objects.get(name='Can add hu')
permiso.codename='Agregar HU'
permiso.save()
permiso=Permission.objects.get(name='Can change hu')
permiso.codename='Modificar HU'
permiso.save()
permiso=Permission.objects.get(name='Can delete hu')
permiso.codename='Eliminar HU'
permiso.save()
permiso=Permission.objects.get(name='Can add asigna_sistema')
permiso.codename='Agregar asigna_sistema'
permiso.save()
permiso=Permission.objects.get(name='Can change asigna_sistema')
permiso.codename='Modificar asigna_sistema'
permiso.save()
permiso=Permission.objects.get(name='Can delete asigna_sistema')
permiso.codename='Eliminar asigna_sistema'
permiso.save()
permiso=Permission.objects.get(name='Can add rol_sistema')
permiso.codename='Agregar rol_sistema'
permiso.save()
permiso=Permission.objects.get(name='Can change rol_sistema')
permiso.codename='Modificar rol_sistema'
permiso.save()
permiso=Permission.objects.get(name='Can delete rol_sistema')
permiso.codename='Eliminar rol_sistema'
permiso.save()
permiso=Permission.objects.get(name='Can add session')
permiso.codename='Agregar session'
permiso.save()
permiso=Permission.objects.get(name='Can change session')
permiso.codename='Modificar session'
permiso.save()
permiso=Permission.objects.get(name='Can delete session')
permiso.codename='Eliminar session'
permiso.save()
permiso=Permission.objects.get(name='Can add queue message')
permiso.codename='Agregar cola de mensajes'
permiso.save()
permiso=Permission.objects.get(name='Can change queue message')
permiso.codename='Modificar cola de mensajes'
permiso.save()
permiso=Permission.objects.get(name='Can delete queue message')
permiso.codename='Eliminar cola de mensajes'
permiso.save()

"""Creacion de correos electronicos asociados a usuarios"""
perm4=Permitido.objects.create(email='gsebacatt@gmail.com')
perm3=Permitido.objects.create(email='katherinevera94@gmail.com')
perm2=Permitido.objects.create(email='delsy.denis.21@gmail.com')
perm1=Permitido.objects.create(email='admin@gmail.com')
perm5=Permitido.objects.create(email='gabriela@gmail.com')
perm6=Permitido.objects.create(email='vanessa@gmail.com')
perm7=Permitido.objects.create(email='valeria@gmail.com')

"""Creacion de usuarios usando los email permitidos creados anteriormente"""
admin=MyUser.objects.create(password='pbkdf2_sha256$15000$5PUgdTbag7Cm$kbLmrEL+pT+iWKraH4+8Kq6aVL9bA5wDHkFFYiRlogI=',username='admin',user_name='Administrador',last_name='Administrador',direccion='Padre Cardozo',is_active=True,is_admin=True,email=perm1,frecuencia_notificaciones='mes')
kathe=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='katherine',user_name='Katherine',last_name='Vera',direccion='Lambare',is_active=True,is_admin=False,email=perm3, frecuencia_notificaciones='dia')
delsy=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='delsy',user_name='Delsy',last_name='Denis',direccion='San Lorenzo',is_active=True,is_admin=False,email=perm2, frecuencia_notificaciones='instante')
sebas=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='sebas',user_name='Sebastian',last_name='Cattaneo',direccion='Asuncion',is_active=True,is_admin=False,email=perm4, frecuencia_notificaciones='semana')
gabriela=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='gabriela',user_name='Gabriela',last_name='Gabriela',direccion='Lambare',is_active=True,is_admin=False,email=perm5, frecuencia_notificaciones='mes')
vanessa=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='vanessa',user_name='Vanessa',last_name='Vanessa',direccion='Lambare',is_active=True,is_admin=False,email=perm6, frecuencia_notificaciones='mes')
valeria=MyUser.objects.create(password='pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=',username='valeria',user_name='Valeria',last_name='Valeria',direccion='Lambare',is_active=True,is_admin=False,email=perm7, frecuencia_notificaciones='mes')

"""Creacion de permisos que faltan"""
content_type = ContentType.objects.get_for_model(HU)
permission1 = Permission.objects.create(codename='Puede agregar horas trabajadas',
                                       name='Agregar horas trabajadas',
                                       content_type=content_type)
permission2 = Permission.objects.create(codename='Puede cambiar HU a nivel Scrum',
                                       name='Can change hu nivel Scrum',
                                       content_type=content_type)
content_type2 = ContentType.objects.get_for_model(proyecto)
permission3 = Permission.objects.create(codename='Visualizar proyecto',
                                       name='Visualizar proyecto',
                                       content_type=content_type2)
permission4 = Permission.objects.create(codename='Visualizar equipo',
                                       name='Visualizar equipo',
                                       content_type=content_type2)
permission5 = Permission.objects.create(codename='Generar Reporte',
                                       name='Generar Reporte',
                                       content_type=content_type)
permission6 = Permission.objects.create(codename='Visualizar Chart',
                                       name='Visualizar Chart',
                                       content_type=content_type)

"""Creacion de proyectos precargados"""
p1=proyecto.objects.create(nombre_corto='p1',nombre_largo='proyecto1',descripcion='proyecto1',fecha_inicio=str(datetime.date.today()+ datetime.timedelta(days=-6)),duracion=20,cantidad_dias_transcurridos=6,fecha_fin=str(datetime.date.today() + datetime.timedelta(days=20)),estado='ACT')
p2=proyecto.objects.create(nombre_corto='p2',nombre_largo='proyecto2',descripcion='proyecto2',fecha_inicio=str(datetime.date.today()- datetime.timedelta(days=20)),duracion=20,cantidad_dias_transcurridos=20,fecha_fin=str(datetime.date.today()),estado='ACT')
p3=proyecto.objects.create(nombre_corto='p3',nombre_largo='proyecto3',descripcion='proyecto3',fecha_inicio=str(datetime.date.today()),duracion=20,cantidad_dias_transcurridos=0,fecha_fin=str(datetime.date.today() + datetime.timedelta(days=20)),estado='PEN')
p4=proyecto.objects.create(nombre_corto='p4',nombre_largo='proyecto4',descripcion='proyecto4',fecha_inicio=str(datetime.date.today()),duracion=20,cantidad_dias_transcurridos=0,fecha_fin=str(datetime.date.today() + datetime.timedelta(days=20)),estado='PEN')


"""Creacion de rol admin y relacionamiento a todos los permisos existentes"""

rol_admin=rol_sistema.objects.create(nombre_rol_id='admin',descripcion='admin tiene todos los permisos')


"""Creacion de roles predefinidos a nivel proyecto Scrum,Owner, etc, y uno hecho por un Scrum para probar que tal"""
rol_scrum=rol.objects.create(nombre_rol_id='Scrum Master',descripcion='Permisos adquiridos por el ScrumMaster',usuario_creador=admin,estado='ACT')
rol_owner=rol.objects.create(nombre_rol_id='Product Owner',descripcion='Permisos adquiridos por el Product Owner',usuario_creador=admin,estado='ACT')
rol_equipo=rol.objects.create(nombre_rol_id='Equipo',descripcion='Permisos adquiridos por el Equipo',usuario_creador=admin,estado='ACT')
rol_cliente=rol.objects.create(nombre_rol_id='Cliente',descripcion='Permisos adquiridos por el Cliente',usuario_creador=admin,estado='ACT')

rol_deScrum=rol.objects.create(nombre_rol_id='Rol creado por Scrum',descripcion='Permisos designados por el Scrum',usuario_creador=delsy,estado='ACT')
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+ROL+"+"C+"+"Se ha creado un nuevo rol de nombre: '"+rol_deScrum.nombre_rol_id+"' con una descripcion '"+rol_deScrum.descripcion+"' con los permisos '"+str([t.codename for t in rol_deScrum.permisos.all()])+"' con fecha y hora: "+str(datetime.date.today())
h=historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=rol_deScrum.nombre_rol_id,  evento=evento_e)
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
rol_scrum.permisos.add(per_add_asignahu,per_change_asignahu,per_delete_asignahu,permission6)


"""Carga para el Product Owner"""
"""Voy a usar los permisos  ya cargados  y obtener los nuevos que se necesiten, lo mismo para los demas roles"""

per_add_hu=Permission.objects.get(name='Can add hu')
per_change_hu=Permission.objects.get(name='Can change hu')
per_delete_hu=Permission.objects.get(name='Can delete hu')

"""Y aca le asigno solamente esos 3 ultimos permisos obtenidos"""
rol_owner.permisos.add(per_add_hu,per_change_hu,per_delete_hu,permission6)

"""Carga para el Equipo"""
rol_equipo.permisos.add(permission1,permission6) # se cargo y se obtuvo en la linea 24


"""Carga para el Cliente"""
"""Se le asigna visualizar proyecto, visualizar equipo y generar reporte que ya se obtuvieron en lineas 31,34,37"""
rol_cliente.permisos.add(permission3,permission4,permission5,permission6)


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
asignacion.objects.create(usuario=delsy,rol=rol_equipo,proyecto=p2)
asignacion.objects.create(usuario=valeria,rol=rol_equipo,proyecto=p2)
asignacion.objects.create(usuario=gabriela,rol=rol_equipo,proyecto=p2)
asignacion.objects.create(usuario=kathe,rol=rol_scrum,proyecto=p3)
asignacion.objects.create(usuario=sebas,rol=rol_owner,proyecto=p3)
asignacion.objects.create(usuario=delsy,rol=rol_equipo,proyecto=p3)


"""Creacion de actividades para el flujo 1"""
act1=Actividades.objects.create(nombre='Analisis',descripcion='analisis')
evento_e=str(delsy.id)+"+"+str(p1.id)+"+SCRUM"+"+ACTIVIDAD+"+"C+"+"La Actividad '"+act1.nombre+"' con descripcion '"+act1.descripcion+"' se ha creado exitosamente en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()),  objeto=act1.nombre,evento=evento_e)
act2=Actividades.objects.create(nombre='Disenho',descripcion='diseño')
evento_e=str(delsy.id)+"+"+str(p1.id)+"+SCRUM"+"+ACTIVIDAD+"+"C+"+"La Actividad '"+act2.nombre+"' con descripcion '"+act2.descripcion+"' se ha creado exitosamente en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()),  objeto=act2.nombre,evento=evento_e)
act3=Actividades.objects.create(nombre='Despliegue',descripcion='Despliegue')
evento_e=str(delsy.id)+"+"+str(p1.id)+"+SCRUM"+"+ACTIVIDAD+"+"C+"+"La Actividad '"+act3.nombre+"' con descripcion '"+act3.descripcion+"' se ha creado exitosamente en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()),  objeto=act3.nombre,evento=evento_e)
act4=Actividades.objects.create(nombre='Desarrollo',descripcion='desarrollo')
evento_e=str(delsy.id)+"+"+str(p1.id)+"+SCRUM"+"+ACTIVIDAD+"+"C+"+"La Actividad '"+act4.nombre+"' con descripcion '"+act4.descripcion+"' se ha creado exitosamente en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()),  objeto=act4.nombre,evento=evento_e)
act5=Actividades.objects.create(nombre='Prueba',descripcion='prueba')
evento_e=str(delsy.id)+"+"+str(p1.id)+"+SCRUM"+"+ACTIVIDAD+"+"C+"+"La Actividad '"+act5.nombre+"' con descripcion '"+act5.descripcion+"' se ha creado exitosamente en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()),  objeto=act5.nombre,evento=evento_e)

"""Creacion de actividades para el flujo 2"""
act6=Actividades.objects.create(nombre='Relevamiento',descripcion='relevamiento')
evento_e=str(delsy.id)+"+"+str(p1.id)+"+SCRUM"+"+ACTIVIDAD+"+"C+"+"La Actividad '"+act6.nombre+"' con descripcion '"+act6.descripcion+"' se ha creado exitosamente en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()),  objeto=act6.nombre,evento=evento_e)
act7=Actividades.objects.create(nombre='Implementacion',descripcion='implementacion')
evento_e=str(delsy.id)+"+"+str(p1.id)+"+SCRUM"+"+ACTIVIDAD+"+"C+"+"La Actividad '"+act7.nombre+"' con descripcion '"+act7.descripcion+"' se ha creado exitosamente en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()),  objeto=act7.nombre,evento=evento_e)
act8=Actividades.objects.create(nombre='Control',descripcion='control de tareas')
evento_e=str(delsy.id)+"+"+str(p1.id)+"+SCRUM"+"+ACTIVIDAD+"+"C+"+"La Actividad '"+act8.nombre+"' con descripcion '"+act8.descripcion+"' se ha creado exitosamente en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()),  objeto=act8.nombre,evento=evento_e)


"""Cargar los primeros flujos"""
f1=Flujo.objects.create(nombre='Flujo1',estado='ACT',orden_actividades='[1,2,3,4,5]')
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"FLUJO+"+"C+"+"Se ha creado un nuevo flujo de nombre: '"+f1.nombre+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=f1.nombre, evento=evento_e)
f2=Flujo.objects.create(nombre='Flujo2',estado='ACT',orden_actividades='[6,7,8]')
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"FLUJO+"+"C+"+"Se ha creado un nuevo flujo de nombre: '"+f2.nombre+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=f2.nombre, evento=evento_e)
#Flujo 3, una combinacion de los flujos anteriores
f3=Flujo.objects.create(nombre='Flujo3',estado='ACT',orden_actividades='[6,2,4,8]')
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"FLUJO+"+"C+"+"Se ha creado un nuevo flujo de nombre: '"+f3.nombre+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=f3.nombre, evento=evento_e)


"""Cargar las actividades del flujo1"""
f1.actividades.add(act1,act2,act3,act4,act5)

"""Cargar las actividades del flujo2"""
f2.actividades.add(act6,act7,act8)


"""Cargar las actividades del flujo3"""
f3.actividades.add(act6,act2,act4,act8)


"""Creacion de HU"""
hu1=HU.objects.create(descripcion='HU1',valor_negocio=3,valor_tecnico=5,prioridad=95,duracion=15,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1,version=1.0)
huv1=HU_version.objects.create(descripcion=hu1.descripcion,valor_negocio=hu1.valor_negocio,hu=hu1,version=hu1.version)
evento_e=str(kathe.id)+"+"+str(p1.id)+"+"+str(rol_owner.id)+"+"+"HU+"+"C+"+"Se ha creado un nuevo HU de nombre: "+hu1.descripcion+" con valor de negocio "+str(hu1.valor_negocio)+" con fecha y hora: "+str(datetime.date.today())
h=historial_notificacion.objects.create(usuario=kathe, fecha_hora=str(datetime.date.today()), objeto=hu1.descripcion, evento=evento_e)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"M+"+"Se ha modificado '"+hu1.descripcion+"' con valor tecnico '"+str(hu1.valor_tecnico)+"' con prioridad '"+str(hu1.prioridad)+" duracion "+str(hu1.duracion)+' y estado '+hu1.estado+" con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu1.descripcion, evento=evento_e)

hu2=HU.objects.create(descripcion='HU2',valor_negocio=5,valor_tecnico=7,prioridad=90,duracion=5,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1,version=1.0)
huv2=HU_version.objects.create(descripcion=hu2.descripcion,valor_negocio=hu2.valor_negocio,hu=hu2,version=hu2.version)
evento_e=str(kathe.id)+"+"+str(p1.id)+"+"+str(rol_owner.id)+"+"+"HU+"+"C+"+"Se ha creado un nuevo HU de nombre: "+hu2.descripcion+" con valor de negocio "+str(hu2.valor_negocio)+" con fecha y hora: "+str(datetime.date.today())
h=historial_notificacion.objects.create(usuario=kathe, fecha_hora=str(datetime.date.today()), objeto=hu2.descripcion, evento=evento_e)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"M+"+"Se ha modificado '"+hu2.descripcion+"' con valor tecnico '"+str(hu2.valor_tecnico)+"' con prioridad '"+str(hu2.prioridad)+" duracion "+str(hu2.duracion)+' y estado '+hu2.estado+" con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu2.descripcion, evento=evento_e)

hu3=HU.objects.create(descripcion='HU3',valor_negocio=8,valor_tecnico=6,prioridad=85,duracion=20,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1,version=1.0)
huv3=HU_version.objects.create(descripcion=hu3.descripcion,valor_negocio=hu3.valor_negocio,hu=hu3,version=hu3.version)
evento_e=str(kathe.id)+"+"+str(p1.id)+"+"+str(rol_owner.id)+"+"+"HU+"+"C+"+"Se ha creado un nuevo HU de nombre: "+hu3.descripcion+" con valor de negocio "+str(hu1.valor_negocio)+" con fecha y hora: "+str(datetime.date.today())
h=historial_notificacion.objects.create(usuario=kathe, fecha_hora=str(datetime.date.today()), objeto=hu3.descripcion, evento=evento_e)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"M+"+"Se ha modificado '"+hu3.descripcion+"' con valor tecnico '"+str(hu3.valor_tecnico)+"' con prioridad '"+str(hu3.prioridad)+" duracion "+str(hu3.duracion)+' y estado '+hu3.estado+" con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu3.descripcion, evento=evento_e)

hu4=HU.objects.create(descripcion='HU4',valor_negocio=2,valor_tecnico=5,prioridad=80,duracion=8,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1,version=1.0)
huv4=HU_version.objects.create(descripcion=hu4.descripcion,valor_negocio=hu4.valor_negocio,hu=hu4,version=hu4.version)
evento_e=str(kathe.id)+"+"+str(p1.id)+"+"+str(rol_owner.id)+"+"+"HU+"+"C+"+"Se ha creado un nuevo HU de nombre: "+hu4.descripcion+" con valor de negocio "+str(hu1.valor_negocio)+" con fecha y hora: "+str(datetime.date.today())
h=historial_notificacion.objects.create(usuario=kathe, fecha_hora=str(datetime.date.today()), objeto=hu4.descripcion, evento=evento_e)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"M+"+"Se ha modificado '"+hu4.descripcion+"' con valor tecnico '"+str(hu4.valor_tecnico)+"' con prioridad '"+str(hu4.prioridad)+" duracion "+str(hu4.duracion)+' y estado '+hu4.estado+" con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu4.descripcion, evento=evento_e)

hu5=HU.objects.create(descripcion='HU5',valor_negocio=9,valor_tecnico=7,prioridad=75,duracion=5,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1,version=1.0)
huv5=HU_version.objects.create(descripcion=hu5.descripcion,valor_negocio=hu5.valor_negocio,hu=hu5,version=hu5.version)
evento_e=str(kathe.id)+"+"+str(p1.id)+"+"+str(rol_owner.id)+"+"+"HU+"+"C+"+"Se ha creado un nuevo HU de nombre: "+hu5.descripcion+" con valor de negocio "+str(hu5.valor_negocio)+" con fecha y hora: "+str(datetime.date.today())
h=historial_notificacion.objects.create(usuario=kathe, fecha_hora=str(datetime.date.today()), objeto=hu5.descripcion, evento=evento_e)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"M+"+"Se ha modificado '"+hu5.descripcion+"' con valor tecnico '"+str(hu5.valor_tecnico)+"' con prioridad '"+str(hu5.prioridad)+" duracion "+str(hu5.duracion)+' y estado '+hu5.estado+" con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu5.descripcion, evento=evento_e)

hu6=HU.objects.create(descripcion='HU6',valor_negocio=8,valor_tecnico=6,prioridad=80,duracion=20,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1,version=1.0)
huv6=HU_version.objects.create(descripcion=hu6.descripcion,valor_negocio=hu6.valor_negocio,hu=hu6,version=hu6.version)
evento_e=str(kathe.id)+"+"+str(p1.id)+"+"+str(rol_owner.id)+"+"+"HU+"+"C+"+"Se ha creado un nuevo HU de nombre: "+hu6.descripcion+" con valor de negocio "+str(hu6.valor_negocio)+" con fecha y hora: "+str(datetime.date.today())
h=historial_notificacion.objects.create(usuario=kathe, fecha_hora=str(datetime.date.today()), objeto=hu6.descripcion, evento=evento_e)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"M+"+"Se ha modificado '"+hu6.descripcion+"' con valor tecnico '"+str(hu6.valor_tecnico)+"' con prioridad '"+str(hu6.prioridad)+" duracion "+str(hu6.duracion)+' y estado '+hu6.estado+" con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu6.descripcion, evento=evento_e)

hu7=HU.objects.create(descripcion='HU7',valor_negocio=10,valor_tecnico=4,prioridad=68,duracion=30,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1,version=1.0)
huv7=HU_version.objects.create(descripcion=hu7.descripcion,valor_negocio=hu7.valor_negocio,hu=hu7,version=hu7.version)
evento_e=str(kathe.id)+"+"+str(p1.id)+"+"+str(rol_owner.id)+"+"+"HU+"+"C+"+"Se ha creado un nuevo HU de nombre: "+hu7.descripcion+" con valor de negocio "+str(hu7.valor_negocio)+" con fecha y hora: "+str(datetime.date.today())
h=historial_notificacion.objects.create(usuario=kathe, fecha_hora=str(datetime.date.today()), objeto=hu7.descripcion, evento=evento_e)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"M+"+"Se ha modificado '"+hu7.descripcion+"' con valor tecnico '"+str(hu7.valor_tecnico)+"' con prioridad '"+str(hu7.prioridad)+" duracion "+str(hu7.duracion)+' y estado '+hu7.estado+" con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu7.descripcion, evento=evento_e)

hu8=HU.objects.create(descripcion='HU8',valor_negocio=5,valor_tecnico=7,prioridad=60,duracion=5,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1,version=1.0)
huv8=HU_version.objects.create(descripcion=hu8.descripcion,valor_negocio=hu8.valor_negocio,hu=hu8,version=hu8.version)
evento_e=str(kathe.id)+"+"+str(p1.id)+"+"+str(rol_owner.id)+"+"+"HU+"+"C+"+"Se ha creado un nuevo HU de nombre: "+hu8.descripcion+" con valor de negocio "+str(hu8.valor_negocio)+" con fecha y hora: "+str(datetime.date.today())
h=historial_notificacion.objects.create(usuario=kathe, fecha_hora=str(datetime.date.today()), objeto=hu8.descripcion, evento=evento_e)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"M+"+"Se ha modificado '"+hu8.descripcion+"' con valor tecnico '"+str(hu8.valor_tecnico)+"' con prioridad '"+str(hu8.prioridad)+" duracion "+str(hu8.duracion)+' y estado '+hu8.estado+" con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu8.descripcion, evento=evento_e)

hu9=HU.objects.create(descripcion='HU9',valor_negocio=8,valor_tecnico=6,prioridad=45,duracion=20,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1,version=1.0)
huv9=HU_version.objects.create(descripcion=hu9.descripcion,valor_negocio=hu9.valor_negocio,hu=hu9,version=hu9.version)
evento_e=str(kathe.id)+"+"+str(p1.id)+"+"+str(rol_owner.id)+"+"+"HU+"+"C+"+"Se ha creado un nuevo HU de nombre: "+hu9.descripcion+" con valor de negocio "+str(hu9.valor_negocio)+" con fecha y hora: "+str(datetime.date.today())
h=historial_notificacion.objects.create(usuario=kathe, fecha_hora=str(datetime.date.today()), objeto=hu9.descripcion, evento=evento_e)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"M+"+"Se ha modificado '"+hu9.descripcion+"' con valor tecnico '"+str(hu9.valor_tecnico)+"' con prioridad '"+str(hu9.prioridad)+" duracion "+str(hu9.duracion)+' y estado '+hu9.estado+" con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu9.descripcion, evento=evento_e)

hu10=HU.objects.create(descripcion='HU10',valor_negocio=2,valor_tecnico=5,prioridad=40,duracion=8,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1,version=1.0)
huv10=HU_version.objects.create(descripcion=hu10.descripcion,valor_negocio=hu10.valor_negocio,hu=hu10,version=hu10.version)
evento_e=str(kathe.id)+"+"+str(p1.id)+"+"+str(rol_owner.id)+"+"+"HU+"+"C+"+"Se ha creado un nuevo HU de nombre: "+hu10.descripcion+" con valor de negocio "+str(hu10.valor_negocio)+" con fecha y hora: "+str(datetime.date.today())
h=historial_notificacion.objects.create(usuario=kathe, fecha_hora=str(datetime.date.today()), objeto=hu10.descripcion, evento=evento_e)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"M+"+"Se ha modificado '"+hu10.descripcion+"' con valor tecnico '"+str(hu10.valor_tecnico)+"' con prioridad '"+str(hu10.prioridad)+" duracion "+str(hu10.duracion)+' y estado '+hu10.estado+" con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu10.descripcion, evento=evento_e)

hu11=HU.objects.create(descripcion='HU11',valor_negocio=9,valor_tecnico=7,prioridad=35,duracion=5,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1,version=1.0)
huv11=HU_version.objects.create(descripcion=hu11.descripcion,valor_negocio=hu11.valor_negocio,hu=hu11,version=hu11.version)
evento_e=str(kathe.id)+"+"+str(p1.id)+"+"+str(rol_owner.id)+"+"+"HU+"+"C+"+"Se ha creado un nuevo HU de nombre: "+hu11.descripcion+" con valor de negocio "+str(hu11.valor_negocio)+" con fecha y hora: "+str(datetime.date.today())
h=historial_notificacion.objects.create(usuario=kathe, fecha_hora=str(datetime.date.today()), objeto=hu11.descripcion, evento=evento_e)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"M+"+"Se ha modificado '"+hu11.descripcion+"' con valor tecnico '"+str(hu11.valor_tecnico)+"' con prioridad '"+str(hu11.prioridad)+" duracion "+str(hu11.duracion)+' y estado '+hu11.estado+" con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu11.descripcion, evento=evento_e)

hu12=HU.objects.create(descripcion='HU12',valor_negocio=10,valor_tecnico=0,prioridad=0,duracion=0,acumulador_horas=0,estado='ACT',estado_en_actividad='PEN',valido=False,proyecto=p1,version=1.0)
huv12=HU_version.objects.create(descripcion=hu12.descripcion,valor_negocio=hu12.valor_negocio,hu=hu12,version=hu12.version)
evento_e=str(kathe.id)+"+"+str(p1.id)+"+"+str(rol_owner.id)+"+"+"HU+"+"C+"+"Se ha creado un nuevo HU de nombre: "+hu12.descripcion+" con valor de negocio "+str(hu12.valor_negocio)+" con fecha y hora: "+str(datetime.date.today())
h=historial_notificacion.objects.create(usuario=kathe, fecha_hora=str(datetime.date.today()), objeto=hu12.descripcion, evento=evento_e)


#Ahora voy a crear las hu para el sprint sp0 terminado, tienen que haber suficientes descripciones que indiquen que se finalizo su duracion
#seran 6 hus para este sprint
hu13=HU.objects.create(descripcion='HU13',valor_negocio=3,valor_tecnico=5,prioridad=95,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p1,version=1.0)
huv13=HU_version.objects.create(descripcion=hu13.descripcion,valor_negocio=hu13.valor_negocio,hu=hu13,version=hu13.version)

hu14=HU.objects.create(descripcion='HU14',valor_negocio=3,valor_tecnico=5,prioridad=85,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p1,version=1.0)
huv14=HU_version.objects.create(descripcion=hu14.descripcion,valor_negocio=hu14.valor_negocio,hu=hu14,version=hu14.version)

hu15=HU.objects.create(descripcion='HU15',valor_negocio=3,valor_tecnico=5,prioridad=75,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p1,version=1.0)
huv15=HU_version.objects.create(descripcion=hu15.descripcion,valor_negocio=hu15.valor_negocio,hu=hu15,version=hu15.version)

hu16=HU.objects.create(descripcion='HU16',valor_negocio=3,valor_tecnico=5,prioridad=65,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p1,version=1.0)
huv16=HU_version.objects.create(descripcion=hu16.descripcion,valor_negocio=hu16.valor_negocio,hu=hu16,version=hu16.version)

hu17=HU.objects.create(descripcion='HU17',valor_negocio=3,valor_tecnico=5,prioridad=55,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p1,version=1.0)
huv17=HU_version.objects.create(descripcion=hu17.descripcion,valor_negocio=hu17.valor_negocio,hu=hu17,version=hu17.version)

hu18=HU.objects.create(descripcion='HU18',valor_negocio=3,valor_tecnico=5,prioridad=45,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p1,version=1.0)
huv18=HU_version.objects.create(descripcion=hu18.descripcion,valor_negocio=hu18.valor_negocio,hu=hu18,version=hu18.version)

#Ahora voy a crear las hu que van a quedar pendientes en el sprint que finaliza anticipadamente sprint01,no les voy a cargar horas
hu19=HU.objects.create(descripcion='HU19',valor_negocio=3,valor_tecnico=5,prioridad=65,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1,version=1.0)
huv19=HU_version.objects.create(descripcion=hu19.descripcion,valor_negocio=hu19.valor_negocio,hu=hu19,version=hu19.version)

hu20=HU.objects.create(descripcion='HU20',valor_negocio=3,valor_tecnico=5,prioridad=55,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1,version=1.0)
huv20=HU_version.objects.create(descripcion=hu20.descripcion,valor_negocio=hu20.valor_negocio,hu=hu20,version=hu20.version)

hu21=HU.objects.create(descripcion='HU21',valor_negocio=3,valor_tecnico=5,prioridad=45,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='PEN',valido=True,proyecto=p1,version=1.0)
huv21=HU_version.objects.create(descripcion=hu21.descripcion,valor_negocio=hu21.valor_negocio,hu=hu21,version=hu21.version)

#HU para el proyeto 2 que va a finalizar
hu22=HU.objects.create(descripcion='HU22',valor_negocio=3,valor_tecnico=5,prioridad=45,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p2,version=1.0)
huv22=HU_version.objects.create(descripcion=hu22.descripcion,valor_negocio=hu22.valor_negocio,hu=hu22,version=hu22.version)

hu23=HU.objects.create(descripcion='HU23',valor_negocio=3,valor_tecnico=5,prioridad=45,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p2,version=1.0)
huv23=HU_version.objects.create(descripcion=hu23.descripcion,valor_negocio=hu23.valor_negocio,hu=hu23,version=hu23.version)

hu24=HU.objects.create(descripcion='HU24',valor_negocio=3,valor_tecnico=5,prioridad=45,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p2,version=1.0)
huv24=HU_version.objects.create(descripcion=hu24.descripcion,valor_negocio=hu24.valor_negocio,hu=hu24,version=hu24.version)

hu25=HU.objects.create(descripcion='HU25',valor_negocio=3,valor_tecnico=5,prioridad=45,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p2,version=1.0)
huv25=HU_version.objects.create(descripcion=hu25.descripcion,valor_negocio=hu25.valor_negocio,hu=hu25,version=hu25.version)

hu26=HU.objects.create(descripcion='HU26',valor_negocio=3,valor_tecnico=5,prioridad=45,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p2,version=1.0)
huv26=HU_version.objects.create(descripcion=hu26.descripcion,valor_negocio=hu26.valor_negocio,hu=hu26,version=hu26.version)

hu27=HU.objects.create(descripcion='HU27',valor_negocio=3,valor_tecnico=5,prioridad=45,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p2,version=1.0)
huv27=HU_version.objects.create(descripcion=hu27.descripcion,valor_negocio=hu27.valor_negocio,hu=hu27,version=hu27.version)

hu28=HU.objects.create(descripcion='HU28',valor_negocio=3,valor_tecnico=5,prioridad=45,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p2,version=1.0)
huv28=HU_version.objects.create(descripcion=hu28.descripcion,valor_negocio=hu28.valor_negocio,hu=hu28,version=hu28.version)

hu29=HU.objects.create(descripcion='HU29',valor_negocio=3,valor_tecnico=5,prioridad=45,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p2,version=1.0)
huv29=HU_version.objects.create(descripcion=hu29.descripcion,valor_negocio=hu29.valor_negocio,hu=hu29,version=hu29.version)

hu30=HU.objects.create(descripcion='HU30',valor_negocio=3,valor_tecnico=5,prioridad=45,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p2,version=1.0)
huv30=HU_version.objects.create(descripcion=hu30.descripcion,valor_negocio=hu30.valor_negocio,hu=hu30,version=hu30.version)

hu31=HU.objects.create(descripcion='HU31',valor_negocio=3,valor_tecnico=5,prioridad=45,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='APR',valido=True,proyecto=p2,version=1.0)
huv31=HU_version.objects.create(descripcion=hu31.descripcion,valor_negocio=hu31.valor_negocio,hu=hu31,version=hu31.version)

hu32=HU.objects.create(descripcion='HU32',valor_negocio=3,valor_tecnico=5,prioridad=45,duracion=15,acumulador_horas=15,estado='ACT',estado_en_actividad='ARP',valido=True,proyecto=p2,version=1.0)
huv32=HU_version.objects.create(descripcion=hu32.descripcion,valor_negocio=hu32.valor_negocio,hu=hu32,version=hu32.version)


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
 
#para el sp0 pongo las hu en actividad 5 nomas ya//parece que esto no hace falta

hu13.actividad=act5
hu13.save()
hu14.actividad=act5
hu14.save()
hu15.actividad=act5
hu15.save()
hu16.actividad=act8
hu16.save()
hu17.actividad=act8
hu17.save()
hu18.actividad=act8
hu18.save()

hu19.actividad=act8
hu19.save()
hu20.actividad=act8
hu20.save()
hu21.actividad=act8
hu21.save()

"""--------------------------------------Creacion de un Sprint finalizado correctamente SPRINT0-----------------------------------"""
#este va a ser el finalizado correctamente, con hus nuevas que tengo que crear
sp0=Sprint.objects.create(descripcion='sprint0',fecha_inicio=str(datetime.date.today()-datetime.timedelta(days=15)),duracion=7,estado='FIN',proyecto=p1)

"""Agregar hus a los sprint creados"""
sp0.hu.add(hu13,hu14,hu15,hu16,hu17,hu18)

"""Agregar hus a los sprint creados"""
sp0.flujo.add(f1,f2)

"""Agregar el quipo a los sprint creados"""
sp0.equipo.add(gabriela,sebas)

"""Clasificar esas hus seleccionadas en flujos"""
#hu 13,14,15 en flujo 1 y 16,17,18 en flujo 2
hu13Flujo1=asignaHU_actividad_flujo.objects.create(flujo_al_que_pertenece=f1)
hu13Flujo1.lista_de_HU.add(hu13,hu14,hu15)
hu13Flujo1.save()
hu16Flujo1=asignaHU_actividad_flujo.objects.create(flujo_al_que_pertenece=f2)
hu16Flujo1.lista_de_HU.add(hu16,hu17,hu18)
hu16Flujo1.save()

delegacion.objects.create(usuario=sebas,hu=hu13)
delegacion.objects.create(usuario=sebas,hu=hu15)
delegacion.objects.create(usuario=sebas,hu=hu17)
delegacion.objects.create(usuario=gabriela,hu=hu14)
delegacion.objects.create(usuario=gabriela,hu=hu16)
delegacion.objects.create(usuario=gabriela,hu=hu18)

#Creacion y asignacion de descripciones de hu 13,14,15
dhu131=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Analisis",estado='PRO')
dhu132=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Disenho",estado='PRO')
dhu133=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Despliegue",estado='PRO')
dhu134=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Desarrollo",estado='PRO')
dhu135=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Prueba",estado='PRO')
hu13.hu_descripcion.add(dhu131)
hu13.hu_descripcion.add(dhu132)
hu13.hu_descripcion.add(dhu133)
hu13.hu_descripcion.add(dhu134)
hu13.hu_descripcion.add(dhu135)
hu13.actividad=act5
hu13.acumulador_horas=15
hu13.save()

dhu141=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Analisis",estado='PRO')
dhu142=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Disenho",estado='PRO')
dhu143=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Despliegue",estado='PRO')
dhu144=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Desarrollo",estado='PRO')
dhu145=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Prueba",estado='PRO')
hu14.hu_descripcion.add(dhu141)
hu14.hu_descripcion.add(dhu142)
hu14.hu_descripcion.add(dhu143)
hu14.hu_descripcion.add(dhu144)
hu14.hu_descripcion.add(dhu145)
hu14.actividad=act5
hu14.acumulador_horas=15
hu14.save()

dhu151=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Analisis",estado='PRO')
dhu152=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="diseño",estado='PRO')
dhu153=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Despliegue",estado='PRO')
dhu154=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="desarrollo",estado='PRO')
dhu155=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="prueba",estado='PRO')
hu15.hu_descripcion.add(dhu151)
hu15.hu_descripcion.add(dhu152)
hu15.hu_descripcion.add(dhu153)
hu15.hu_descripcion.add(dhu154)
hu15.hu_descripcion.add(dhu155)
hu15.actividad=act5
hu15.acumulador_horas=15
hu15.save()

#Creacion y asignacion de descripciones de hu 16,17,18
dhu161=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Relevamiento",estado='PRO')
dhu162=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Implementacion",estado='PRO')
dhu163=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Control",estado='PRO')
hu16.hu_descripcion.add(dhu161)
hu16.hu_descripcion.add(dhu162)
hu16.hu_descripcion.add(dhu163)
hu16.actividad=act8
hu16.acumulador_horas=15
hu16.save()

dhu171=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Relevamiento",estado='PRO')
dhu172=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Implementacion",estado='PRO')
dhu173=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Control",estado='PRO')
hu17.hu_descripcion.add(dhu171)
hu17.hu_descripcion.add(dhu172)
hu17.hu_descripcion.add(dhu173)
hu17.actividad=act8
hu17.acumulador_horas=15
hu17.save()

dhu181=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Relevamiento",estado='PRO')
dhu182=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Implementacion",estado='PRO')
dhu183=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Control",estado='PRO')
hu18.hu_descripcion.add(dhu181)
hu18.hu_descripcion.add(dhu182)
hu18.hu_descripcion.add(dhu183)
hu18.actividad=act8
hu18.acumulador_horas=15
hu18.save()

"""--------------------------------------Creacion de un Sprint finalizado con HUs pendientes SPRINT01------------------------------"""

#este va a ser el que tenga hus pendientes las cuales tengo que crear nuevas
sp01=Sprint.objects.create(descripcion='sprint01',fecha_inicio=str(datetime.date.today()+datetime.timedelta(days=-7)),duracion=6,estado='FIN',proyecto=p1)

"""Agregar hus a los sprint creados"""
sp01.hu.add(hu19,hu20,hu21)

"""Agregar hus a los sprint creados"""
sp01.flujo.add(f2)

"""Agregar el quipo a los sprint creados"""
sp01.equipo.add(gabriela,sebas)

"""Clasificar esas hus seleccionadas en flujos"""
#agregar descripciones de progreso
dhu191=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Relevamiento",estado='PRO')
hu19.hu_descripcion.add(dhu191)
hu19.estado_en_actividad='PRO'
hu19.actividad=act8
hu19.acumulador_horas=3
hu19.save()

dhu201=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Relevamiento",estado='PRO')
hu20.hu_descripcion.add(dhu201)
hu20.estado_en_actividad='PRO'
hu20.actividad=act8
hu20.acumulador_horas=3
hu20.save()

dhu211=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Relevamiento",estado='PRO')
hu21.hu_descripcion.add(dhu211)
hu21.estado_en_actividad='PRO'
hu21.actividad=act8
hu21.acumulador_horas=3
hu21.save()

#hu 19,20,21 en flujo 1 para sprint01
hu19Flujo1=asignaHU_actividad_flujo.objects.create(flujo_al_que_pertenece=f2)
hu19Flujo1.lista_de_HU.add(hu19,hu20,hu21)
hu19Flujo1.save()

"""--------------------------------------Creacion de un Sprint de consulta SPRINT1-----------------------------------------------"""

sp1=Sprint.objects.create(descripcion='sprint1',fecha_inicio=str(datetime.date.today()),duracion=10,estado='ACT',proyecto=p1)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"SPRINT+"+"C+"+"Se ha creado un nuevo Sprint de nombre: '"+sp1.descripcion+"' con una fecha de inicio '"+str(sp1.fecha_inicio)+"' ,duracion '"+str(sp1.duracion)+ "' en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=sp1.descripcion, evento=evento_e)

sp1.hu.add(hu1,hu2,hu3,hu4,hu5,hu6,hu7,hu8)

sp1.flujo.add(f1,f2)

sp1.equipo.add(gabriela,sebas)

#hu1 y hu2 estan en el flujo 1
hu1Flujo1=asignaHU_actividad_flujo.objects.create(flujo_al_que_pertenece=f1)
hu1Flujo1.lista_de_HU.add(hu1,hu2,hu3,hu4,hu5)

#hu3 esta en el flujo 2
hu3flujo2=asignaHU_actividad_flujo.objects.create(flujo_al_que_pertenece=f2)
hu3flujo2.lista_de_HU.add(hu6,hu7,hu8)

"""Delegacion de HU a un usuario"""
delegacion.objects.create(usuario=sebas,hu=hu19)
delegacion.objects.create(usuario=sebas,hu=hu20)
delegacion.objects.create(usuario=gabriela,hu=hu21)


delegacion.objects.create(usuario=sebas,hu=hu1)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"AS+"+"Se ha asignado una HU '"+hu1.descripcion+"' al usuario '"+str(sebas)+"' en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu1.descripcion, evento=evento_e)

delegacion.objects.create(usuario=sebas,hu=hu2)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"AS+"+"Se ha asignado una HU '"+hu2.descripcion+"' al usuario '"+str(sebas)+"' en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu2.descripcion, evento=evento_e)

delegacion.objects.create(usuario=sebas,hu=hu3)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"AS+"+"Se ha asignado una HU '"+hu3.descripcion+"' al usuario '"+str(sebas)+"' en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu3.descripcion, evento=evento_e)

delegacion.objects.create(usuario=sebas,hu=hu4)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"AS+"+"Se ha asignado una HU '"+hu4.descripcion+"' al usuario '"+str(sebas)+"' en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu4.descripcion, evento=evento_e)

delegacion.objects.create(usuario=sebas,hu=hu5)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"AS+"+"Se ha asignado una HU '"+hu5.descripcion+"' al usuario '"+str(sebas)+"' en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu5.descripcion, evento=evento_e)

delegacion.objects.create(usuario=gabriela,hu=hu6)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"AS+"+"Se ha asignado una HU '"+hu6.descripcion+"' al usuario '"+str(gabriela)+"' en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu6.descripcion, evento=evento_e)

delegacion.objects.create(usuario=gabriela,hu=hu7)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"AS+"+"Se ha asignado una HU '"+hu7.descripcion+"' al usuario '"+str(gabriela)+"' en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu7.descripcion, evento=evento_e)

delegacion.objects.create(usuario=gabriela,hu=hu8)
evento_e=str(delsy.id)+"+"+str(p1.id)+"+"+str(rol_scrum.id)+"+"+"HU+"+"AS+"+"Se ha asignado una HU '"+hu8.descripcion+"' al usuario '"+str(gabriela)+"' en la fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=delsy, fecha_hora=str(datetime.date.today()), objeto=hu8.descripcion, evento=evento_e)

"""Creacion de descripciones para la HU1 Mensaje Finalizada a Tiempo"""
dhu1=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Analisis",estado='PRO')
evento_e=str(sebas.id)+"+"+str(p1.id)+"+"+str(rol_equipo.id)+"+"+"HU+"+"A+"+"Se ha agregado '"+str(dhu1.horas_trabajadas)+"' horas a la '"+str(hu1.descripcion)+"' con una descripcion '"+dhu1.descripcion_horas_trabajadas+"' estando en la actividad '"+ dhu1.actividad+ "' con el estado '"+dhu1.estado+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=sebas, fecha_hora=str(datetime.date.today()), objeto=hu1.descripcion, evento=evento_e)
dhu2=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea2',fecha=str(datetime.date.today()),actividad="Analisis",estado='FIN')
evento_e=str(sebas.id)+"+"+str(p1.id)+"+"+str(rol_equipo.id)+"+"+"HU+"+"A+"+"Se ha agregado '"+str(dhu2.horas_trabajadas)+"' horas a la '"+str(hu1.descripcion)+"' con una descripcion '"+dhu2.descripcion_horas_trabajadas+"' estando en la actividad '"+ dhu2.actividad+ "' con el estado '"+dhu2.estado+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=sebas, fecha_hora=str(datetime.date.today()), objeto=hu1.descripcion, evento=evento_e)
dhu3=HU_descripcion.objects.create(horas_trabajadas=4,descripcion_horas_trabajadas='Tarea3',fecha=str(datetime.date.today()),actividad="Diseño",estado='PRO')
evento_e=str(sebas.id)+"+"+str(p1.id)+"+"+str(rol_equipo.id)+"+"+"HU+"+"A+"+"Se ha agregado '"+str(dhu3.horas_trabajadas)+"' horas a la '"+str(hu1.descripcion)+"' con una descripcion '"+dhu3.descripcion_horas_trabajadas+"' estando en la actividad '"+ dhu3.actividad+ "' con el estado '"+dhu3.estado+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=sebas, fecha_hora=str(datetime.date.today()), objeto=hu1.descripcion, evento=evento_e)
dhu4=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea4',fecha=str(datetime.date.today() + datetime.timedelta(1)),actividad="Diseño",estado='FIN')
evento_e=str(sebas.id)+"+"+str(p1.id)+"+"+str(rol_equipo.id)+"+"+"HU+"+"A+"+"Se ha agregado '"+str(dhu4.horas_trabajadas)+"' horas a la '"+str(hu1.descripcion)+"' con una descripcion '"+dhu4.descripcion_horas_trabajadas+"' estando en la actividad '"+ dhu4.actividad+ "' con el estado '"+dhu4.estado+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=sebas, fecha_hora=str(datetime.date.today()), objeto=hu1.descripcion, evento=evento_e)
dhu5=HU_descripcion.objects.create(horas_trabajadas=1.2,descripcion_horas_trabajadas='Tarea5',fecha=str(datetime.date.today() + datetime.timedelta(1)),actividad="Despliegue",estado='FIN')
evento_e=str(sebas.id)+"+"+str(p1.id)+"+"+str(rol_equipo.id)+"+"+"HU+"+"A+"+"Se ha agregado '"+str(dhu5.horas_trabajadas)+"' horas a la '"+str(hu1.descripcion)+"' con una descripcion '"+dhu5.descripcion_horas_trabajadas+"' estando en la actividad '"+ dhu5.actividad+ "' con el estado '"+dhu5.estado+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=sebas, fecha_hora=str(datetime.date.today()), objeto=hu1.descripcion, evento=evento_e)
dhu6=HU_descripcion.objects.create(horas_trabajadas=1.8,descripcion_horas_trabajadas='Tarea6',fecha=str(datetime.date.today() + datetime.timedelta(1)),actividad="Desarrollo",estado='FIN')
evento_e=str(sebas.id)+"+"+str(p1.id)+"+"+str(rol_equipo.id)+"+"+"HU+"+"A+"+"Se ha agregado '"+str(dhu6.horas_trabajadas)+"' horas a la '"+str(hu1.descripcion)+"' con una descripcion '"+dhu6.descripcion_horas_trabajadas+"' estando en la actividad '"+ dhu6.actividad+ "' con el estado '"+dhu6.estado+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=sebas, fecha_hora=str(datetime.date.today()), objeto=hu1.descripcion, evento=evento_e)
dhu7=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea7',fecha=str(datetime.date.today() + datetime.timedelta(1)),actividad="Prueba",estado='FIN')
evento_e=str(sebas.id)+"+"+str(p1.id)+"+"+str(rol_equipo.id)+"+"+"HU+"+"A+"+"Se ha agregado '"+str(dhu7.horas_trabajadas)+"' horas a la '"+str(hu1.descripcion)+"' con una descripcion '"+dhu7.descripcion_horas_trabajadas+"' estando en la actividad '"+ dhu7.actividad+ "' con el estado '"+dhu7.estado+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=sebas, fecha_hora=str(datetime.date.today()), objeto=hu1.descripcion, evento=evento_e)
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
dhu1=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()+ datetime.timedelta(2)),actividad="Analisis",estado='PRO')
evento_e=str(sebas.id)+"+"+str(p1.id)+"+"+str(rol_equipo.id)+"+"+"HU+"+"A+"+"Se ha agregado '"+str(dhu1.horas_trabajadas)+"' horas a la '"+str(hu1.descripcion)+"' con una descripcion '"+dhu1.descripcion_horas_trabajadas+"' estando en la actividad '"+ dhu1.actividad+ "' con el estado '"+dhu1.estado+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=sebas, fecha_hora=str(datetime.date.today()), objeto=hu1.descripcion, evento=evento_e)
dhu2=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea2',fecha=str(datetime.date.today() + datetime.timedelta(2)),actividad="Analisis",estado='FIN')
evento_e=str(sebas.id)+"+"+str(p1.id)+"+"+str(rol_equipo.id)+"+"+"HU+"+"A+"+"Se ha agregado '"+str(dhu2.horas_trabajadas)+"' horas a la '"+str(hu1.descripcion)+"' con una descripcion '"+dhu2.descripcion_horas_trabajadas+"' estando en la actividad '"+ dhu2.actividad+ "' con el estado '"+dhu2.estado+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=sebas, fecha_hora=str(datetime.date.today()), objeto=hu1.descripcion, evento=evento_e)
dhu3=HU_descripcion.objects.create(horas_trabajadas=1,descripcion_horas_trabajadas='Tarea3',fecha=str(datetime.date.today() + datetime.timedelta(2)),actividad="Diseño",estado='PRO')
evento_e=str(sebas.id)+"+"+str(p1.id)+"+"+str(rol_equipo.id)+"+"+"HU+"+"A+"+"Se ha agregado '"+str(dhu3.horas_trabajadas)+"' horas a la '"+str(hu1.descripcion)+"' con una descripcion '"+dhu3.descripcion_horas_trabajadas+"' estando en la actividad '"+ dhu3.actividad+ "' con el estado '"+dhu3.estado+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=sebas, fecha_hora=str(datetime.date.today()), objeto=hu1.descripcion, evento=evento_e)

"""Asociar la hu con una descripcion para HU2, mismo que el anterior, estan en el mismo Flujo"""
hu2.hu_descripcion.add(dhu1)
hu2.hu_descripcion.add(dhu2)
hu2.hu_descripcion.add(dhu3)

hu2.estado_en_actividad='PRO'
hu2.actividad=act2
hu2.acumulador_horas=5
hu2.save()

"""Creacion de descripciones para la HU3 Mensaje Finalizado antes de tiempo"""
dhu1=HU_descripcion.objects.create(horas_trabajadas=4,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()+ datetime.timedelta(3)),actividad="Analisis",estado='FIN')
evento_e=str(sebas.id)+"+"+str(p1.id)+"+"+str(rol_equipo.id)+"+"+"HU+"+"A+"+"Se ha agregado '"+str(dhu1.horas_trabajadas)+"' horas a la '"+str(hu1.descripcion)+"' con una descripcion '"+dhu1.descripcion_horas_trabajadas+"' estando en la actividad '"+ dhu1.actividad+ "' con el estado '"+dhu1.estado+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=sebas, fecha_hora=str(datetime.date.today()+ datetime.timedelta(3)), objeto=hu1.descripcion, evento=evento_e)
dhu2=HU_descripcion.objects.create(horas_trabajadas=4,descripcion_horas_trabajadas='Tarea2',fecha=str(datetime.date.today()+ datetime.timedelta(3)),actividad="Diseño",estado='FIN')
evento_e=str(sebas.id)+"+"+str(p1.id)+"+"+str(rol_equipo.id)+"+"+"HU+"+"A+"+"Se ha agregado '"+str(dhu2.horas_trabajadas)+"' horas a la '"+str(hu1.descripcion)+"' con una descripcion '"+dhu2.descripcion_horas_trabajadas+"' estando en la actividad '"+ dhu2.actividad+ "' con el estado '"+dhu2.estado+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=sebas, fecha_hora=str(datetime.date.today()+ datetime.timedelta(3)), objeto=hu1.descripcion, evento=evento_e)
dhu3=HU_descripcion.objects.create(horas_trabajadas=4,descripcion_horas_trabajadas='Tarea3',fecha=str(datetime.date.today() + datetime.timedelta(4)),actividad="Despliegue",estado='FIN')
evento_e=str(sebas.id)+"+"+str(p1.id)+"+"+str(rol_equipo.id)+"+"+"HU+"+"A+"+"Se ha agregado '"+str(dhu3.horas_trabajadas)+"' horas a la '"+str(hu1.descripcion)+"' con una descripcion '"+dhu3.descripcion_horas_trabajadas+"' estando en la actividad '"+ dhu3.actividad+ "' con el estado '"+dhu3.estado+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=sebas, fecha_hora=str(datetime.date.today()+ datetime.timedelta(4)), objeto=hu1.descripcion, evento=evento_e)
dhu4=HU_descripcion.objects.create(horas_trabajadas=2,descripcion_horas_trabajadas='Tarea4',fecha=str(datetime.date.today() + datetime.timedelta(4)),actividad="Desarrollo",estado='FIN')
evento_e=str(sebas.id)+"+"+str(p1.id)+"+"+str(rol_equipo.id)+"+"+"HU+"+"A+"+"Se ha agregado '"+str(dhu4.horas_trabajadas)+"' horas a la '"+str(hu1.descripcion)+"' con una descripcion '"+dhu4.descripcion_horas_trabajadas+"' estando en la actividad '"+ dhu4.actividad+ "' con el estado '"+dhu4.estado+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=sebas, fecha_hora=str(datetime.date.today()+ datetime.timedelta(4)), objeto=hu1.descripcion, evento=evento_e)
dhu5=HU_descripcion.objects.create(horas_trabajadas=4,descripcion_horas_trabajadas='Tarea5',fecha=str(datetime.date.today() + datetime.timedelta(5)),actividad="Prueba",estado='FIN')
evento_e=str(sebas.id)+"+"+str(p1.id)+"+"+str(rol_equipo.id)+"+"+"HU+"+"A+"+"Se ha agregado '"+str(dhu5.horas_trabajadas)+"' horas a la '"+str(hu1.descripcion)+"' con una descripcion '"+dhu5.descripcion_horas_trabajadas+"' estando en la actividad '"+ dhu5.actividad+ "' con el estado '"+dhu5.estado+"' con fecha y hora: "+str(datetime.date.today())
historial_notificacion.objects.create(usuario=sebas, fecha_hora=str(datetime.date.today()+ datetime.timedelta(5)), objeto=hu1.descripcion, evento=evento_e)

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

"""--------------------------------------Creacion de un Sprint finalizado correctamente SPRINT_FIN-----------------------------------"""
#este va a ser el finalizado correctamente, con hus nuevas que tengo que crear
spF=Sprint.objects.create(descripcion='sprint_fin',fecha_inicio=str(datetime.date.today()-datetime.timedelta(days=15)),duracion=7,estado='FIN',proyecto=p2)

"""Agregar hus a los sprint creados"""
spF.hu.add(hu22,hu23,hu24,hu25,hu26,hu27,hu28,hu29,hu30,hu31,hu32)

"""Agregar hus a los sprint creados"""
spF.flujo.add(f1,f2,f3)

"""Agregar el quipo a los sprint creados"""
spF.equipo.add(delsy,gabriela,valeria)

"""Clasificar esas hus seleccionadas en flujos"""
#hu 22,23,24,25 en flujo 1 , 26,27,28 en flujo y 29,30,31,32 en el flujo3
hu22Flujo1=asignaHU_actividad_flujo.objects.create(flujo_al_que_pertenece=f1)
hu22Flujo1.lista_de_HU.add(hu22,hu23,hu24,hu25)
hu22Flujo1.save()
hu26Flujo2=asignaHU_actividad_flujo.objects.create(flujo_al_que_pertenece=f2)
hu26Flujo2.lista_de_HU.add(hu26,hu27,hu28)
hu26Flujo2.save()
hu29Flujo3=asignaHU_actividad_flujo.objects.create(flujo_al_que_pertenece=f3)
hu29Flujo3.lista_de_HU.add(hu29,hu30,hu31,hu32)
hu29Flujo3.save()

delegacion.objects.create(usuario=delsy,hu=hu22)
delegacion.objects.create(usuario=delsy,hu=hu23)
delegacion.objects.create(usuario=delsy,hu=hu24)
delegacion.objects.create(usuario=delsy,hu=hu25)
delegacion.objects.create(usuario=gabriela,hu=hu26)
delegacion.objects.create(usuario=gabriela,hu=hu27)
delegacion.objects.create(usuario=gabriela,hu=hu28)
delegacion.objects.create(usuario=valeria,hu=hu29)
delegacion.objects.create(usuario=valeria,hu=hu30)
delegacion.objects.create(usuario=valeria,hu=hu31)
delegacion.objects.create(usuario=valeria,hu=hu32)

#Creacion y asignacion de descripciones de hu 22, 23,24,25
dhu221=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Analisis",estado='PRO')
dhu222=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Disenho",estado='PRO')
dhu223=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Despliegue",estado='PRO')
dhu224=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Desarrollo",estado='PRO')
dhu225=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Prueba",estado='PRO')
hu22.hu_descripcion.add(dhu221)
hu22.hu_descripcion.add(dhu222)
hu22.hu_descripcion.add(dhu223)
hu22.hu_descripcion.add(dhu224)
hu22.hu_descripcion.add(dhu225)
hu22.actividad=act1
hu22.acumulador_horas=15
hu22.save()

"""Coloco en los campos estado y actividad de la HU a la que cargamos las descripciones los datos correctos segun la descripcion agregada"""
hu22.estado_en_actividad='APR'
hu22.actividad=act1
hu22.acumulador_horas=15
hu22.save()


dhu231=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Analisis",estado='PRO')
dhu232=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Disenho",estado='PRO')
dhu233=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Despliegue",estado='PRO')
dhu234=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Desarrollo",estado='PRO')
dhu235=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Prueba",estado='PRO')
hu23.hu_descripcion.add(dhu231)
hu23.hu_descripcion.add(dhu232)
hu23.hu_descripcion.add(dhu233)
hu23.hu_descripcion.add(dhu234)
hu23.hu_descripcion.add(dhu235)
hu23.actividad=act1
hu23.acumulador_horas=15
hu23.save()


"""Coloco en los campos estado y actividad de la HU a la que cargamos las descripciones los datos correctos segun la descripcion agregada"""
hu23.estado_en_actividad='APR'
hu23.actividad=act1
hu23.acumulador_horas=15
hu23.save()


dhu241=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Analisis",estado='PRO')
dhu242=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Disenho",estado='PRO')
dhu243=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Despliegue",estado='PRO')
dhu244=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Desarrollo",estado='PRO')
dhu245=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Prueba",estado='PRO')
hu24.hu_descripcion.add(dhu241)
hu24.hu_descripcion.add(dhu242)
hu24.hu_descripcion.add(dhu243)
hu24.hu_descripcion.add(dhu244)
hu24.hu_descripcion.add(dhu245)
hu24.actividad=act1
hu24.acumulador_horas=15
hu24.save()


"""Coloco en los campos estado y actividad de la HU a la que cargamos las descripciones los datos correctos segun la descripcion agregada"""
hu24.estado_en_actividad='APR'
hu24.actividad=act1
hu24.acumulador_horas=15
hu24.save()


dhu251=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Analisis",estado='PRO')
dhu252=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="diseño",estado='PRO')
dhu253=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Despliegue",estado='PRO')
dhu254=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="desarrollo",estado='PRO')
dhu255=HU_descripcion.objects.create(horas_trabajadas=3,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="prueba",estado='PRO')
hu25.hu_descripcion.add(dhu251)
hu25.hu_descripcion.add(dhu252)
hu25.hu_descripcion.add(dhu253)
hu25.hu_descripcion.add(dhu254)
hu25.hu_descripcion.add(dhu255)
hu25.actividad=act1
hu25.acumulador_horas=15
hu25.save()


"""Coloco en los campos estado y actividad de la HU a la que cargamos las descripciones los datos correctos segun la descripcion agregada"""
hu25.estado_en_actividad='APR'
hu25.actividad=act1
hu25.acumulador_horas=15
hu25.save()

#Creacion y asignacion de descripciones de hu 26,27,28
dhu261=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Relevamiento",estado='PRO')
dhu262=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Implementacion",estado='PRO')
dhu263=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Control",estado='PRO')
hu26.hu_descripcion.add(dhu261)
hu26.hu_descripcion.add(dhu262)
hu26.hu_descripcion.add(dhu263)
hu26.actividad=act6
hu26.acumulador_horas=15
hu26.save()


"""Coloco en los campos estado y actividad de la HU a la que cargamos las descripciones los datos correctos segun la descripcion agregada"""
hu26.estado_en_actividad='APR'
hu26.actividad=act6
hu26.acumulador_horas=15
hu26.save()


dhu271=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Relevamiento",estado='PRO')
dhu272=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Implementacion",estado='PRO')
dhu273=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Control",estado='PRO')
hu27.hu_descripcion.add(dhu271)
hu27.hu_descripcion.add(dhu272)
hu27.hu_descripcion.add(dhu273)
hu27.actividad=act6
hu27.acumulador_horas=15
hu27.save()


"""Coloco en los campos estado y actividad de la HU a la que cargamos las descripciones los datos correctos segun la descripcion agregada"""
hu27.estado_en_actividad='APR'
hu27.actividad=act6
hu27.acumulador_horas=15
hu27.save()


dhu281=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Relevamiento",estado='PRO')
dhu282=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Implementacion",estado='PRO')
dhu283=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Control",estado='PRO')
hu28.hu_descripcion.add(dhu281)
hu28.hu_descripcion.add(dhu282)
hu28.hu_descripcion.add(dhu283)
hu28.actividad=act8
hu28.acumulador_horas=15
hu28.save()

"""Coloco en los campos estado y actividad de la HU a la que cargamos las descripciones los datos correctos segun la descripcion agregada"""
hu28.estado_en_actividad='APR'
hu28.actividad=act6
hu28.acumulador_horas=15
hu28.save()


#Creacion y asignacion de descripciones de hu 29,30,31,32
dhu291=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Relevamiento",estado='PRO')
dhu292=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Disenho",estado='PRO')
dhu293=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Desarrollo",estado='PRO')
dhu294=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Control",estado='PRO')
hu29.hu_descripcion.add(dhu291)
hu29.hu_descripcion.add(dhu292)
hu29.hu_descripcion.add(dhu293)
hu29.hu_descripcion.add(dhu294)
hu29.actividad=act6
hu29.acumulador_horas=15
hu29.save()

"""Coloco en los campos estado y actividad de la HU a la que cargamos las descripciones los datos correctos segun la descripcion agregada"""
hu29.estado_en_actividad='APR'
hu29.actividad=act6
hu29.acumulador_horas=15
hu29.save()


dhu301=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Relevamiento",estado='PRO')
dhu302=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Disenho",estado='PRO')
dhu303=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Desarrollo",estado='PRO')
dhu304=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Control",estado='PRO')
hu30.hu_descripcion.add(dhu301)
hu30.hu_descripcion.add(dhu302)
hu30.hu_descripcion.add(dhu303)
hu30.hu_descripcion.add(dhu304)
hu30.actividad=act8
hu30.acumulador_horas=15
hu30.save()

"""Coloco en los campos estado y actividad de la HU a la que cargamos las descripciones los datos correctos segun la descripcion agregada"""
hu30.estado_en_actividad='APR'
hu30.actividad=act6
hu30.acumulador_horas=15
hu30.save()


dhu311=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Relevamiento",estado='PRO')
dhu312=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Disenho",estado='PRO')
dhu313=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Desarrollo",estado='PRO')
dhu314=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Control",estado='PRO')
hu31.hu_descripcion.add(dhu311)
hu31.hu_descripcion.add(dhu312)
hu31.hu_descripcion.add(dhu313)
hu31.hu_descripcion.add(dhu314)
hu31.actividad=act6
hu31.acumulador_horas=15
hu31.save()

"""Coloco en los campos estado y actividad de la HU a la que cargamos las descripciones los datos correctos segun la descripcion agregada"""
hu31.estado_en_actividad='APR'
hu31.actividad=act6
hu31.acumulador_horas=15
hu31.save()

dhu321=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Relevamiento",estado='PRO')
dhu322=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Disenho",estado='PRO')
dhu323=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Desarrollo",estado='PRO')
dhu324=HU_descripcion.objects.create(horas_trabajadas=5,descripcion_horas_trabajadas='Tarea1',fecha=str(datetime.date.today()),actividad="Control",estado='PRO')
hu32.hu_descripcion.add(dhu321)
hu32.hu_descripcion.add(dhu322)
hu32.hu_descripcion.add(dhu323)
hu32.hu_descripcion.add(dhu324)
hu32.actividad=act6
hu32.acumulador_horas=15
hu32.save()

"""Coloco en los campos estado y actividad de la HU a la que cargamos las descripciones los datos correctos segun la descripcion agregada"""
hu32.estado_en_actividad='APR'
hu32.actividad=act6
hu32.acumulador_horas=15
hu32.save()