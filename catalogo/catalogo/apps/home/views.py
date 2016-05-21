from django.shortcuts import render_to_response
from django.template import RequestContext
from catalogo.apps.ventas.models import Producto
from catalogo.apps.ventas.models import Marca
from catalogo.apps.home.forms import contact_form
from django.core.mail import EmailMultiAlternatives

from catalogo.apps.home.forms import contact_form, Login_form, RegisterForm

from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage, InvalidPage


from django.contrib.auth.models import User

def index_view (request):
	return render_to_response('home/index.html', context_instance = RequestContext(request))

def contacto_view (request):
		info_enviado = False 
		email = ""
		country = ""
		sex  = ""
		age = ""
		if request.method == "POST":
			formulario = contact_form(request.POST)
			if formulario.is_valid():
				info_enviado = True
				email 	= formulario.cleaned_data['correo']
				country = formulario.cleaned_data['pais']
				sex  	= formulario.cleaned_data['sexo']
				age  	= formulario.cleaned_data['edad']
		else:
			formulario = contact_form()		
		ctx = {'form':formulario, 'email':email, 'country':country, 'sex':sex, 'age':age, 'info_enviado':info_enviado}	
		return render_to_response('home/contacto.html',ctx,context_instance = RequestContext(request))

#def productos_view (request):
	#lista_prod = Producto.objects.filter(status = True)	 #Select * from producto where status = true
#	lista_prod = Producto.objects.all()
	#lista_prod = Producto.objects.filter(id= 2)
	#lista_prod = Producto.objects.filter(id= 3)
	#lista_prod = Producto.objects.filter(status = False)
	#lista_prod = Producto.objects.order_by('precio')
	#lista_prod = Producto.objects.order_by('nombre')
	#lista_prod = Producto.objects.order_by('marca')
	#lista_prod = Producto.objects.all()[5:10]
	#lista_prod = Producto.objects.all()[:3]
	#lista_prod = Producto.objects.all()[:10:3]
	#lista_prod = Producto.objects.filter(marca_id= 1)
	#lista_prod = Producto.objects.filter(marca_id= 2)
	#lista_prod = Producto.objects.order_by('nombre' and 'precio')
	#lista_prod = Marca.objects.exclude(nombre__startswith = 'r')
	#lista_prod = Producto.objects.filter(marca__lt='2')
	#lista_prod = Producto.objects.filter(marca__exact='6')
	#lista_prod = Producto.objects.filter(id__contains='2')
	#lista_prod = Producto.objects.filter(marca__gte ='6')

	#ctx = {'productos':lista_prod}
	#return render_to_response('home/productos.html',ctx, context_instance = RequestContext(request))

def add_producto_view (request):
	return render_to_response('home/about.html',ctx, context_instance = RequestContext(request))	

def single_product_view(request, id_prod):
	prod = Producto.objects.get(id = id_prod)	
	ctx = {'producto':prod}
	return render_to_response('home/single_producto.html',ctx,context_instance = RequestContext(request))




def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			formulario = Login_form(request.POST)
			if formulario.is_valid():
				usu = formulario.cleaned_data['usuario']
				pas = formulario.cleaned_data['clave']
				usuario = authenticate(username = usu, password = pas)
				if usuario is not None and usuario.is_active:
					login(request, usuario)
					return HttpResponseRedirect('/')
				else:
					mensaje = "usuario y/o clave incorrecta"
		formulario = Login_form() 			
		ctx = {'form':formulario, 'mensaje':mensaje}
		return render_to_response('home/login.html', ctx, context_instance = RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')


def productos_view(request, pagina):
	lista_prod = Producto.objects.filter(status = True)
	paginator = Paginator(lista_prod, 3)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		productos = paginator.page(page)
	except (EmptyPage,InvalidPage):
		productos = paginator.page(paginator.num_pages)

	ctx = {'productos':productos}	
	return render_to_response ('home/productos.html', ctx, context_instance = RequestContext(request))


def register_view(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			u = User.objects.create_user(username=usuario,email=email,password=password_one)
			u.save()
			return render_to_response('home/thanks_register.html',context_instance=RequestContext(request))
		else:
			ctx = {'form':form}
			return render_to_response('home/register.html',ctx,context_instance=RequestContext(request))
	ctx = {'form':form}	
	return render_to_response('home/register.html',ctx,context_instance=RequestContext(request))	