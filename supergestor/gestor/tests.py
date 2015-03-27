"""

Casos de prueba para los modelos existentes dentro del sistema.

"""
from django.test import TestCase, Client

from gestor.models import MyUser, Permitido

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