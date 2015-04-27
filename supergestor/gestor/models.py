#coding: utf-8
"""Archivo donde django busca las definiciones de modelos, con sus atributos , metodos y managers,
 y relaciones de modelos que heredan
de la clase models de django.db """

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
    , Permission)
from django.conf import settings


class MyUserManager(BaseUserManager):
    """Clase utilizada para la creacion de managers customizados 
    de clase de usuarios tambian customizada, herada metodos y atributos
    de la clase abstracta BaseUserManager que exige redefinir los metodos
    create_user y create_superuser"""
    def create_user(self, username, email, password=None):
        """
        Crea y guarda un usuario con el nombre de usuario , email y contraseña
        dados
        """
        if not username:
            raise ValueError('Los usuarios deben tener un nombre de usuario')

        user = self.model(
            username=username,
            email=Permitido.objects.get(pk=email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Crea y guarda un superuser con el nombre de usuario, email y password
        dados
        """
        user = self.create_user(username,
            password=password,
            email=Permitido.objects.get(pk=email),
        )
        user.is_admin =True
        user.save(using=self._db)
        return user

class Permitido(models.Model):
    """Este modelos mantiene registros de correos permitidos para la creacion de usuarios"""
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,primary_key=True,
    )
    
    def __unicode__(self):
        """Representacion unicode del objeto permitido"""
        return self.email
    
#    def is_exists(self, email_recibido):
    #    if self.email

class MyUser(AbstractBaseUser):
    """Clase que representa usuario del modulo de autenticacion customizada con mas atributos, hereda
    metodos y atributos de la clase abstracta AbstractBaseUser, especifica la confgutacion 
    de sus instancias en USERNAME_FIELDS y los atributos requeridos en create_user y create_superuser
    en REQUIRED_FIELDS, ademas redefine metodos: get_full_name(),get_short_name(),has_perm(),
    has_module_perms(),is_staff()"""
    username=models.CharField(max_length=40,unique=True)
    user_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    direccion=models.CharField(max_length=255)
    email = models.OneToOneField(Permitido)
    #email.unique()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','direccion']
    
    def create(self,username,email,password,user_name, last_name,direccion):
        """Metodo para la creacion de usuarios desde interfaz web completando todos los 
        atributos"""
        usuario=MyUser.objects.create_user(username, email, password=None)
        usuario.last_name=last_name
        usuario.user_name=user_name
        usuario.direccion=direccion
        return usuario
        

    def get_full_name(self):
        """Retorna el nombre y apellido del usuario"""
        # The user is identified by their email address
        return self.user_name+self.last_name
    
    def get_short_name(self):
        """Retorna el username identificador del usuario"""
        # The user is identified by their email address
        return self.username

    def __unicode__(self):
        """Representacion unicode del objeto usuario"""
        return self.username

    def has_perm(self, perm, obj=None):
        "Por implementar: Retornara true si un usuario tiene el permiso indicado como argumento"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Por implementar: Retornarea true si el usuario tiene permiso de acceder a una 
        applicacion particular"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Retorna true si el usuario es administrador"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
       
class rol(models.Model):
    """Modelo que representa roles con relacion muchos a muchos a la tabla de permisos"""
    ESTADO_CHOICES = (
        ('CAN', 'Cancelado'),
        ('ACT', 'Activo'),
    )
    permisos= models.ManyToManyField(Permission)
    nombre_rol_id = models.CharField(max_length = 200)
    descripcion = models.CharField(max_length = 200)
    usuario_creador = models.ForeignKey(MyUser)
    estado = models.CharField(max_length = 3, choices = ESTADO_CHOICES)
    
    def tiene_permiso(self,perm):
        """checkea si un rol esta compuesto por un permiso"""
        permiso= Permission.objects.get(name=perm)
        if permiso in self.permisos.all():
            return True
        else:
            return False

    def __unicode__(self):
        """Representacion unicode del objeto rol"""
        return self.nombre_rol_id
    
class rol_sistema(models.Model): 
    """Modelo que representa roles exclusivos de permisos de sistema, tiene una relacion
    muchos a muchos con permisos"""   
    permisos= models.ManyToManyField(Permission)
    nombre_rol_id = models.CharField(max_length = 200)
    descripcion = models.CharField(max_length = 200)
    #tipo = models.CharField(max_length = 3, choices = ROL_CHOICES)
    def __unicode__(self):
        """Representacion unicode del objeto rol sistema"""
        return self.nombre_rol_id
      
class Actividades(models.Model):
    """Representacion de la actividad de un flujo relacionada a su proyecto"""
    nombre = models.CharField(max_length = 200)
    descripcion = models.CharField(max_length = 200)
    def __unicode__(self):
        """Representacion unicode del objeto actividad"""
        return str(self.id)  + " - " + self.nombre
    
    
class Flujo(models.Model):
    """Representacion de un flujo de proyecto relacionado a su respectivo proyecto
    mediante"""
    
    ESTADO_CHOICES = (
        ('CAN', 'Cancelado'),
        ('ACT', 'Activo'),
    )
     
    nombre = models.CharField(max_length = 200)
    estado = models.CharField(max_length = 3, choices = ESTADO_CHOICES)
    actividades = models.ManyToManyField(Actividades)
    def __unicode__(self):
        """Representacion unicode del objeto flujo"""
        return str(self.id) + self.nombre


class proyecto(models.Model):
    """Modelo que representa los proyectos que se pueden usar en el sistema"""
    ESTADO_CHOICES = (
        ('PEN', 'Pendiente'),
        ('ACT', 'Activo'),
        ('ANU', 'Anulado'),
        ('FIN', 'Finalizado'),
    )
    
    nombre_corto = models.CharField(max_length = 200)
    nombre_largo = models.CharField(max_length = 200)
    descripcion = models.CharField(max_length = 200)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(max_length = 3, choices = ESTADO_CHOICES)
    flujos = models.ManyToManyField(Flujo)
    
    def __unicode__(self):
        """Representacion unicode del objeto proyecto"""
        return self.nombre_corto   
class HU_descripcion(models.Model):
    """
    Modelo representa la descripcion de cada hora de trabajo agregada
    """
    horas_trabajadas=models.FloatField()  
    descripcion_horas_trabajadas=models.CharField(max_length = 200)
    def __unicode__(self):
        """Representacion unicode del objeto HU_descripcion"""
        return str(self.id)    
    
class HU(models.Model):
    """Modelo que reprenseta las historias de usuario"""
    VALORES100_CHOICES = zip(range(1,101), range(1,101))
    VALORES10_CHOICES = zip(range(1,11), range(1,11))

    ESTADO_CHOICES = (
        ('CAN', 'Cancelado'),
        ('ACT', 'Activo'),
    )
    
    ESTADO_ACTIVIDAD_CHOICES = (
        ('PEN', 'Pendiente'),
        ('PRO', 'En Progreso'),
        ('FIN', 'Finalizado'),
    )
    
    descripcion = models.CharField(max_length = 200)
    valor_negocio = models.IntegerField(choices = VALORES10_CHOICES)
    valor_tecnico = models.IntegerField(choices = VALORES10_CHOICES)
    prioridad = models.IntegerField(choices = VALORES100_CHOICES)
    duracion = models.FloatField()
    acumulador_horas = models.FloatField()
    estado = models.CharField(max_length = 3, choices = ESTADO_CHOICES)
    estado_en_actividad = models.CharField(max_length = 3, choices = ESTADO_ACTIVIDAD_CHOICES)
    proyecto=models.ForeignKey(proyecto) #este campo va indicar a que proyecto pertenece asi en la vista ya no tenemos que hacer hu.objects.all()
    valido=models.BooleanField(default=False) # rl productOwner debe validar
    hu_descripcion=models.ManyToManyField(HU_descripcion)
    
    def __unicode__(self):
        """Representacion unicode del objeto HU"""
        return self.descripcion
      
class archivoadjunto(models.Model):
    archivo=models.FileField()
    hU=models.OneToOneField(HU)

class Sprint(models.Model):
    """Modelo que reprenseta los Spring de un proyecto relacionados a
    sus respectivos proyectos mediante un foreign key"""
    
    ESTADO_CHOICES = (
        ('CAN', 'Cancelado'),
        ('ACT', 'Activo'),
        ('CON', 'Consulta'),
    )
     
    descripcion = models.CharField(max_length = 200)
    hu=models.ManyToManyField(HU)
    fecha_inicio = models.DateTimeField()
    duracion = models.FloatField()
    estado = models.CharField(max_length = 3, choices = ESTADO_CHOICES)
    proyecto=models.ForeignKey(proyecto)
    
    def __unicode__(self):
        """Representacion unicode del objeto sprint"""
        return self.descripcion
    
#Modelo para asignacion de actividades con HU en un flujo determinado
class asignacion(models.Model):
    """Modelo que especifica una asignacion de un rol a un usuario en un proyecto"""
    usuario=models.ForeignKey(MyUser)
    rol=models.ForeignKey(rol)    
    proyecto=models.ForeignKey(proyecto)
    def __unicode__(self):
        """Representacion unicode del objeto asignacion"""
        return str(self.id)+" - "+str(self.usuario)+" - "+str(self.rol)+" - "+str(self.proyecto) 
    
#Modelo para asignacion de roles de proyecto
class asigna_sistema(models.Model):
    """Modelo que representa la asignaciones de roles de sistema a usuarios con clave foranea a 
    modelo rol sistema"""
    usuario=models.ForeignKey(MyUser)
    rol=models.ForeignKey(rol_sistema)    
    def __unicode__(self):
        """Representacion unicode del objeto asigna sistema"""
        return str(self.id)+" - "+str(self.usuario)+" - "+str(self.rol)

class delegacion(models.Model):
    """Modelo que especifica una delegacion de una HU a un usuario en un proyecto"""
    usuario=models.ForeignKey(settings.AUTH_USER_MODEL)
    hu=models.ForeignKey(HU)
    def __unicode__(self):
        """Representacion unicode del objeto delegacion"""
        return str(self.id)+" - "+str(self.usuario)+" - "+str(self.HU.descripcion)+" - "+str(self.HU.proyecto)

class asignaHU_actividad_flujo(models.Model):
    """Modelo intermedio para la relacion varios a varios del modelo flujo con actividades"""
    lista_de_HU = models.ManyToManyField(HU)
    flujo_al_que_pertenece = models.ForeignKey(Flujo)
    actividad_al_que_pertenece = models.ForeignKey(Actividades)
    def __unicode__(self):
        """Representacion unicode del objeto asignaHU_actividad_flujo"""
        return str(self.id)+" - "+str(self.flujo_al_que_pertenece)+" - "+str(self.actividad_al_que_pertenece)
    
    
