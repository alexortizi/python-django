from django.urls import path
from .views import SignUpView, ProfileUpdate, EmailUpdate,ProfileHospitalUpdate, SignUpMedicoView,cambiarEstadoServicio,ProfileMedicoUpdate, cambiarEstadoEspecialidad,SignUpObservaciones, observaciones_listPageView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('signupMedico/', SignUpMedicoView.as_view(), name="signupMedico"),
    path('signupObservaciones/', SignUpObservaciones.as_view(), name="signupObservaciones"),
    path('profile/', ProfileUpdate.as_view(), name="profile"),
    path('profileHospital/', ProfileHospitalUpdate.as_view(), name="profileHospital"),
    path('profileMedico/', ProfileMedicoUpdate.as_view(), name="profileMedico"),
    path('profile/email/', EmailUpdate.as_view(), name="profile_email"),
    path('profile/estado/', cambiarEstadoServicio, name="servicioestado"),
    path('profileMedico/estado/', cambiarEstadoEspecialidad, name="especialidadestado"),
    path('observaciones/', observaciones_listPageView.as_view(), name="observaciones"),
]