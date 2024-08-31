from django.urls import path
from main.views import index, register,profile, change_pass, add_propiedad, edit_propiedad, delete_propiedad,details_propiedad, CrearSolicitudArriendoView , ListarSolicitudesArriendoView, gestionar_solicitudes_arriendo

urlpatterns = [

    path ('', index, name='index'),   
    path ('accounts/register', register, name='register',),
    path ('accounts/profile/', profile, name='profile',),
    path ('accounts/change-pass',change_pass, name='change_pass',),
    path ('propiedad/add-propiedad',add_propiedad, name='add_propiedad',),
    path('propiedad/edit-propiedad/<id>', edit_propiedad, name='edit_propiedad',),
    path('propiedad/delete-propiedad/<id>', delete_propiedad, name='delete_propiedad',),
    path('propiedad/detalles/<id>', details_propiedad, name='details_propiedad',),
    path('solicitar-arriendo/<int:inmueble_id>/', CrearSolicitudArriendoView.as_view(), name='crear_solicitud_arriendo'),
    path('mis-solicitudes/', ListarSolicitudesArriendoView.as_view(), name='listar_solicitudes_arriendo'),
    path('gestionar-solicitudes/', gestionar_solicitudes_arriendo, name='gestionar_solicitudes_arriendo'),


]
