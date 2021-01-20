from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, ProfileHospital, registroObservaciones,EspecialidadMedico


class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. 254 carácteres como máximo y debe ser válido.")

    class Meta:
        model = User
        fields = ("username", "email","first_name", "is_staff", "is_superuser", "password1", "password2")
        help_texts = {
            'is_staff': 'Marcar si es Paciente',
            'is_superuser': 'Marcar si es Hospital',
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ya está registrado, prueba con otro.")
        return email

class UserCreationFormWithEmailMedico(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. 254 carácteres como máximo y debe ser válido.")

    class Meta:
        model = User
        fields = ("username", "email","first_name", "password1", "password2")
        

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ya está registrado, prueba con otro.")
        return email



        


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nombre', 'direccion', 'fechanac']

class ProfileHospitalForm(forms.ModelForm):
    class Meta:
        model = ProfileHospital
        fields = ['nombre', 'direccion']
       


class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Requerido. 254 carácteres como máximo d debe ser válido.")

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("El email ya está registrado, prueba con otro.")
        return email



class ObservacionesForm(forms.ModelForm):


    class Meta:
        model = registroObservaciones
        fields = ["medico", "paciente","observaciones", "estadoSalud", "especialidad"]
    

        
