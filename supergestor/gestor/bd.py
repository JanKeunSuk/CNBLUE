#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2

#Establecemos la conexion con la base de datos
conexion = psycopg2.connect("dbname=prueba5 host=localhost port=5432 user=seba2 password=seba2")

#Preparamos el cursor que nos va a ayudar a realizar las operaciones con la base de datos
cur=conexion.cursor()


#Correos permitidos
# Preparamos el query SQL para insertar un registro en la BD
c="insert into gestor_permitido (email) values ('admin@gmail.com');"
# Ejecutamos un query SQL usando el método execute() que nos proporciona el cursor
cur.execute(c)
c="insert into gestor_permitido (email) values ('delsy.denis.21@gmail.com');"
cur.execute(c)
c="insert into gestor_permitido (email) values ('katherinevera94@gmail.com');"
cur.execute(c)
c="insert into gestor_permitido (email) values ('gsebacatt@gmail.com');"
cur.execute(c)
#Efectuamos los cambios en la base de datos
conexion.commit()

#Carga de usuarios
#contraseña: admin
c="insert into gestor_myuser (password,last_login,username, user_name, last_name, direccion, is_active, is_admin, email_id) values ('pbkdf2_sha256$15000$5PUgdTbag7Cm$kbLmrEL+pT+iWKraH4+8Kq6aVL9bA5wDHkFFYiRlogI=','2015-03-31 09:16:23.277637-04','admin','admin','admin', 'Asuncion', 'TRUE', 'TRUE','admin@gmail.com');"
cur.execute(c)
#contraseña: 1234
c="insert into gestor_myuser (password,last_login,username, user_name, last_name, direccion, is_active, is_admin, email_id) values ('pbkdf2_sha256$15000$4FMgo6Ef1xDS$Jmf7hATzgtfttaXHMKBeac/pap4+DExO6fjP4qtS0S8=','2015-03-31 09:16:23.277637-04','delsy','delsy','denis', 'Asuncion', 'TRUE', 'FALSE','delsy.denis.21@gmail.com');"
cur.execute(c)
#contraseña: 1234
c="insert into gestor_myuser (password,last_login,username, user_name, last_name, direccion, is_active, is_admin, email_id) values ('pbkdf2_sha256$15000$iJm8i4VvYLBq$QZBdHrTW23XNbh8JB0XPUFVd7ckUJxa0ZbDC6GYJuoI=','2015-03-31 09:16:23.277637-04','katherine','katherine','vera', 'Asuncion', 'TRUE', 'FALSE','katherinevera94@gmail.com');"
cur.execute(c)
#contraseña: 1234
c="insert into gestor_myuser (password,last_login,username, user_name, last_name, direccion, is_active, is_admin, email_id) values ('pbkdf2_sha256$15000$Wwp6bhAeZDZv$d82uJ3SqwA08rtuY4Vm91tvT27KPkL5kF/YJ3Z3bzI8=','2015-03-31 09:16:23.277637-04','sebas','sebas','sebas', 'Asuncion', 'TRUE', 'FALSE','gsebacatt@gmail.com');"
cur.execute(c)

conexion.commit()
#carga de Proyecto
c="insert into gestor_proyecto (nombre_corto, nombre_largo, descripcion, fecha_inicio, fecha_fin, estado) values ('p1','proyecto1', 'proyecto1','2015-03-31','2015-04-01', 'PEN');"
cur.execute(c)
c="insert into gestor_proyecto (nombre_corto, nombre_largo, descripcion, fecha_inicio, fecha_fin, estado) values ('p2','proyecto2', 'proyecto2','2015-03-31','2015-04-01', 'PEN');"
cur.execute(c)
c="insert into gestor_proyecto (nombre_corto, nombre_largo, descripcion, fecha_inicio, fecha_fin, estado) values ('p3','proyecto3', 'proyecto3','2015-03-31','2015-04-01', 'PEN');"
cur.execute(c)
c="insert into gestor_proyecto (nombre_corto, nombre_largo, descripcion, fecha_inicio, fecha_fin, estado) values ('p4','proyecto4', 'proyecto4','2015-03-31','2015-04-01', 'PEN');"
cur.execute(c)

#Carga de Rol de Sistema
c="insert into gestor_rol_sistema (nombre_rol_id, descripcion) values ('admin', 'admin tiene todos los permisos');"
cur.execute(c)
#Carga de Rol
c="insert into gestor_rol (nombre_rol_id, descripcion, usuario_creador_id) values ('Srum Master','permisos adqueridos por el ScrumMaster','1');"
cur.execute(c)
c="insert into gestor_rol (nombre_rol_id, descripcion, usuario_creador_id) values ('Product Owner','permisos adqueridos por el ProductOwner','1');"
cur.execute(c)
c="insert into gestor_rol (nombre_rol_id, descripcion, usuario_creador_id) values ('Equipo','permisos adqueridos por el Equipo','1');"
cur.execute(c)
c="insert into gestor_rol (nombre_rol_id, descripcion, usuario_creador_id) values ('Cliente','permisos adqueridos por el Cliente','1');"
cur.execute(c)
conexion.commit()

#Carga de Permisos del Rol
#SRUM MASTER
#Administracion rol
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','22');"
cur.execute(c)
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','23');"
cur.execute(c)
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','24');"
cur.execute(c)
#Administracion HU
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','28');"
cur.execute(c)
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','29');"
cur.execute(c)
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','30');"
cur.execute(c)
#Administracion sprint
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','31');"
cur.execute(c)
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','32');"
cur.execute(c)
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','33');"
cur.execute(c)
#Administracion Flujo
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','37');"
cur.execute(c)
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','38');"
cur.execute(c)
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','39');"
cur.execute(c)
#Administracion Proyecto
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','43');"
cur.execute(c)
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','44');"
cur.execute(c)
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','45');"
cur.execute(c)
#Asignacion
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','46');"
cur.execute(c)
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','47');"
cur.execute(c)
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('1','48');"
cur.execute(c)
#PRODUCT OWNER
#Administracion sprint
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('2','31');"
cur.execute(c)
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('2','32');"
cur.execute(c)
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('2','33');"
cur.execute(c)
#EQUIPO
#Modificar sprint
c="insert into gestor_rol_permisos (rol_id, permission_id) values ('3','32');"
cur.execute(c)
#EQUIPO

conexion.commit()

#Carga de Permisos del Rol de Sistema
#Tiene todos los permisos
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','1');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','2');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','3');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','4');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','5');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','6');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','7');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','8');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','9');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','10');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','11');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','12');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','13');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','14');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','15');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','16');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','17');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','18');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','19');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','20');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','21');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','22');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','23');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','24');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','25');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','26');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','27');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','28');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','29');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','30');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','31');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','32');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','33');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','34');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','35');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','36');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','37');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','38');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','39');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','40');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','41');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','42');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','43');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','44');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','45');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','46');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','47');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','48');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','49');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','50');"
cur.execute(c)
c="insert into gestor_rol_sistema_permisos (rol_id, permission_id) values ('1','51');"
cur.execute(c)
conexion.commit()

#Carga actividades
c="insert into gestor_actividades (nombre, descripcion) values ('Analisis','analisis');"
cur.execute(c)
c="insert into gestor_actividades (nombre, descripcion) values ('Diseño','diseño');"
cur.execute(c)
c="insert into gestor_actividades (nombre, descripcion) values ('Despliegue','despliegue');"
cur.execute(c)
conexion.commit()

#Cargar Flujos
c="insert into gestor_flujo (nombre, estado) values ('Flujo1','ACT');"
cur.execute(c)
c="insert into gestor_flujo (nombre, estado) values ('Flujo2','ACT');"
cur.execute(c)
c="insert into gestor_flujo (nombre, estado) values ('Flujo3','ACT');"
cur.execute(c)
conexion.commit()

#carga de Proyecto Flujo
c="insert into gestor_proyecto_flujo (proyecto_id, flujo_id) values ('1','1');"
cur.execute(c)
conexion.commit()

#creacion de HU
c="insert into gestor_HU (descripcion, valor_negocio, valor_tecnico, prioridad, duracion, acumulador_horas, estado, estado_en_actividad, proyecto) values ('HU1', '3', '0', '0', '0', '0', 'ACT', 'PEN', '1');"
cur.execute(c)
c="insert into gestor_HU (descripcion, valor_negocio, valor_tecnico, prioridad, duracion, acumulador_horas, estado, estado_en_actividad, proyecto) values ('HU2', '5', '0', '0', '0', '0', 'ACT', 'PEN', '1');"
cur.execute(c)
c="insert into gestor_HU (descripcion, valor_negocio, valor_tecnico, prioridad, duracion, acumulador_horas, estado, estado_en_actividad, proyecto) values ('HU3', '8', '0', '0', '0', '0', 'ACT', 'PEN', '1');"
cur.execute(c)

#creacion de sprint
c="insert into gestor_sprint (descripcion, fecha_inicio, duracion, estado) values ('sprint1', '2015-04-18 20:00:00-04', '2', 'ACT');"
cur.execute(c)
c="insert into gestor_sprint (descripcion, fecha_inicio, duracion, estado) values ('sprint2', '2015-04-18 20:05:00-04', '2', 'ACT');"
cur.execute(c)
c="insert into gestor_sprint (descripcion, fecha_inicio, duracion, estado) values ('sprint3', '2015-04-18 20:10:00-04', '2', 'ACT');"
cur.execute(c)

#Efectuamos los cambios en la base de datos
conexion.commit()
#Cerramos el cursor
cur.close()
#Cerramos la conexion con la base de datos
conexion.close()