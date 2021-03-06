"""

Casos de prueba para los modelos existentes dentro del sistema.

"""
from django.test import TestCase, Client
from gestor.models import MyUser, Permitido, rol, rol_sistema, Actividades, Flujo, proyecto, asignacion, asigna_sistema
from gestor.views import FormularioRolProyecto, proyectoFrom, FormularioFlujoProyecto, formularioActividad
from django.test.client import RequestFactory
from django.contrib.auth.models import Permission
from django.utils import timezone
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
        response=self.client.get('/crearRol/2/1/')
        self.assertEqual(response.status_code, 200)
         
class Rol_sistemaTest(TestCase):
    
    def create_rol_sistema(self):
        return rol_sistema.objects.create( nombre_rol_id="nuevoRol", descripcion="nuevo_rol")
    
    def test_rol_sistema_creation(self):
        w=self.create_rol_sistema()
        self.assertTrue(isinstance(w, rol_sistema))
        self.assertEqual(w.__unicode__(), w.nombre_rol_id)
    """
    def test_guardarRolView(self):
        response=self.client.get('/guardarRol/2/',follow=True)
        self.assertEqual(response.status_code, 200)
    """          
class ActividadesTest(TestCase):
    def create_Actividades(self, nombre="nuevaActividad", descripcion="nuevo Actividad" ):
        return Actividades.objects.create(nombre=nombre, descripcion=descripcion)
    
    def test_Actividad_creation(self):
        w=self.create_Actividades()
        self.assertTrue(isinstance(w, Actividades))
        self.assertEqual(w.__unicode__(), str(w.id)  + " " + w.nombre)
        
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
    
     
    def test_modificar_actividad(self):
        w=self.create_proyecto()    
        u= MyUser.objects.create_user('anonimo', Permitido.objects.create(email='anonimo2@hotmail.com'), '1234')
        y= self.create_Actividades()

        post_data={'usuario':u.id,'proyecto':w.id,'actividad':y.id}
        Actividad_url='/modificarActividad/1/1/'
        self.client.post(Actividad_url, data=post_data)
        
class FlujoTest(TestCase):
    def create_Flujo(self, nombre="nuevoFlujo", estado="ACT" ):
        return Flujo.objects.create(nombre=nombre, estado=estado)
    
    def test_Flujo_creation(self):
        w=self.create_Flujo()
        self.assertTrue(isinstance(w, Flujo))
        self.assertEqual(w.__unicode__(), str(w.id) + w.nombre)
    
    def test_crear_flujo_views(self):
        response=self.client.get('/crearFlujo/2/1/')
        self.assertEqual(response.status_code, 200)  
        
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
        w = rol.objects.create(nombre_rol_id="nuevoRol", descripcion="nuevoRol", usuario_creador=MyUser.objects.create_user('kathe', Permitido.objects.create(email='kathe@gmail.com'), '1234'))
        w.permisos.add(Permission.objects.get(id=34))
        form = FormularioRolProyecto({'nombre_rol_id':w.nombre_rol_id, 'descripcion':w.descripcion,'permisos':[t.id for t in w.permisos.all()], })
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
    def create_asignacion(self, usuario_id='1', rol_id='1', proyecto_id='1'):
        return asignacion.objects.create(usuario_id=usuario_id, rol_id=rol_id, proyecto_id=proyecto_id)
    
    def test_asignacion_creation(self):
        w=self.create_asignacion()
        self.assertTrue(isinstance(w, asignacion))
        self.assertEqual(w.__unicode__(), str(w.id))
        
class asigna_sistemacionTest(TestCase):
    def create_asigna_sistema(self, usuario_id='1', rol_id='1'):
        return asigna_sistema.objects.create(usuario_id=usuario_id, rol_id=rol_id) 
    
    def test_asigna_sistema_creation(self):
        w=self.create_asigna_sistema()
        self.assertTrue(isinstance(w, asigna_sistema))
        self.assertEqual(w.__unicode__(), str(w.id))

    def create_proyecto(self):
        return proyecto(nombre_corto="P9", nombre_largo="proyecto9", descripcion="proyecto9", fecha_inicio=timezone.now(), fecha_fin=datetime.timedelta(days=1), estado="PEN")

        
    def create_rol(self):
        return rol.objects.create( nombre_rol_id="nuevoRol", descripcion="nuevo_rol", usuario_creador= MyUser.objects.create_user('delsy', Permitido.objects.create(email='delsy@gmail.com'), '1234'))

    def test_asignarRol_POST(self):
        w=self.create_proyecto()
        x=self.create_rol()
        post_data={'proyecto':w.id,'rol':x.id, 'usuario':x.usuario_creador}
        asignarRol_url='/asignarRol/1/1/'
        self.client.post(asignarRol_url, data=post_data)
                

 
        
     
        