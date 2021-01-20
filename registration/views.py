from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm, ProfileHospitalForm, UserCreationFormWithEmailMedico, ObservacionesForm
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django import forms
from django.views.generic.list import ListView
from .models import Profile, ProfileHospital, ServicioMedico, ServicioHospital, EspecialidadMedica, EspecialidadMedico,registroObservaciones
from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.
class HospitalRequiredMixin(object):
    """"Este mixin requerira que el usuario sea superuser"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect(reverse_lazy('home'))
        return super(HospitalRequiredMixin,self).dispatch(request,*args,**kwargs)

class MedicoRequiredMixin(object):
    """"Este mixin requerira que el usuario sea superuser"""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            return redirect(reverse_lazy('home'))
        return super(MedicoRequiredMixin,self).dispatch(request,*args,**kwargs)

class PacienteRequiredMixin(object):
    """"Este mixin requerira que el usuario sea superuser"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect(reverse_lazy('home'))
        return super(PacienteRequiredMixin,self).dispatch(request,*args,**kwargs)

class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'   

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        # Modificar en tiempo real
        form.fields['username'].widget = forms.TextInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Identificación'})
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Dirección email'})
        form.fields['first_name'].widget = forms.TextInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Teléfono'})
        form.fields['is_staff'].widget = forms. CheckboxInput(
            attrs={ 'class':' only-one'})
            
        form.fields['is_superuser'].widget = forms. CheckboxInput(
             attrs={ 'class':' only-one'})
           
        form.fields['password1'].widget = forms.PasswordInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Repite la contraseña'})
        return form

class SignUpMedicoView(HospitalRequiredMixin, CreateView):
    form_class = UserCreationFormWithEmailMedico
    template_name = 'registration/signupMedico.html'

    def get_success_url(self):
        return reverse_lazy('signupMedico') + '?register'   

    def get_form(self, form_class=None):
        form = super(SignUpMedicoView, self).get_form()
        # Modificar en tiempo real
        form.fields['username'].widget = forms.TextInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Identificación'})
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Dirección email'})
        form.fields['first_name'].widget = forms.TextInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Teléfono'})
        form.fields['password1'].widget = forms.PasswordInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Repite la contraseña'})
        return form


@method_decorator(login_required, name='dispatch')
class ProfileUpdate(PacienteRequiredMixin, UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_form.html'

    def get_object(self):
        # recuperar el objeto que se va editar
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    def get_form(self, form_class=None):
        form = super(ProfileUpdate, self).get_form()
        # Modificar en tiempo real
        form.fields['nombre'].widget = forms.TextInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Nombre'})
        
        form.fields['direccion'].widget = forms.TextInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Direccion'})
        
        form.fields['fechanac'].widget = forms.DateTimeInput(
            attrs={'class':'form-control mb-2', 'type':"date", 'value':'{{placement.date|date:"Y-m-d" }}'})
       
        return form

@method_decorator(login_required, name='dispatch')
class ProfileMedicoUpdate(MedicoRequiredMixin, UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profileMedico')
    template_name = 'registration/profileMedico_form.html'

    def get_object(self):
        # recuperar el objeto que se va editar
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    def get_form(self, form_class=None):
        form = super(ProfileMedicoUpdate, self).get_form()
        # Modificar en tiempo real
        form.fields['nombre'].widget = forms.TextInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Nombre'})
        
        form.fields['direccion'].widget = forms.TextInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Direccion'})
        
        form.fields['fechanac'].widget = forms.DateTimeInput(
            attrs={'class':'form-control mb-2', 'type':"date", 'value':'{{placement.date|date:"Y-m-d" }}'})
       
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
         #creo datos en la tabla intermedia en caso de no existir
        ObjetoServicioMedico = EspecialidadMedica.objects.filter(estado=True)
        for objservicio in ObjetoServicioMedico:
            obj, created = EspecialidadMedico.objects.get_or_create(
            user=self.request.user,
            especialidad=objservicio,
        )
        #tomo los datos a usar
        ObjetoEspecialidadMedico=EspecialidadMedico.objects.filter(user=self.request.user)
        context['datoEspecialidadMedico'] =ObjetoEspecialidadMedico
        return context

def cambiarEstadoEspecialidad(request):
    idencontrada=request.GET.get("id")
    html = "Error"
    if idencontrada:
        datos=EspecialidadMedico.objects.get(id=idencontrada)
        if datos.estado is True:
            EspecialidadMedico.objects.filter(id=idencontrada).update(estado=False)
            html = "Especialidad desactivada con exito"
            print("Especialidad desactivada con exito")
        else:
            EspecialidadMedico.objects.filter(id=idencontrada).update(estado=True)
            html = "Especialidad  activada con exito"
       
    return HttpResponse(html)
    
@method_decorator(login_required, name='dispatch')
class ProfileHospitalUpdate(HospitalRequiredMixin, UpdateView):
    form_class = ProfileHospitalForm
    success_url = reverse_lazy('profileHospital')
    template_name = 'registration/profileHospital_form.html'
    

    def get_object(self):
        # recuperar el objeto que se va editar
        profile, created = ProfileHospital.objects.get_or_create(user=self.request.user)
        return profile
    def get_form(self, form_class=None):
        form = super(ProfileHospitalUpdate, self).get_form()
        # Modificar en tiempo real
        form.fields['nombre'].widget = forms.TextInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Nombre'})
        
        form.fields['direccion'].widget = forms.TextInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Direccion'})

        return form

   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
         #creo datos en la tabla intermedia en caso de no existir
        ObjetoServicioMedico = ServicioMedico.objects.filter(estado=True)
        for objservicio in ObjetoServicioMedico:
            obj, created = ServicioHospital.objects.get_or_create(
            user=self.request.user,
            servicio=objservicio,
        )
       
        

        
        #tomo los datos a usar
        ObjetoServicioHospital=ServicioHospital.objects.filter(user=self.request.user)
        context['datoServicioMedico'] =ObjetoServicioHospital
        return context


def cambiarEstadoServicio(request):
    idencontrada=request.GET.get("id")
    html = "Error"
    if idencontrada:
        datos=ServicioHospital.objects.get(id=idencontrada)
        if datos.estado is True:
            ServicioHospital.objects.filter(id=idencontrada).update(estado=False)
            html = "Servicio desactivado con exito"
            print("Servicio desactivado con exito")
        else:
            ServicioHospital.objects.filter(id=idencontrada).update(estado=True)
            html = "Servicio activado con exito"
       
    return HttpResponse(html)

@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        # recuperar el objeto que se va editar
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        # Modificar en tiempo real
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Email'})
        return form



class SignUpObservaciones(CreateView):
    form_class = ObservacionesForm
    template_name = 'registration/signupObservaciones.html'

    def get_success_url(self):
        return reverse_lazy('signupObservaciones') + '?register'   

    def get_form(self, form_class=None):
        form = super(SignUpObservaciones, self).get_form()
        form.fields['observaciones'].widget = forms.Textarea(
            attrs={'class':'form-control mb-2', 'placeholder':'Escriba las observaciones médicas'})
        form.fields['estadoSalud'].widget = forms.TextInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Escriba el estado de salud'})
       
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        medico=Profile.objects.get(user=self.request.user)

            
        context['medico'] =medico.nombre
        return context

class observaciones_listPageView(HospitalRequiredMixin, ListView):
    model=registroObservaciones
    