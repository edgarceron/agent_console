"""Models for the users app"""
from django.db import models
from django.db.models import Q
from profiles.models import Profile

class Tecnology(models.Model):
    pass

class Location(models.Model):
    pass

class User(models.Model):
    "Model for an user"
    username = models.EmailField(
        unique=True,
        verbose_name="Nombre de usuario",
        null=False,
        error_messages={'unique':'Ya existe un usuario registrado con este correo'})
    password = models.CharField(max_length=255, verbose_name="Constraseña", null=False)
    name = models.CharField(max_length=100, verbose_name="Nombres", null=False)
    lastname = models.CharField(max_length=100, verbose_name="Apellidos", null=False)
    active = models.BooleanField(verbose_name="Activo/Inactivo", null=False) 
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=True)
    need_password = models.BooleanField(verbose_name="Cambiar contraseña", null=False, default=True)

    @staticmethod
    def usersPickerFilter(value):
        return list(User.objects.filter(
            Q(active=True),
            Q(username__contains=value) | Q(name__contains=value) | Q(lastname__contains=value)
        )[:10])

    @staticmethod
    def users_listing_filter(search, start, length, count=False):
        """Filters the corresponding models given a search string"""
        if count:
            return User.objects.filter(
                Q(username__contains=search) | Q(name__contains=search)
                | Q(lastname__contains=search)
            ).count()
        else:
            return User.objects.filter(
                Q(username__contains=search) | Q(name__contains=search)
                | Q(lastname__contains=search)
            )[start:start + length]

class UserDeveloper(models.Model):
    """Model to represent a developer user"""
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.DO_NOTHING)

class DeveloperTecnologies(models.Model):
    """Model to represent the tecnologies an user knows"""
    developer = models.ForeignKey(UserDeveloper, on_delete=models.CASCADE)
    tecnology = models.ForeignKey('Tecnology', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('developer', 'tecnology')

class LoginSession(models.Model):
    key = models.CharField(unique=True, null=False, max_length=255)
    life = models.DateTimeField(null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    