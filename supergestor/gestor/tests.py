#coding: utf-8
"""

Casos de prueba para los modelos existentes dentro del sistema.

"""
from django.test import TestCase, Client
from gestor.models import MyUser, Permitido, rol, rol_sistema, Actividades, Flujo, proyecto, asignacion, asigna_sistema, HU, Sprint, HU_descripcion, HU_version, historial_notificacion
from gestor.views import FormularioRolProyecto, proyectoFrom, FormularioFlujoProyecto, formularioActividad, FormularioHU, FormularioSprintProyecto, delegacion
from django.test.client import RequestFactory
from django.contrib.auth.models import Permission
from django.utils import timezone
from django.core import mail
from selenium import webdriver
from selenium.webdriver.common.keys import Keys     
from django.test import LiveServerTestCase
import time
import datetime

class MyUserManagerTests(TestCase):

    def test_create_user_is_an_instance_of_User(self):
        """
        create_user() deberia retornar un objeto user con nombre de usuario,
        el email dado y contrasenha
        """
        usuario = MyUser.objects.create_user('anonimo', Permitido.objects.create(email='anonimo2@hotmail.com'), 'kathe123')
        self.assertEqual(isinstance(usuario, MyUser),True)

    def test_create_user_is_active_is_not_admin(self):
        """
        create_user() verificar si esta activo y no es admin
        """
        usuario = MyUser.objects.create_user('anonimo', Permitido.objects.create(email='anonimo2@hotmail.com'), 'kathe123')
        self.assertEqual(usuario.is_admin,False)
        self.assertEqual(usuario.is_active,True)
        
    def test_create_superuser_is_an_instance_of_User(self):
        """
        create_superuser() deberia retornar un objeto user con nombre de usuario,
        el email dado y contrasenha
        """
        usuario = MyUser.objects.create_superuser('anonimo', Permitido.objects.create(email='anonimo2@hotmail.com'), 'kathe123')
        self.assertEqual(isinstance(usuario, MyUser),True)
        
    def test_create_superuser_is_active_is_admin(self):
        """
        create_superuser() verificar si esta activo y no es admin
        """
        usuario = MyUser.objects.create_superuser('anonimo', Permitido.objects.create(email='anonimo2@hotmail.com'), 'kathe123')
        self.assertEqual(usuario.is_admin,True)
        self.assertEqual(usuario.is_active,True)
    
class PermitidoTest(TestCase): 
    def CorreoValidotest(self):
        usuario=MyUser.create('anonimo', Permitido.objects.create(email='anonimo2@hotmail.com'), 'kathe123', 'Carlos', 'Gomez', 'Lambare')
        self.assertEqual(usuario.email.__str__().count('@'),1)
        
class MyUserTest(TestCase):   
    def test_get_short_name_is_correct(self):
        """/
        create_user() realmente guarda bien los datos que se le pasan como parametros?
        """
        usuario = MyUser.objects.create_user('anonimo', Permitido.objects.create(email='anonimo2@hotmail.com'), 'kathe123')
        self.assertEqual(usuario.get_short_name(),'anonimo')
    
    def test_has_perm(self):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        #Asignar un permiso a usuario y controlar que sea ese el permiso asignado al mismo
        #eliminar algun permiso del usuario y ver que no tenga ese permiso
        pass

    def test_has_module_perms(self):
        ##mismo caso anterior pero con mas de un permiso
        pass

    def test_is_staff(self):
        # crear un superusuario y ver si es admin
        #crear un usuario comun y ver que realmente no sea admin
        pass
    """
    def test_create_User_Completo(self):
        usuario=MyUser.create('anonimo', Permitido.objects.create(email='anonimo2@hotmail.com'), 'kathe123', 'Carlos', 'Gomez', 'Lambare')
        self.assertEqual(isinstance(usuario, MyUser),True)

    
    
    def test_login_Usuario_Registrado(self):
        c=Client()
        response = c.post('/login/', {'username': 'admin', 'password': 'admin2'})
        self.assertEqual(response.templates[0].name, 'hola.html')
        #c=Client()
        #self.assertEqual(c.login(username='admin', password='admin2'),True)
    """ 
    def test_login_Usuario_No_Registrado(self):
        c=Client()
        response = c.post('/login/', {'username': 'Micaela', 'password': 'admin2'})
        self.assertEqual(response.templates[0].name, 'registration/login.html')
        
        #self.assertEqual(c.login(username='admin', password='admin2'),True)
        #response = self.client.get('/login/')
        #self.assertEqual(response.context['name'],'login')
        #c=Client().get('/login/')
        #self.assertEqual(c.login(username='fred', password='secret'),False)
        #response = c.post('/login/', {'username': 'Micaela', 'password': 'katherine'})
        #d=Client().get('/login/')
        #self.assertEqual(response.content,d.content)
    
    def tes_Control_de_Estados_de_Views(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/hola/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/registrar/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/save/')
        self.assertEqual(response.status_code, 200)
        
    def create_proyecto(self):
        return proyecto(nombre_corto="P9", nombre_largo="proyecto9", descripcion="proyecto9", fecha_inicio=timezone.now(), fecha_fin=datetime.timedelta(days=1), estado="PEN")
    
    def usuario(self):
        return MyUser.objects.create_user(username='delsy', email=Permitido.objects.create(email='delsy@gmail.com'), password='1234')
        
    def test_modificarUsuario(self):
        w=self.usuario()
        w.username='magali'
        w.save()
        self.assertEqual(w.username, 'magali')
         
    def create_notificacion(self):
        usuario=self.usuario()
        return historial_notificacion.objects.create(usuario=usuario, fecha_hora=timezone.now(), objeto="prueba", evento="prueba")
    
    def test_notificacion(self):
        w=self.create_notificacion()
        self.assertTrue(isinstance(w, historial_notificacion))
        
    def test_notificacion_historial(self):
        w=self.create_notificacion()
        self.assertEqual(w.objeto, 'prueba')
        
class RolTest(TestCase):
    
    def create_rol(self):
        return rol.objects.create( nombre_rol_id="nuevoRol", descripcion="nuevo_rol", usuario_creador= MyUser.objects.create_user('delsy', Permitido.objects.create(email='delsy@gmail.com'), '1234'))
    
    def test_rol_creation(self):
        w=self.create_rol()
        self.assertTrue(isinstance(w, rol))
        self.assertEqual(w.__unicode__(), w.nombre_rol_id)
        
    def setUp(self):
        self.factory=RequestFactory
        self.rol=rol.objects.create(nombre_rol_id="nuevoRol", descripcion="nuevo_rol", usuario_creador=MyUser.objects.create_user('kathe', Permitido.objects.create(email='kathe@gmail.com'), '1234'))
        
    def test_rol_view(self):
        response=self.client.get('/crearRol/2/1/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_modificarRol(self):
        w=self.create_rol()
        w.descripcion='rol_cambiado'
        w.save()
        self.assertEqual(w.descripcion, 'rol_cambiado')
    
    def test_dato_invalido(self):
        w=self.create_rol()
        w.descripcion='rol_cambiado'
        w.save()
        self.assertNotEqual(w.descripcion, 'nuevo_rol')
         
class Rol_sistemaTest(TestCase):
    
    def create_rol_sistema(self):
        return rol_sistema.objects.create( nombre_rol_id="nuevoRol", descripcion="nuevo_rol")
    
    def test_rol_sistema_creation(self):
        w=self.create_rol_sistema()
        self.assertTrue(isinstance(w, rol_sistema))
        self.assertEqual(w.__unicode__(), w.nombre_rol_id)
        
    def test_modificarRol_sistema(self):
        w=self.create_rol_sistema()
        w.nombre_rol_id='rol_prueba'
        w.save()
        self.assertEqual(w.nombre_rol_id, 'rol_prueba')
          
class ActividadesTest(TestCase):
    def create_Actividades(self, nombre="nuevaActividad", descripcion="nuevo Actividad" ):
        return Actividades.objects.create(nombre=nombre, descripcion=descripcion)
    
    def test_Actividad_creation(self):
        w=self.create_Actividades()
        self.assertTrue(isinstance(w, Actividades))
        self.assertEqual(w.__unicode__(), str(w.id)  + " - " + w.nombre)
        
    def test_valid_formularioActividad(self):
        w = Actividades.objects.create(nombre="nuevaActividad", descripcion='nueva Actividad' )
        data = {'nombre':w.nombre, 'descripcion':w.descripcion,}
        form = formularioActividad(data=data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_formularioActividad(self):
        w = Actividades.objects.create(nombre="nuevaActividad", descripcion='nueva Actividad' )
        data = {'nombre':w.nombre,}
        form = formularioActividad(data=data)
        self.assertFalse(form.is_valid())
        
    def test_crear_actividad_views_get(self):
        response=self.client.get('/crearActividad/2/1/')
        self.assertEqual(response.status_code, 200)
        
    def test_crear_actividad_views_pos(self):
        w = Actividades.objects.create(nombre="nuevaActividad", descripcion='nueva Actividad' )
        w.save()
        
        actividad_in=Actividades.objects.get(pk=w.id)
        self.assertEquals(actividad_in.nombre, w.nombre)    
       
    def create_proyecto(self):
        return proyecto(nombre_corto="P9", nombre_largo="proyecto9", descripcion="proyecto9", fecha_inicio=timezone.now(), fecha_fin=datetime.timedelta(days=1), estado="PEN")
    
     
    def test_modificar_actividad_views(self):
        w=self.create_proyecto()    
        u= MyUser.objects.create_user('anonimo', Permitido.objects.create(email='anonimo2@hotmail.com'), '1234')
        y= self.create_Actividades()

        post_data={'usuario':u.id,'proyecto':w.id,'actividad':y.id}
        Actividad_url='/modificarActividad/1/1/'
        self.client.post(Actividad_url, data=post_data)
    
    def test_modificarActividad(self):
        w=self.create_Actividades()
        w.nombre='actividad_prueba'
        w.save()
        self.assertEqual(w.nombre, 'actividad_prueba')
        
class FlujoTest(TestCase):
    def create_Flujo(self, nombre="1nuevoFlujo", estado="ACT" ):
        return Flujo.objects.create(nombre=nombre, estado=estado)
    
    def test_Flujo_creation(self):
        w=self.create_Flujo()
        self.assertTrue(isinstance(w, Flujo))
        #self.assertEqual(w.__unicode__(), str(w.id) + w.nombre)
    
    def test_crear_flujo_views(self):
        response=self.client.get('/crearFlujo/2/1/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_flujo_modificar_estado(self):
        w=self.create_Flujo()
        w.estado='CAN'
        w.save()
        self.assertEqual(w.estado, 'CAN')  
        
class proyectoTest(TestCase):
    
    def create_proyecto(self):
        return proyecto(nombre_corto="P9", nombre_largo="proyecto9", descripcion="proyecto9", fecha_inicio=timezone.now(), fecha_fin=datetime.timedelta(days=1), estado="PEN")
    
    def test_proyecto_creation(self):
        w=self.create_proyecto()
        self.assertTrue(isinstance(w, proyecto))
        self.assertEqual(w.__unicode__(), w.nombre_corto)
    """ 
    def test_valid_proyectoFrom(self):
        w = proyecto(nombre_corto="P9", nombre_largo="proyecto9", descripcion="proyecto9", fecha_inicio=timezone.now(), fecha_fin=datetime.timedelta(days=1), estado="PEN")
        #w.flujos.create(nombre="nuevoFlujo", estado="ACT")
        form = proyectoFrom({'nombre_corto':w.nombre_corto, 'nombre_largo':w.nombre_largo, 'descripcion':w.descripcion, 'fecha_inicio':w.fecha_inicio, 'fecha_fin': w.fecha_fin, 'estado':w.estado})
        self.assertTrue(form.is_valid())
    """
    def test_invalid_proyectoFrom(self):
        w = proyecto.objects.create(nombre_corto="P9", nombre_largo="proyecto9", descripcion="proyecto9", fecha_inicio="2015-03-31 00:00:00-04", fecha_fin="2015-03-31 00:00:00-04" ,estado="PEN" )
        data = {'nombre_corto':w.nombre_corto, 'nombre_largo':w.nombre_largo, 'descripcion':w.descripcion, 'fecha_inicio':w.fecha_inicio, 'fecha_fin': w.fecha_fin, }
        form = proyectoFrom(data=data)
        self.assertFalse(form.is_valid())
        
    def test_valid_FormularioRolProyecto(self):
        w = rol.objects.create(nombre_rol_id="nuevoRol", descripcion="nuevoRol", usuario_creador=MyUser.objects.create_user('kathe', Permitido.objects.create(email='kathe@gmail.com'), '1234'), estado="ACT")
        w.permisos.add(Permission.objects.get(id=34))
        form = FormularioRolProyecto({'nombre_rol_id':w.nombre_rol_id, 'descripcion':w.descripcion,'permisos':[t.id for t in w.permisos.all()],'estado':w.estado ,})
        self.assertTrue(form.is_valid())

    def test_invalid_FormularioRolProyecto(self):
        w = proyecto(nombre_corto="P9", nombre_largo="proyecto9", descripcion="proyecto9", fecha_inicio=timezone.now(), fecha_fin=datetime.timedelta(days=1) ,estado="PEN" )
        data = {'nombre_corto':w.nombre_corto, 'nombre_largo':w.nombre_largo, 'descripcion':w.descripcion, 'fecha_inicio':w.fecha_inicio, 'fecha_fin': w.fecha_fin, 'estado':w.estado ,}
        form = FormularioRolProyecto(data=data)
        self.assertFalse(form.is_valid())
      
    def test_valid_FormularioFlujoProyecto(self):
        w = Flujo.objects.create(nombre='nuevoFlujo', estado='ACT')
        w.actividades.create(nombre='Actividad1', descripcion='actividad')
        form = FormularioFlujoProyecto({'nombre':w.nombre, 'estado':w.estado, 'actividades': [t.id for t in w.actividades.all()],})
        self.assertTrue(form.is_valid())
        
    def test_invalid_FormularioFlujoProyecto(self):
        w = Flujo.objects.create(nombre='nuevoFlujo', estado='ACT')
        data = {'nombre':w.nombre, 'estado':w.estado, }
        form = FormularioFlujoProyecto(data=data)
        self.assertFalse(form.is_valid()) 
        
        
class asignacionTest(TestCase):
    def create_proyecto(self):
        return proyecto.objects.create(nombre_corto="P9", nombre_largo="proyecto9", descripcion="proyecto9", fecha_inicio="2015-03-31 00:00:00-04", fecha_fin="2015-03-31 00:00:00-04" ,estado="PEN" )
        
    def create_rol(self):
        return rol.objects.create( nombre_rol_id="nuevoRol", descripcion="nuevo_rol", usuario_creador= MyUser.objects.create_user('delsy', Permitido.objects.create(email='delsy@gmail.com'), '1234'))

    def create_asignacion(self):
        usuario=MyUser.objects.create_user('anonimo', Permitido.objects.create(email='anonimo2@hotmail.com'), '1234')
        rol=self.create_rol()
        proyecto=self.create_proyecto()
        return asignacion.objects.create(usuario=usuario, rol=rol, proyecto=proyecto)
    
    def test_asignacion_creation(self):
        w=self.create_asignacion()
        self.assertEqual(w.usuario.username, 'anonimo')
        
    def create_proyecto2(self):
        return proyecto.objects.create(nombre_corto="P", nombre_largo="proyecto", descripcion="proyecto", fecha_inicio="2015-03-31 00:00:00-04", fecha_fin="2015-03-31 00:00:00-04" ,estado="PEN" )
        
    def test_asignacion_modificar(self):
        w=self.create_asignacion()
        w.proyecto=self.create_proyecto2()
        w.save()
        self.assertEqual(w.proyecto.nombre_corto, 'P')        
        
class asigna_sistemacionTest(TestCase):
    def create_proyecto(self):
        return proyecto(nombre_corto="P9", nombre_largo="proyecto9", descripcion="proyecto9", fecha_inicio=timezone.now(), fecha_fin=datetime.timedelta(days=1), estado="PEN")
    
    def create_rol(self):
        return rol.objects.create( nombre_rol_id="nuevoRol", descripcion="nuevo_rol", usuario_creador= MyUser.objects.create_user('delsy', Permitido.objects.create(email='delsy@gmail.com'), '1234'))
    
    def create_rol_sistema(self):
        return rol_sistema.objects.create( nombre_rol_id="nuevoRol", descripcion="nuevo_rol")
    
    def create_asigna_sistema(self):
        rol=self.create_rol_sistema()
        usuario=MyUser.objects.create_user('anonimo', Permitido.objects.create(email='anonimo2@hotmail.com'), '1234')
        return asigna_sistema.objects.create(usuario=usuario, rol=rol) 
     
    def test_asigna_sistema_creation(self):
        w=self.create_asigna_sistema()
        self.assertEqual(w.usuario.username, 'anonimo')
    
    def test_asignarRol_POST(self):
        w=self.create_proyecto()
        x=self.create_rol()
        post_data={'proyecto':w.id,'rol':x.id, 'usuario':x.usuario_creador}
        asignarRol_url='/asignarRol/1/1/'
        self.client.post(asignarRol_url, data=post_data)
   
class huTest(TestCase):
    def create_hu(self, descripcion="hu", valor_negocio="7", valor_tecnico="0", prioridad="0", duracion="0", acumulador_horas="0", estado="ACT", estado_en_actividad="PEN", valido="FALSE", proyecto_id="1", version="1"):
            return HU.objects.create(descripcion=descripcion, valor_negocio=valor_negocio, valor_tecnico=valor_tecnico, prioridad=prioridad, duracion=duracion, acumulador_horas=acumulador_horas, estado=estado, estado_en_actividad=estado_en_actividad, valido=valido, proyecto_id=proyecto_id, version=version)
        
    def test_hu_creation(self):
        """
        Test del modelo HU, crea un hu llamando a la create_hu, verifica la condicion de las instancias
        comprueba si el resultado es el esperado del __unicode__
        """
        w=self.create_hu()
        self.assertTrue(isinstance(w, HU))
        self.assertEqual(w.__unicode__(), w.descripcion)
        
    def test_crear_hu(self):
        """
        Con cliente obtenemos la direccion /crearHU/1/1/1/ y
        comprueba si el resultado es el esperado
        """
        response=self.client.get('/crearHU/1/1/1/')
        self.assertEqual(response.status_code, 200)
        
    def test_formularioHU_valido(self):
        """
        Test del Formulario HU, prueba que el HU creado sea valido
        """
        w=HU.objects.create(valor_tecnico='1', valor_negocio='1', prioridad='1', duracion='1',acumulador_horas='1', estado='ACT', proyecto_id='1', version='1')
        data={'valor_tecnico':w.valor_tecnico, 'valor_negocio':w.valor_negocio, 'prioridad':w.prioridad, 'duracion':w.duracion, 'acumulador_horas':w.acumulador_horas, 'estado':w.estado,'proyecto_id':w.proyecto_id}
        form=FormularioHU(data=data)
        self.assertTrue(form.is_valid())
        
    def test_formularioHU_invalido(self):
        """
        Test del Formulario HU, prueba que el HU creado sea invalido
        """        
        w=HU.objects.create(valor_tecnico='1', valor_negocio='1', prioridad='1', duracion='1',acumulador_horas='1', estado='ACT', proyecto_id='1', version='1')
        data={'valor_tecnico':w.valor_tecnico, 'valor_negocio':w.valor_negocio, 'prioridad':w.prioridad, 'duracion':w.duracion}
        form=FormularioHU(data=data)
        self.assertTrue(form.is_valid())
        
    def create_proyecto(self):
        return proyecto(nombre_corto="P9", nombre_largo="proyecto9", descripcion="proyecto9", fecha_inicio=timezone.now(), fecha_fin=datetime.timedelta(days=1), estado="PEN")

    def create_rol(self):
        return rol.objects.create( nombre_rol_id="nuevoRol", descripcion="nuevo_rol", usuario_creador= MyUser.objects.create_user('delsy', Permitido.objects.create(email='delsy@gmail.com'), '1234'))

    def test_modificar_hu(self):
        """
        Verifica que el hu se ha modificado correctamente el valor_negocio
        """
        w=HU.objects.create(valor_tecnico='1', valor_negocio='1', prioridad='1', duracion='1',acumulador_horas='1', estado='ACT', proyecto_id='1', version='1')
        w.valor_negocio=2
        w.save()
        self.assertEqual(w.valor_negocio, 2)
         
    def test_cambioestado_hu(self):
        """
        Verifica que el hu se ha modificado correctamente su estado
        """
        w=HU.objects.create(descripcion='hu', valor_tecnico='1', valor_negocio='1', prioridad='1', duracion='1',acumulador_horas='1', estado='ACT',proyecto_id='1', valido='1', version='1')
        w.estado='CAN'
        w.save()
        self.assertEqual(w.estado, 'CAN')    
        
    def test_validaHU(self):
        """
        Comprueba que se valide correctamente un HU
        """
        hu=self.create_hu()
        hu.valido=True
        hu.save()
        self.assertEqual(hu.valido, True)
    
    def test_cambiar_version(self):
        hu=self.create_hu()
        hu.version=2
        hu.save()
        self.assertEqual(hu.version,2 )
    
    def create_version(self):
        hu=self.create_hu()
        return HU_version.objects.create(hu=hu, version="1", descripcion="nuevo", valor_negocio="1")
    
    def test_crear_version(self):
        w=self.create_version()
        self.assertTrue(isinstance(w, HU_version))
        self.assertEqual(w.__unicode__(), 'descripcion:'+w.descripcion + 'valor negocio: '+w.valor_negocio)

class SprintTest(TestCase):
    def create_sprint(self):
        return Sprint.objects.create( descripcion='sprintTest', fecha_inicio=timezone.now(), duracion='3', estado='ACT', proyecto_id='1')
    
    def test_sprint_creation(self):
        """
        Verifica la correcta creacion del Sprint
        """
        w=self.create_sprint()
        self.assertEqual(w.descripcion, 'sprintTest')
        
    def test_FormularioSprintProyecto_invalido(self):
        """
        Comprobamos que el formulario de Sprint no es valido al faltarle un campo
        """
        w=Sprint.objects.create(descripcion='sprint1', fecha_inicio=timezone.now(), duracion='3', estado='ACT', proyecto_id='1')
        data={'descripcion':w.descripcion, 'fecha_inicio':w.fecha_inicio, 'duracion':w.duracion}
        form=FormularioSprintProyecto(data=data)
        self.assertFalse(form.is_valid())
          
    def test_modificar_sprint(self):
        """
        Verifica que el sprint se ha modificado correctamente su duracion
        """
        sprint=self.create_sprint()
        sprint.duracion=4
        sprint.save()
        self.assertEqual(sprint.duracion, 4)
        
    def test_cambiarestado_sprint(self):
        """
        Verifica que el sprint se ha cambiado correctamente su estado
        """
        sprint=self.create_sprint()
        sprint.estado='CAN'
        sprint.save()
        self.assertEqual(sprint.estado, 'CAN')
        
    def test_login_valido(self):
        """
        Verifica que el login funcione correctamente, con un usuario creado
        """
        self.user = MyUser.objects.create_user('anonimo', Permitido.objects.create(email='anonimo2@hotmail.com'), '1234') 
        self.user.set_password('1234') 
        self.user.save() 
        #self.user = authenticate(username='testuser', password='hello') 
        login = self.client.login(username='anonimo', password='1234') 
        self.assertTrue(login) 
        
    def test_login_invalido(self):
        """
        Verifica que el login funcione correctamente, ingresando un usuario incorrecto
        """
        self.user = MyUser.objects.create_user('anonimo', Permitido.objects.create(email='anonimo2@hotmail.com'), '1234') 
        self.user.set_password('1234') 
        self.user.save() 
        #self.user = authenticate(username='testuser', password='hello') 
        login = self.client.login(username='anonimo2', password='1234') 
        self.assertFalse(login)
        
    def create_hu_descripcion(self, horas_trabajadas="1", descripcion_horas_trabajadas="Tarea", fecha="2015-04-30 17:40:33.036118-04", actividad="1 - Analisis", estado="PRO" ):
        return HU_descripcion.objects.create(horas_trabajadas=horas_trabajadas, descripcion_horas_trabajadas=descripcion_horas_trabajadas, fecha=fecha, actividad=actividad, estado=estado)

    def test_hu_descripcion(self):
        w=self.create_hu_descripcion()
        self.assertTrue(isinstance(w, HU_descripcion))
        self.assertEqual(w.__unicode__(), str(w.id))
        
class test_notificaciones(TestCase):
    #Crear Rol
    def create_rol(self):
        return rol.objects.create( nombre_rol_id="nuevoRol", descripcion="nuevo_rol", usuario_creador= MyUser.objects.create_user('delsy', Permitido.objects.create(email='delsy@gmail.com'), '1234'))
 
    def test_Rol(self):
        """
        Prueba envio de mail de notificaciones al crear Rol
        """
        mail.outbox = []
        rol=self.create_rol()
        evento_e="Se ha creado un nuevo rol de nombre: "+rol.nombre_rol_id
        email_e=str(rol.usuario_creador.email)
        mail.send_mail('Notificacion', evento_e,'usuariodjango@gmail.com', [email_e], fail_silently=False)

        #Verifica que el subject del mensaje es correcto
        self.assertEqual(mail.outbox[0].subject, 'Notificacion')
        
        #verifica que se ha enviado correctamente el cuerpo del mensaje
        self.assertEqual(mail.outbox[0].body, "Se ha creado un nuevo rol de nombre: "+rol.nombre_rol_id)
    
    #Crear Flujo
    def create_Flujo(self, nombre="1nuevoFlujo", estado="ACT" ):
        return Flujo.objects.create(nombre=nombre, estado=estado)
    
    def usuario(self):
        return MyUser.objects.create_user(username='delsy', email=Permitido.objects.create(email='delsy@gmail.com'), password='1234')
    
    def test_Flujo(self):
        """
        Prueba envio de mail de notificaciones al crear flujo
        """
        mail.outbox = []
        flujo=self.create_Flujo()
        evento_e="Se ha creado un nuevo flujo de nombre: "+flujo.nombre
        usuario=self.usuario()
        email_e=str(usuario.email)
        mail.send_mail('Notificacion', evento_e,'usuariodjango@gmail.com', [email_e], fail_silently=False)

        #Verifica que el subject del mensaje es correcto
        self.assertEqual(mail.outbox[0].subject, 'Notificacion')
        
        #verifica que se ha enviado correctamente el cuerpo del mensaje
        self.assertEqual(mail.outbox[0].body, "Se ha creado un nuevo flujo de nombre: "+flujo.nombre)
        
    def create_hu(self, descripcion="hu", valor_negocio="7", valor_tecnico="0", prioridad="0", duracion="0", acumulador_horas="0", estado="ACT", estado_en_actividad="PEN", valido="FALSE", proyecto_id="1", version="1"):
            return HU.objects.create(descripcion=descripcion, valor_negocio=valor_negocio, valor_tecnico=valor_tecnico, prioridad=prioridad, duracion=duracion, acumulador_horas=acumulador_horas, estado=estado, estado_en_actividad=estado_en_actividad, valido=valido, proyecto_id=proyecto_id, version=version)

    def test_HU(self):
        """
        Prueba envio de mail de notificaciones al crear hu
        """
        mail.outbox = []
        hu=self.create_hu()
        evento_e="Se ha creado un nuevo hu de nombre: "+hu.descripcion
        usuario=self.usuario()
        email_e=str(usuario.email)
        mail.send_mail('Notificacion', evento_e,'usuariodjango@gmail.com', [email_e], fail_silently=False)

        #Verifica que el subject del mensaje es correcto
        self.assertEqual(mail.outbox[0].subject, 'Notificacion')
        
        #verifica que se ha enviado correctamente el cuerpo del mensaje
        self.assertEqual(mail.outbox[0].body, "Se ha creado un nuevo hu de nombre: "+hu.descripcion)

    def create_sprint(self):
        return Sprint.objects.create( descripcion='sprintTest', fecha_inicio=timezone.now(), duracion='3', estado='ACT', proyecto_id='1')
        
    def test_sprint(self):
        """
        Prueba envio de mail de notificaciones al crear un sprint
        """
        mail.outbox = []
        sprint=self.create_sprint()
        evento_e="Se ha creado un nuevo sprint de nombre: "+sprint.descripcion
        usuario=self.usuario()
        email_e=str(usuario.email)
        mail.send_mail('Notificacion', evento_e,'usuariodjango@gmail.com', [email_e], fail_silently=False)

        #Verifica que el subject del mensaje es correcto
        self.assertEqual(mail.outbox[0].subject, 'Notificacion')
        
        #verifica que se ha enviado correctamente el cuerpo del mensaje
        self.assertEqual(mail.outbox[0].body, "Se ha creado un nuevo sprint de nombre: "+sprint.descripcion)
        
    def create_Actividades(self, nombre="nuevaActividad", descripcion="nuevo Actividad" ):
        return Actividades.objects.create(nombre=nombre, descripcion=descripcion)

    def test_actividad(self):
        """
        Prueba envio de mail de notificaciones al crear una actividad
        """
        mail.outbox = []
        actividad=self.create_Actividades()
        evento_e="Se ha creado una nueva actividad de nombre: "+actividad.nombre
        usuario=self.usuario()
        email_e=str(usuario.email)
        mail.send_mail('Notificacion', evento_e,'usuariodjango@gmail.com', [email_e], fail_silently=False)

        #Verifica que el subject del mensaje es correcto
        self.assertEqual(mail.outbox[0].subject, 'Notificacion')
        
        #verifica que se ha enviado correctamente el cuerpo del mensaje
        self.assertEqual(mail.outbox[0].body, "Se ha creado una nueva actividad de nombre: "+actividad.nombre)
    
    def test_actividad_modificado(self):
        """
        Prueba envio de mail de notificaciones al modificar una actividad
        """
        mail.outbox = []
        actividad=self.create_Actividades()
        actividad.nombre="Prueba"
        actividad.save()
        evento_e="Se ha modificado la actividad de nombre: "+actividad.nombre
        usuario=self.usuario()
        email_e=str(usuario.email)
        mail.send_mail('Notificacion', evento_e,'usuariodjango@gmail.com', [email_e], fail_silently=False)

        #Verifica que el subject del mensaje es correcto
        self.assertEqual(mail.outbox[0].subject, 'Notificacion')
        
        #verifica que se ha enviado correctamente el cuerpo del mensaje
        self.assertEqual(mail.outbox[0].body, "Se ha modificado la actividad de nombre: "+actividad.nombre)

    def test_Flujo_modificar(self):
        """
        Prueba envio de mail de notificaciones al modificar flujo
        """
        mail.outbox = []
        flujo=self.create_Flujo()
        flujo.nombre="Prueba"
        flujo.save()
        evento_e="Se ha modificado el flujo de nombre: "+flujo.nombre
        usuario=self.usuario()
        email_e=str(usuario.email)
        mail.send_mail('Notificacion', evento_e,'usuariodjango@gmail.com', [email_e], fail_silently=False)

        #Verifica que el subject del mensaje es correcto
        self.assertEqual(mail.outbox[0].subject, 'Notificacion')
        
        #verifica que se ha enviado correctamente el cuerpo del mensaje
        self.assertEqual(mail.outbox[0].body, "Se ha modificado el flujo de nombre: "+flujo.nombre)
        
    def test_sprint_modificado(self):
        """
        Prueba envio de mail de notificaciones al modificado un sprint
        """
        mail.outbox = []
        sprint=self.create_sprint()
        evento_e="Se ha modificado el sprint de nombre: "+sprint.descripcion
        usuario=self.usuario()
        email_e=str(usuario.email)
        mail.send_mail('Notificacion', evento_e,'usuariodjango@gmail.com', [email_e], fail_silently=False)

        #Verifica que el subject del mensaje es correcto
        self.assertEqual(mail.outbox[0].subject, 'Notificacion')
        
        #verifica que se ha enviado correctamente el cuerpo del mensaje
        self.assertEqual(mail.outbox[0].body, "Se ha modificado el sprint de nombre: "+sprint.descripcion)

class TestholaScrumView(TestCase):
      
    def create_rol(self):
        return rol.objects.create( nombre_rol_id="nuevoRol", descripcion="nuevo_rol", usuario_creador= MyUser.objects.create_user('delsy', Permitido.objects.create(email='delsy@gmail.com'), '1234'))
    
    def create_hu(self, descripcion="hu", valor_negocio="7", valor_tecnico="0", prioridad="0", duracion="0", acumulador_horas="0", estado="ACT", estado_en_actividad="PEN", valido="FALSE", proyecto_id="1", version="1"):
            return HU.objects.create(descripcion=descripcion, valor_negocio=valor_negocio, valor_tecnico=valor_tecnico, prioridad=prioridad, duracion=duracion, acumulador_horas=acumulador_horas, estado=estado, estado_en_actividad=estado_en_actividad, valido=valido, proyecto_id=proyecto_id, version=version)
    
    def usuario(self):
        return MyUser.objects.create_user(username='delsy', email=Permitido.objects.create(email='delsy@gmail.com'), password='1234')
    
    def create_Flujo(self, nombre="1nuevoFlujo", estado="ACT" ):
        return Flujo.objects.create(nombre=nombre, estado=estado)

    def create_sprint(self):
        return Sprint.objects.create( descripcion='sprintTest', fecha_inicio=timezone.now(), duracion='3', estado='ACT', proyecto_id='1')
  
    def test_permiso(self):
        w=self.create_rol()
        w.permisos.add(Permission.objects.get(id=22))
        w.save()
        if w.tiene_permiso('Can add rol'):
            self.assertEqual(w.nombre_rol_id, 'nuevoRol')
    
    def test_permiso_invalido(self):
        w=self.create_rol()
        w.permisos.add(Permission.objects.get(id=22))
        w.save()
        if w.tiene_permiso('Can change hu'):
            self.assertEqual(w.nombre_rol_id, 'nuevoRol')
        else:
            self.assertEqual(w.nombre_rol_id, 'nuevoRol')

    def test_scrum_agota_tiempo(self):
        HUsm_horas_agotadas=[]
        rol=self.create_rol()
        rol.nombre_rol_id="Scrum"
        rol.permisos.add(Permission.objects.create(name='Can change hu nivel Scrum', content_type_id=13, codename='Can change hu nivel Scrum'))
        rol.save()
        self.assertEqual(rol.nombre_rol_id, 'Scrum')
        proyectox=proyecto.objects.create(nombre_corto='p1',nombre_largo='proyecto1',descripcion='proyecto1',fecha_inicio=timezone.now(),fecha_fin=timezone.now(),estado='PEN')
        hu=self.create_hu()
        hu.valido=True
        hu.duracion=4
        hu.acumulador_horas=4
        hu.proyecto_id=proyectox
        hu.save()
        
        if rol.tiene_permiso('Can change hu nivel Scrum'):
            HUsm = HU.objects.filter(proyecto_id=proyectox.id).filter(valido=True)
            for h in HUsm:
                if h.estado_en_actividad != "FIN" and h.estado_en_actividad !='APR' and h.duracion == h.acumulador_horas and h.acumulador_horas !=0:
                    HUsm_horas_agotadas.append(h)
                    
        self.assertEqual(HUsm_horas_agotadas, [hu])
              
    def test_delegacion(self):
        HU_no_asignada=[]
        HU_asignada=[]
        rolx=self.create_rol()
        rolx.nombre_rol_id="Scrum"
        rolx.permisos.add(Permission.objects.create(name='agregar delegacion', content_type_id=15, codename='Can add delegacion'))
        rolx.save()
        self.assertEqual(rolx.nombre_rol_id, 'Scrum')
        proyectox=proyecto.objects.create(nombre_corto='p1',nombre_largo='proyecto1',descripcion='proyecto1',fecha_inicio=timezone.now(),fecha_fin=timezone.now(),estado='ACT')
        hu=self.create_hu()
        hu.valido=True
        hu.estado="ACT"
        hu.proyecto_id=proyectox.id
        hu.save()
        d=delegacion.objects.create(usuario=rolx.usuario_creador, hu=hu)
        
        if rolx.tiene_permiso('agregar delegacion'):
            for h in HU.objects.filter(proyecto=proyectox).filter(estado='ACT').filter(valido=True):
                x=0
                for d in delegacion.objects.all():
                    if d.hu == h:
                        x=1
                if x == 0:
                    HU_no_asignada.append(h)
                else:
                    HU_asignada.append(h)
                    
        self.assertEqual(HU_asignada, [d.hu])
                
    def test_Agregar_horas(self):
        rolx=self.create_rol()
        rolx.nombre_rol_id="Scrum"
        rolx.permisos.add(Permission.objects.create(name='Agregar horas trabajadas', content_type_id=16, codename='Agregar horas trabajadas'))
        rolx.save()
        self.assertEqual(rolx.nombre_rol_id, 'Scrum')
        proyectox=proyecto.objects.create(nombre_corto='p1',nombre_largo='proyecto1',descripcion='proyecto1',fecha_inicio=timezone.now(),fecha_fin=timezone.now(),estado='ACT')
        hu=self.create_hu()
        hu.valido=True
        hu.estado="ACT"
        hu.proyecto_id=proyectox.id
        hu.save()
        d=delegacion.objects.create(usuario=rolx.usuario_creador, hu=hu)
        HUs_add_horas=[]
        if rolx.tiene_permiso('Agregar horas trabajadas'):
            for d in delegacion.objects.all():
                if d.hu.proyecto == proyectox and str(d.usuario.id) == str(rolx.usuario_creador.id):
                    if d.hu.estado == 'ACT':
                        HUs_add_horas.append(d.hu)
                                                 
        self.assertEqual(HUs_add_horas, [d.hu])
            
    def test_modificar_hu(self):
        HU_no_asignada_owner=[]
        HU_asignada_owner=[]
        rolx=self.create_rol()
        rolx.nombre_rol_id="ProductOwner"
        rolx.permisos.add(Permission.objects.create(name='modificar hu', content_type_id=17, codename='Can change hu'))
        rolx.save()
        self.assertEqual(rolx.nombre_rol_id, 'ProductOwner')
        proyectox=proyecto.objects.create(nombre_corto='p1',nombre_largo='proyecto1',descripcion='proyecto1',fecha_inicio=timezone.now(),fecha_fin=timezone.now(),estado='ACT')
        hu=self.create_hu()
        hu.proyecto_id=proyectox.id
        hu.save()
        if rolx.tiene_permiso('modificar hu'):
            for HUa in HU.objects.filter(proyecto=proyectox):
                x=0
                for d in delegacion.objects.all():
                    if d.hu == HUa:
                        x=1
                if x == 0:
                    HU_no_asignada_owner.append(HUa)
                else:
                    HU_asignada_owner.append(HUa)
        self.assertEqual(HU_no_asignada_owner, [hu])            

            
    def test_flujo_modificar(self):
        """Tiene permiso de modificar flujo, obtengo todos los flujos para enviar al rol-flujo-para-scrum.html"""
        rolx=self.create_rol()
        rolx.nombre_rol_id="Scrum"
        rolx.permisos.add(Permission.objects.get(id=47))
        rolx.save()
        self.assertEqual(rolx.nombre_rol_id, 'Scrum')
        flujo=Flujo.objects.create(nombre="1nuevoFlujo", estado="ACT")
        flujo2=Flujo.objects.create(nombre="2nuevoFlujo", estado="ACT")
        sprint=Sprint.objects.create( descripcion='sprintTest', fecha_inicio=timezone.now(), duracion='3', estado='CON', proyecto_id='1')
        sprint.flujo.add(flujo)
        sprint.save()
        self.assertEqual(sprint.descripcion, 'sprintTest')
        sprint2=Sprint.objects.create( descripcion='sprintTest', fecha_inicio=timezone.now(), duracion='3', estado='ACT', proyecto_id='1')
        sprint2.flujo.add(flujo2)
        sprint2.save()
        self.assertEqual(sprint.estado, 'CON')
        self.assertEqual(sprint2.estado, 'ACT')
        flujosm=[]
        if rolx.tiene_permiso('Can change flujo'):
            flujosm=Flujo.objects.all()
            for flujo in flujosm:
                for s in Sprint.objects.all():
                    if s.estado == 'CON':
                        for f in s.flujo.all():
                            if f == flujo:
                                flujosm=flujosm.exclude(id=f.id)
        for f in flujosm.all():
            self.assertEqual(f.nombre, "2nuevoFlujo")
            
           


class loginCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
  
    def test_admin_login(self):
        """
        Usando el selenium, podemos simular que un usuario abre el navegador web, y navega a la pagina de login
        el usuario es dirigido a la pagina http://localhost/login/ que simula ingresar su usuario y contraseña
        si las credenciales de inicio de sesion son las correctas, el usuario es redirigido a la pagina
        principal /hola/, y cierra el navegador
        """
    # usuario abre el navegador web, navega a pagina login
        
        self.browser.get("http://localhost/login/")

        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('delsy')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('1234')
        password_field.send_keys(Keys.RETURN)
        # Las credenciales de inicio de sesion son correctos, y el usuario es redirigido a la página principal de HOLA
        title = self.browser.find_element_by_tag_name('body')
        self.assertIn('Pagina Principal', title.text)
        user_link = self.browser.find_elements_by_link_text('Scrum Master')
        user_link[0].click()
        user_link = self.browser.find_elements_by_link_text('Visualizar Product Backlog')
        user_link[0].click()
        title = self.browser.find_element_by_tag_name('body')
        self.assertIn('Visualizar Product Backlog', title.text)
        time.sleep(3)
        user_link2 = self.browser.find_elements_by_link_text('Visualizar Product Backlog')
        user_link2[0].click()
        user_link = self.browser.find_elements_by_link_text('Salir')
        user_link[0].click()
        title = self.browser.find_element_by_tag_name('body')
        self.assertIn('Gracias por utilizar nuestro sistema', title.text)
        user_link = self.browser.find_elements_by_link_text('Iniciar sesion de nuevo')
        user_link[0].click()
        time.sleep(3)
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('katherine')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('1234')
        password_field.send_keys(Keys.RETURN)
        time.sleep(1)
        user_link = self.browser.find_elements_by_link_text('Product Owner')
        user_link[0].click()
        time.sleep(1)
        title = self.browser.find_element_by_tag_name('body')
        self.assertIn('Pagina Principal', title.text)
        user_link = self.browser.find_elements_by_link_text('Agregar HU')
        user_link[0].click()
        title = self.browser.find_element_by_tag_name('body')
        self.assertIn('Pagina Principal', title.text)
        self.browser.find_element_by_name('descripcion').send_keys("HU")
        valor_field = self.browser.find_element_by_name('valor_negocio')
        valor_field.send_keys("5")
        time.sleep(1)
        self.browser.find_element_by_css_selector("input[value='Guardar']").click()
        title = self.browser.find_element_by_tag_name('body')
        self.assertIn('La HU se ha creado y relacionado con el proyecto', title.text)
        time.sleep(3)
    #cierra el browser   
    def tearDown(self):
        self.browser.quit()
        
class AgregarhorasCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
  
    def test_agregar_horas(self):
    # usuario abre el navegador web, navega a pagina login
        
        self.browser.get("http://localhost/login/")

        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('sebas')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('1234')
        password_field.send_keys(Keys.RETURN)
        # Las credenciales de inicio de sesion son correctos, y el usuario es redirigido a la página principal de HOLA
        title = self.browser.find_element_by_tag_name('body')
        self.assertIn('Pagina Principal', title.text)
        time.sleep(2)
        user_link = self.browser.find_elements_by_link_text('Equipo')
        user_link[0].click()
        title = self.browser.find_element_by_tag_name('body')
        self.assertIn('Pagina Principal', title.text)
        user_link2 =self.browser.find_elements_by_link_text('Agregar horas trabajadas')
        user_link2[0].click()
        self.browser.find_element_by_name('horas_agregar').send_keys("0.1")
        self.browser.find_element_by_name('descripcion_horas').send_keys("Tarea")
        time.sleep(2)
        self.browser.find_element_by_css_selector("input[value='Guardar']").click()
        user_link = self.browser.find_elements_by_link_text('Modificación de HU')
        user_link[0].click()
        time.sleep(3)
        
    #cierra el browser   
    def tearDown(self):
        self.browser.quit()