from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename

# Create your models here.
class Profile(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.TextField(null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    fechanac = models.DateTimeField(null=True, blank=True)
    estado= models.BooleanField(default=True)
    

    class Meta:
        ordering = ['nombre']
    def __str__(self):
        return self.user.username




class ProfileHospital(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.TextField(null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    class Meta:
         ordering = ['user__username']



class ServicioMedico(models.Model):
    id=models.AutoField(primary_key=True)
    nombre = models.TextField(null=True, blank=True)
    estado= models.BooleanField(default=True)

class ServicioHospital(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    servicio=models.ForeignKey(ServicioMedico, on_delete=models.CASCADE)
    estado= models.BooleanField(default=False)

class EspecialidadMedica(models.Model):
    id=models.AutoField(primary_key=True)
    nombre = models.TextField(null=True, blank=True)
    estado= models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class EspecialidadMedico(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    especialidad=models.ForeignKey(EspecialidadMedica, on_delete=models.CASCADE)
    estado= models.BooleanField(default=False)
    def __str__(self):
        return self.especialidad.nombre


class registroObservaciones(models.Model):
    id=models.AutoField(primary_key=True)
    medico = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    paciente = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    observaciones=models.TextField(null=True, blank=True)
    estadoSalud=models.TextField(null=True, blank=True)
    especialidad=models.ForeignKey(EspecialidadMedico, on_delete=models.CASCADE, blank=True, null=True)
    fecha_creacion=models.DateTimeField(auto_now_add=True)
    estado= models.BooleanField(default=True)




@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        if instance.is_staff:
            Profile.objects.get_or_create(user=instance)
            print("Se acaba de crear un usuario y su perfil enlazado staff paciente")
        elif instance.is_superuser:
            ProfileHospital.objects.get_or_create(user=instance)
            print("Se acaba de crear un usuario y su perfil enlazado staff hospital")
        