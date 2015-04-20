#coding: utf-8
"""Archivo que indica a django la configuracion 
de la interfaz del admin a los superusuarios,formularios 
y funciones particulares relacionadas a modelos 
registrados para ser administrados desde el admin"""
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField 
from gestor.models import MyUser, Permitido, rol, asignacion, proyecto,\
    asigna_sistema, rol_sistema,Flujo, Sprint


class UserCreationForm(forms.ModelForm):
    """Un formulario para crear nuevos usuarios, incluyendo todos los campos requeridos
    mas un campo dende se repite la contraseña"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        """Clase meta de un ModelForm donde se indica el Modelo relacionado y los campos a mostrar"""
        model = MyUser
        fields = ('username', 'email', 'user_name', 'last_name','direccion')

    def clean_password2(self):
        """metodo que resetea los campos de contraseñas en caso de que no coincidan 
        las contraseñas ingresadas"""
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """metodo que permite guardar los datos ingresados en el formulario"""
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    


class UserChangeForm(forms.ModelForm):
    """Formulario para actualizar usuarios. incluye todos los campo de usuario
    ,pero reemplaza el campo de contraseña con el campo hash de contraseña
    del admin
    
    """
    password = ReadOnlyPasswordHashField()
    class Meta:
        """Clase meta de un ModelForm donde se indica el Modelo relacionado y los campos a mostrar"""
        model = MyUser
        fields = ('username','email', 'password',  'is_active', 'is_admin',)

    def clean_password(self):
        """metodo que resetea los campos de contraseñas en caso de que no coincidan 
        las contraseñas ingresadas"""
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class RolCreationForm(forms.ModelForm):
    class Meta:
        model=rol
        fields=('permisos','nombre_rol_id','descripcion')

    
  
class MyUserAdmin(UserAdmin):
    """Configura la vista de administracion de un modelo, 
    los campos visibles de cada registro, los campos de filtro y busqueda
    ademas del metodo de ordenado"""
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on gestor_MyUser
    list_display = ('username','email', 'is_admin','is_active',)
    list_filter = ('is_admin','is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email','user_name', 'last_name','direccion',)}),
        ('Permissions', {'fields': ('is_admin','is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'user_name', 'last_name','direccion', 'password1', 'password2')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()
    save_as = True 
    
    
  
class FlujoCreationForm(forms.ModelForm):
    class Meta:
        model=Flujo
        fields=('nombre','actividades') #el estado en el momento de creacion tendra valor por defecto el usuario no decide  
    
         

class FlujoAdmin(admin.ModelAdmin):
    """Configura la vista de administracion de Flujos para un usuario administrador,
    lista nombre y estado y al modificar permite guardar como"""
    form=FlujoCreationForm
    list_display = ('nombre', 'estado')
    list_filter = ('estado',)
    ordering = ('id',)
    filter_horizontal = ('actividades',)
    exclude = ('proyecto',)
    save_as = True 
    def save_model(self,request,obj,form,change):
        """Permite establecer el Estado por defecto en el momento de la creacion que es ACTIVO????"""
        obj.estado='ACTIVO'
        obj.save()
        
    
class RolAdmin(admin.ModelAdmin):
    """Configura la vista de administracion, modificacion y creacion de roles para un administrador,
    lsta nombre y desprpcion y al crear, automaticamente establece al usuario actual como creador del rol"""
    form=RolCreationForm
    list_display = ('nombre_rol_id', 'descripcion')
    list_filter = ('id',)
    ordering = ('id',)
    filter_horizontal = ('permisos',)
    def save_model(self, request, obj, form, change):
        """Permite establecer al usuario actual utilizando la interfaz admin como creador del rol"""
        obj.usuario_creador = request.user
        obj.save()
    """add_fieldsets = (
        (None, {
            'fields': ('permisos','usuario_rol_id','descripcion')}
        ),
    )"""
    save_as = True 
    
    
    
    
class SprintCreationForm(forms.ModelForm):
    class Meta:
        model=Flujo
        fields=('descripcion','duracion','fecha_inicio') #el estado en el momento de creacion tendra valor por defecto el usuario no decide  
    
         

class SprintAdmin(admin.ModelAdmin):
    """Configura la vista de administracion de Sprint para un usuario administrador,
    lista nombre y estado y al modificar permite guardar como"""
    form=SprintCreationForm
    list_display = ('id', 'descripcion','duracion','fecha_inicio')
    list_filter = ('estado',)
    ordering = ('id',)
    save_as = True 
    def save_model(self,request,obj,form,change):
        """Permite establecer el Estado por defecto en el momento de la creacion que es ACTIVO????"""
        obj.estado='CONSULTA'
        obj.save()
        pass


# Now register the new UserAdmin...
"""registra el ModelAdmin(o UserAdmin) para ser desplegado en la interfaz del admin"""
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Permitido)
admin.site.register(rol, RolAdmin) 
admin.site.register(asignacion)
admin.site.register(proyecto)
admin.site.register(asigna_sistema)
admin.site.register(rol_sistema)
admin.site.register(Flujo,FlujoAdmin)
admin.site.register(Sprint,SprintAdmin)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
