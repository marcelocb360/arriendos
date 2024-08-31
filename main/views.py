from django.shortcuts import render, redirect
from main.services import crear_user, editar_user_sin_password, cambio_password, crear_inmueble, editar_inmueble, eliminar_inmueble, filtro_comuna_region, filtro_comuna_region
from django.contrib.auth.decorators import login_required
from main.models import Inmueble, Region, Comuna, SolicitudArriendo,UserProfile
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.views.generic import ListView

# Create your views here.

def index(request):
    # Recibe información vía get:
    propiedades = Inmueble.objects.all()
    datos = request.GET
    comuna_cod = datos.get('comuna_cod', '')
    region_cod = datos.get('region_cod', '')
    tipo_inmueble = datos.get('tipo_inmueble', '')

    propiedades = filtro_comuna_region(comuna_cod, region_cod, tipo_inmueble)

    comunas = Comuna.objects.all().order_by('nombre')
    regiones = Region.objects.all()
    tipos_inmuebles = Inmueble.inmuebles
    context = {
        'comunas': comunas,
        'regiones': regiones,
        'tipos_inmuebles': tipos_inmuebles,
        'propiedades': propiedades
    }
    return render(request, 'index.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        rol = request.POST['rol']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']
            
        crear = crear_user( username, first_name, last_name, email, password, password_repeat, direccion, rol, telefono)

        if crear: # Si crear es True
            return redirect('/accounts/login') 
        # Si llegó, crear fue False
        return render(request, 'registration/register.html', {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'direccion': direccion,
            'telefono': telefono,
            'rol': rol,
            })
    else: # en caso de metodo GET
        return render(request, 'registration/register.html')
    
@login_required
def profile(request):
    id_usuario = request.user.id
    propiedades = Inmueble.objects.filter(propietario_id=id_usuario)
    context = {
        'propiedades': propiedades
    }

    if request.method == 'POST':
        if request.POST['telefono'].strip() != '':
            username = request.user
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            direccion = request.POST['direccion']
            telefono = request.POST['telefono']
            rol = request.POST['rol']
            editar_user_sin_password(username, first_name, last_name, email, direccion, rol, telefono)
            messages.success(request, 'Ha actualizado sus datos con exito')
            return redirect('/accounts/profile')
        else:
            username = request.user
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            direccion = request.POST['direccion']
            rol = request.POST['rol']
                        
            editar_user_sin_password(username, first_name, last_name, email, rol, direccion)
            messages.success(request, 'Ha actualizado sus datos con exito sin telefono')
            return redirect('/accounts/profile')
    else:
        return render(request, 'profile.html', context)
    

def change_pass(request):
    password = request.POST['password']
    password_repeat = request.POST['password_repeat']
    cambio_password(request, password, password_repeat)
    return redirect('/accounts/profile')

@login_required
def add_propiedad(request):
    regiones = Region.objects.all()
    comunas = Comuna.objects.all().order_by('nombre')
    tipos_inmuebles = Inmueble.inmuebles # Tipos de inmuebles
    context = {
        'regiones': regiones,
        'comunas': comunas,
        'tipos_inmuebles': tipos_inmuebles
    }

    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        m2_construidos = int(request.POST['m2_construidos'])
        m2_totales = int(request.POST['m2_totales'])
        num_estacionamientos = int(request.POST['num_estacionamientos'])
        num_habitaciones = int(request.POST['num_habitaciones'])
        num_baños = int(request.POST['num_baños'])
        direccion = request.POST['direccion']
        precio_mensual_arriendo = int(request.POST['precio_mensual_arriendo'])
        tipo_de_inmueble = request.POST['tipo_de_inmueble']
        comuna_cod = request.POST['comuna_cod']
        rut_propietario = request.user

        crear = crear_inmueble(nombre, descripcion, m2_construidos, m2_totales, num_estacionamientos, num_habitaciones, num_baños, direccion, precio_mensual_arriendo, tipo_de_inmueble, comuna_cod, rut_propietario)
        if crear: # Si return render(request, 'add_propiedad.html', context)crear es True
            messages.success(request, 'Propiedad ingresada con éxito')
            return redirect('profile')
        # Si llega aquí, es porque crear fue False
        messages.warning(request, 'Hubo un problema al crear la propiedad, favor revisar')
        return render(request, 'add_propiedad.html', context)
    else: 
        return render(request, 'add_propiedad.html', context)
    
@login_required
def edit_propiedad(request, id):
    if request.method == 'GET':
        inmueble = Inmueble.objects.get(id=id)
        regiones = Region.objects.all()
        comunas = Comuna.objects.all().order_by('nombre')
        cod_region_actual = inmueble.comuna_id[0:2]
        context = {
            'inmueble': inmueble,
            'regiones': regiones,
            'comunas': comunas,
            'cod_region': cod_region_actual
        } 
        return render(request, 'edit_propiedad.html', context)
    else:
        inmueble_id = id
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        m2_construidos = int(request.POST['m2_construidos'])
        m2_totales = int(request.POST['m2_totales'])
        num_estacionamientos = int(request.POST['num_estacionamientos'])
        num_habitaciones = int(request.POST['num_habitaciones'])
        num_baños = int(request.POST['num_baños'])
        direccion = request.POST['direccion']
        precio_mensual_arriendo = int(request.POST['precio_mensual_arriendo'])
        tipo_de_inmueble = request.POST['tipo_de_inmueble']
        comuna = request.POST['comuna_cod']
        rut_propietario = request.user
        
        editar = editar_inmueble(inmueble_id, nombre, descripcion, m2_construidos, m2_totales, num_estacionamientos, num_habitaciones, num_baños, direccion, precio_mensual_arriendo, tipo_de_inmueble, comuna, rut_propietario)
        if editar:
            messages.success(request, 'Propiedad editada exitosamente')
            return redirect('profile')
        messages.error(request, 'Hubo un problema al editar la propiedad, favor revisar')
        return render(request, 'edit_propiedad.html', context)

@login_required
def delete_propiedad(request, id):
    eliminar = eliminar_inmueble(id)
    if eliminar:
        messages.warning(request, f'La propiedad {id} fue eliminada')
        return redirect('profile')
    else:
        messages.warning(request, 'Hubo un problema al eliminar la propiedad, favor revisar')
        return render(request, 'profile.html')

@login_required
def details_propiedad(request, id):
    id_buscado  = int(id)
    propiedad_encontrada = Inmueble.objects.get(id=id_buscado)
    context = {
        'propiedad': propiedad_encontrada
    }
    return render(request, 'detalles_propiedad.html', context)


@method_decorator(login_required, name='dispatch')
class CrearSolicitudArriendoView(View):
    def get(self, request, inmueble_id):
        inmueble = Inmueble.objects.get(id=inmueble_id)
        return render(request, 'crear_solicitud_arriendo.html', {'inmueble': inmueble})

    def post(self, request, inmueble_id):
        inmueble = Inmueble.objects.get(id=inmueble_id)
        arrendatario = UserProfile.objects.get(user=request.user)
        
        # Crear la solicitud de arriendo
        SolicitudArriendo.objects.create(
            arrendatario=arrendatario,
            inmueble=inmueble
        )

        messages.success(request, 'Solicitud de arriendo creada exitosamente.')
        return redirect('details_propiedad', id=inmueble.id)
    
class ListarSolicitudesArriendoView(ListView):
        model = SolicitudArriendo
        template_name = 'listar_solicitudes_arriendo.html'
        context_object_name = 'solicitudes'

        def get_queryset(self):
            # Filtrar las solicitudes por el usuario autenticado
            return SolicitudArriendo.objects.filter(arrendatario__user=self.request.user)

        def get_queryset(self):
            user_profile = UserProfile.objects.get(user=self.request.user)
            if user_profile.rol == 'arrendador':
                return SolicitudArriendo.objects.filter(inmueble__propietario=self.request.user)
            else:
                return SolicitudArriendo.objects.filter(arrendatario=user_profile)
            




@login_required
def gestionar_solicitudes_arriendo(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    if user_profile.rol == 'arrendador':
        solicitudes = SolicitudArriendo.objects.filter(inmueble__propietario=request.user)
        
        if request.method == 'POST':
            solicitud_id = request.POST.get('solicitud_id')
            accion = request.POST.get('accion')
            
            solicitud = SolicitudArriendo.objects.get(id=solicitud_id)

            if accion == 'aceptar':
                solicitud.estado_solicitud = 'aceptada'
                messages.success(request, 'La solicitud ha sido aceptada.')
            elif accion == 'rechazar':
                solicitud.estado_solicitud = 'rechazada'
                messages.success(request, 'La solicitud ha sido rechazada.')

            solicitud.save()
            return redirect('gestionar_solicitudes_arriendo')

        return render(request, 'gestionar_solicitudes_arriendo.html', {'solicitudes': solicitudes})
    
    else:
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('index')
