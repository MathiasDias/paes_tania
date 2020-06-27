from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import Categorias, Produtos

def index(request):
    try:
        status = request.session['status']
    except KeyError:
        status = 'none'
    try:
        status2 = request.session['status2']
    except KeyError:
        status2 = 'none'
    try:
        status3 = request.session['status3']
    except KeyError:
        status3 = 'none'
    try:
        status4 = request.session['status4']
    except KeyError:
        status4 = 'none'
    try:
        status5 = request.session['status5']
    except KeyError:
        status5 = 'none'
    try:
        status6 = request.session['status6']
    except KeyError:
        status6 = 'none'
    context = {
    "status": status,
    "status2": status2,
    "status3": status3,
    "status4": status4,
    "status5": status5,
    "status6": status6,
    "log": request.user.is_authenticated,
    "username": request.user
    }
    request.session['status'] = 'none'
    request.session['status2'] = 'none'
    request.session['status3'] = 'none'
    request.session['status4'] = 'none'
    request.session['status5'] = 'none'
    request.session['status6'] = 'none'
    return render(request, "loja/index.html", context)

def auth_logingin(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        request.session['status'] = 'flex'
        return HttpResponseRedirect(reverse("index"))

def auth_registering(request):
    username = request.POST["username"]
    password = request.POST["password"]
    firstn = request.POST["firstn"]
    lastn = request.POST["lastn"]
    to_email = request.POST["email"]
    if User.objects.filter(username=username).exists():
        request.session['status5'] = 'flex'
        return HttpResponseRedirect(reverse("index"))
    if User.objects.filter(email=to_email).exists():
        request.session['status5'] = 'flex'
        return HttpResponseRedirect(reverse("index"))
    try:
        user2 = User.objects.create_user(username=username, email=to_email, password=password, first_name=firstn, last_name=lastn)
        user2.is_active = False
        user2.save()
        current_site = get_current_site(request)
        mail_subject = 'Ative sua conta Paes.'
        message = render_to_string('acc_active_email.html', {
            'user': user2,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user2.pk)),
            'token':account_activation_token.make_token(user2),
        })
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        request.session['status2'] = 'flex'
        return HttpResponseRedirect(reverse("index"))
    except ValueError:
        request.session['status4'] = 'flex'
        return HttpResponseRedirect(reverse("index"))
    except KeyError:
        request.session['status4'] = 'flex'
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("index"))

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        request.session['status6'] = 'flex'
        return HttpResponseRedirect(reverse("index"))
    else:
        request.session['status4'] = 'flex'
        return HttpResponseRedirect(reverse("index"))

def auth_logout(request):
    if request.user.is_authenticated:
        logout(request)
        request.session['status3'] = 'flex'
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))

def my_profile(request):
    if request.user.is_authenticated:
        context = {
            "log": request.user.is_authenticated,
            "username": request.user
        }
        return render(request, "loja/perfil.html", context)
    else:
        return HttpResponseRedirect(reverse("index"))

def quemsomos(request):
    context = {
        "log": request.user.is_authenticated,
        "username": request.user
    }
    return render(request, "loja/quem_somos.html", context)

def loja_produto(request, produto_id):
    try:
        produto = Produtos.objects.get(pk=produto_id)
    except KeyError:
        return render(request, "loja/erro.html")
    except Produtos.DoesNotExist:
        return render(request, "loja/erro.html")
    context = {
        "produto": produto,
        "log": request.user.is_authenticated,
        "username": request.user
    }
    return render(request, "loja/produto.html", context)

def loja_principal(request, ordem="Nome"):
    try:
        produtos = Produtos.objects.order_by(ordem)
        categorias = Categorias.objects.all()
    except KeyError:
        return render(request, "loja/erro.html")
    context = {
        "produtos": produtos,
        "categorias": categorias,
        "log": request.user.is_authenticated,
        "username": request.user
    }
    return render(request, "loja/loja.html", context)

def loja_categoria(request, categoria):
    try:
        categoria_id = Categorias.objects.get(Nome=categoria).id
        produtos = Produtos.objects.filter(Categoriateste=categoria_id)
        categorias = Categorias.objects.all()
    except KeyError:
        return render(request, "loja/erro.html")
    except Produtos.DoesNotExist:
        return render(request, "loja/erro.html")
    except Categorias.DoesNotExist:
        return render(request, "loja/erro.html")
    context = {
        "produtos": produtos,
        "cat": categoria,
        "categorias": categorias,
        "log": request.user.is_authenticated,
        "username": request.user
    }
    return render(request, "loja/loja.html", context)

def add_carrinho(request, produto_id):
    try:
        cart = request.session["carrinho"]
    except KeyError:
        request.session["carrinho"] = []
    try:
        produto = Produtos.objects.get(pk=produto_id)
        cart = request.session["carrinho"]
        cart.append(produto_id)
        request.session["carrinho"] = cart
    except KeyError:
        return render(request, "loja/erro.html")
    except Produtos.DoesNotExist:
        return render(request, "loja/erro.html")
    return HttpResponseRedirect(reverse("carrinho"))

def view_cart(request):
    try:
        cart = request.session["carrinho"]
    except KeyError:
        request.session["carrinho"] = []
    try:
        cart_2 = request.session["carrinho"]
        items = Produtos.objects.filter(id__in=cart_2)
    except KeyError:
        return render(request, "loja/erro.html")
    context = {
        "produtos": items,
        "log": request.user.is_authenticated,
        "username": request.user
    }
    return render(request, "loja/carrinho.html", context)
