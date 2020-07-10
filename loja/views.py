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
from .models import Categorias, Produtos, Pedidos, UserProfile, Descontos
from django.urls import resolve
import pycep_correios
from pycep_correios.excecoes import CEPInvalido, ExcecaoPyCEPCorreios

def status_code(request, status_code):
    request.session['status'] = 'none'
    request.session['status2'] = 'none'
    request.session['status3'] = 'none'
    request.session['status4'] = 'none'
    request.session['status5'] = 'none'
    request.session['status6'] = 'none'
    request.session['status7'] = 'none'
    request.session['status8'] = 'none'
    request.session['status9'] = 'none'
    request.session['status10'] = 'none'
    if status_code == 0:
        request.session['status'] = 'flex'
    elif status_code == 1:
        request.session['status2'] = 'flex'
    elif status_code == 2:
        request.session['status3'] = 'flex'
    elif status_code == 3:
        request.session['status4'] = 'flex'
    elif status_code == 4:
        request.session['status5'] = 'flex'
    elif status_code == 5:
        request.session['status6'] = 'flex'
    elif status_code == 6:
        request.session['status7'] = 'flex'
    elif status_code == 7:
        request.session['status8'] = 'flex'
    elif status_code == 8:
        request.session['status9'] = 'flex'
    elif status_code == 9:
        request.session['status10'] = 'flex'

def final_status(request):
    try:
        status = request.session['status']
    except KeyError:
        request.session['status'] = 'none'
    try:
        status2 = request.session['status2']
    except KeyError:
        request.session['status2'] = 'none'
    try:
        status3 = request.session['status3']
    except KeyError:
        request.session['status3'] = 'none'
    try:
        status4 = request.session['status4']
    except KeyError:
        request.session['status4'] = 'none'
    try:
        status5 = request.session['status5']
    except KeyError:
        request.session['status5'] = 'none'
    try:
        status6 = request.session['status6']
    except KeyError:
        request.session['status6'] = 'none'
    try:
        status7 = request.session['status7']
    except KeyError:
        request.session['status7'] = 'none'
    try:
        status8 = request.session['status8']
    except KeyError:
        request.session['status8'] = 'none'
    try:
        status9 = request.session['status9']
    except KeyError:
        request.session['status9'] = 'none'
    try:
        status10 = request.session['status10']
    except KeyError:
        request.session['status10'] = 'none'
    context = {
        "status": request.session['status'],
        "status2": request.session['status2'],
        "status3": request.session['status3'],
        "status4": request.session['status4'],
        "status5": request.session['status5'],
        "status6": request.session['status6'],
        "status7": request.session['status7'],
        "status8": request.session['status8'],
        "status9": request.session['status9'],
        "status10": request.session['status10'],
    }
    return context

def clear_status(request):
    request.session['status'] = 'none'
    request.session['status2'] = 'none'
    request.session['status3'] = 'none'
    request.session['status4'] = 'none'
    request.session['status5'] = 'none'
    request.session['status6'] = 'none'
    request.session['status7'] = 'none'
    request.session['status8'] = 'none'
    request.session['status9'] = 'none'
    request.session['status10'] = 'none'

def index(request):
    context = {
    "log": request.user.is_authenticated,
    "username": request.user
    }
    final_status2 = final_status(request)
    context.update(final_status2)
    clear_status(request)
    return render(request, "loja/index.html", context)

def auth_logingin(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        status_code(request, 0)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def auth_registering(request):
    username = request.POST["username"]
    password = request.POST["password"]
    firstn = request.POST["firstn"]
    lastn = request.POST["lastn"]
    cpf = request.POST["cpf"]
    celular = request.POST["celular"]
    to_email = request.POST["email"]
    if User.objects.filter(username=username).exists():
        status_code(request, 4)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    if User.objects.filter(email=to_email).exists():
        status_code(request, 4)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    try:
        user2 = User.objects.create_user(username=username, email=to_email, password=password, first_name=firstn, last_name=lastn)
        user2.is_active = False
        user2.save()
        user3 = UserProfile.objects.create(user=user2, cpf=cpf, celular=celular)
        user3.save()
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
        status_code(request, 1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except ValueError:
        status_code(request, 3)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except KeyError:
        status_code(request, 3)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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
        status_code(request, 5)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        status_code(request, 3)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def auth_logout(request):
    if request.user.is_authenticated:
        logout(request)
        status_code(request, 2)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(reverse("index"))

def my_profile(request):
    if request.user.is_authenticated:
        context = {
            "log": request.user.is_authenticated,
            "username": request.user
        }
        final_status2 = final_status(request)
        context.update(final_status2)
        clear_status(request)
        return render(request, "loja/perfil.html", context)
    else:
        status_code(request, 6)
        return HttpResponseRedirect(reverse("index"))

def my_orders(request):
    if request.user.is_authenticated:
        pedidos = Pedidos.objects.filter(Cpf_cliente=request.user.userprofile.cpf)
        context = {
            "log": request.user.is_authenticated,
            "pedidos": pedidos,
            "username": request.user
        }
        final_status2 = final_status(request)
        context.update(final_status2)
        clear_status(request)
        return render(request, "loja/pedidos.html", context)
    else:
        status_code(request, 6)
        return HttpResponseRedirect(reverse("index"))

def quemsomos(request):
    context = {
        "log": request.user.is_authenticated,
        "username": request.user
    }
    final_status2 = final_status(request)
    context.update(final_status2)
    clear_status(request)
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
    final_status2 = final_status(request)
    context.update(final_status2)
    clear_status(request)
    return render(request, "loja/produto.html", context)

def loja_principal(request, ordem="Nome", num_pagina=1):
    try:
        produtos = Produtos.objects.order_by(ordem)
        num = Produtos.objects.order_by(ordem).count()
        categorias = Categorias.objects.all()
    except KeyError:
        return render(request, "loja/erro.html")
    if num > 16:
        pags = int(num/16) + 1
    else:
        pags = 1
    paginas = []
    for n in range(1, pags + 1):
        paginas.append(n)
    produtos = produtos[(num_pagina - 1)*16:16*num_pagina]
    context = {
        "produtos": produtos,
        "categorias": categorias,
        "num": num,
        "ordem": ordem,
        "paginas": paginas,
        "num_pagina": num_pagina,
        "log": request.user.is_authenticated,
        "username": request.user
    }
    final_status2 = final_status(request)
    context.update(final_status2)
    clear_status(request)
    return render(request, "loja/loja.html", context)

def loja_categoria(request, categoria, num_pagina=1, ordem="Nome"):
    try:
        categoria_id = Categorias.objects.get(Nome=categoria).id
        produtos = Produtos.objects.filter(Categoriateste=categoria_id).order_by(ordem)
        num = Produtos.objects.filter(Categoriateste=categoria_id).count()
        categorias = Categorias.objects.all()
    except KeyError:
        return render(request, "loja/erro.html")
    except Produtos.DoesNotExist:
        return render(request, "loja/erro.html")
    except Categorias.DoesNotExist:
        return render(request, "loja/erro.html")
    if num > 16:
        pags = int(num/16) + 1
    else:
        pags = 1
    paginas = []
    for n in range(1, pags + 1):
        paginas.append(n)
    produtos = produtos[(num_pagina - 1)*16:16*num_pagina]
    context = {
        "cat": categoria,
        "produtos": produtos,
        "categorias": categorias,
        "num": num,
        "ordem": ordem,
        "paginas": paginas,
        "num_pagina": num_pagina,
        "log": request.user.is_authenticated,
        "username": request.user
    }
    final_status2 = final_status(request)
    context.update(final_status2)
    clear_status(request)
    return render(request, "loja/loja.html", context)

def add_carrinho(request, produto_id):
    try:
        cart = request.session["carrinho"]
    except KeyError:
        request.session["carrinho"] = []
        request.session["quantidades"] = []
        request.session["total"] = 0.00
    try:
        produto = Produtos.objects.get(pk=produto_id)
        cart = request.session["carrinho"]
        quantidade = request.session["quantidades"]
        total = request.session["total"]
        cart.append(produto_id)
        quantidade.append(1)
        total = total + float(produto.Preço)
        request.session["total"] = total
        request.session["quantidades"] = quantidade
        request.session["carrinho"] = cart
    except KeyError:
        return render(request, "loja/erro.html")
    except Produtos.DoesNotExist:
        return render(request, "loja/erro.html")
    return HttpResponseRedirect(reverse("carrinho"))

def view_cart(request):
    try:
        frete = request.session["frete"]
    except KeyError:
        request.session["frete"] = 0
    try:
        desconto = request.session["desconto"]
    except KeyError:
        request.session["desconto"] = 0
    try:
        cart_2 = request.session["carrinho"]
        total = request.session["total"]
        produtos = Produtos.objects.filter(id__in=cart_2)
        quantidades = request.session["quantidades"]
        frete = request.session["frete"]
        desconto = request.session["desconto"]
        valor_desconto = (total * (desconto * 0.01))
        valor_desconto = round(valor_desconto,2)
        total_final = total + frete - valor_desconto
        request.session["total_final"] = total_final
        itemsequantidade = zip(produtos, quantidades)
    except KeyError:
        request.session["carrinho"] = []
        request.session["total"] = 0.0
        request.session["quantidades"] = []
        return HttpResponseRedirect(reverse("carrinho"))
    context = {
        "produtos": itemsequantidade,
        "total_produtos": total,
        "desconto": desconto,
        "valor_desconto": valor_desconto,
        "frete": frete,
        "total_final": total_final,
        "log": request.user.is_authenticated,
        "username": request.user
    }
    final_status2 = final_status(request)
    context.update(final_status2)
    clear_status(request)
    return render(request, "loja/carrinho.html", context)

def rem_carrinho(request, produto_id, quantidade=1):
    try:
        cart = request.session["carrinho"]
        position = cart.index(produto_id)
        del cart[position]
        request.session["carrinho"] = cart
        produto = Produtos.objects.get(pk=produto_id)
        total = request.session["total"]
        total = total - (quantidade * float(produto.Preço))
        request.session["total"] = total
    except KeyError:
        return render(request, "loja/erro.html")
    return HttpResponseRedirect(reverse("carrinho"))

def rem_quantidade(request, produto_id):
    try:
        cart = request.session["carrinho"]
        position = cart.index(produto_id)
        quantidades = request.session["quantidades"]
        if int(quantidades[position]) > 1:
            quantidades[position] = quantidades[position] - 1
            request.session["quantidades"] = quantidades
            produto = Produtos.objects.get(pk=produto_id)
            total = request.session["total"]
            total = total - float(produto.Preço)
            request.session["total"] = total
        else:
            rem_carrinho(request, produto_id)
    except KeyError:
        return render(request, "loja/erro.html")
    return HttpResponseRedirect(reverse("carrinho"))

def add_quantidade(request, produto_id):
    try:
        cart = request.session["carrinho"]
        position = cart.index(produto_id)
        quantidades = request.session["quantidades"]
        if quantidades[position] < 9:
            quantidades[position] = quantidades[position] + 1
            request.session["quantidades"] = quantidades
            produto = Produtos.objects.get(pk=produto_id)
            total = request.session["total"]
            total = total + float(produto.Preço)
            request.session["total"] = total
    except KeyError:
        return render(request, "loja/erro.html")
    return HttpResponseRedirect(reverse("carrinho"))

def clear_cart(request):
    try:
        request.session["carrinho"] = []
        request.session["quantidades"] = []
        request.session["total"] = 0.00
    except KeyError:
        return render(request, "loja/erro.html")
    return HttpResponseRedirect(reverse("carrinho"))

def pesquisa(request):
    try:
        pesquisa = request.POST["pesquisa"]
    except KeyError:
        pesquisa = ""
    try:
        produtos = Produtos.objects.filter(Nome__icontains=pesquisa)
        num = Produtos.objects.filter(Nome__icontains=pesquisa).count()
        categorias = Categorias.objects.all()
    except KeyError:
        return render(request, "loja/erro.html")
    except TypeError:
        return render(request, "loja/erro.html")
    context = {
        "produtos": produtos,
        "pesquisa": pesquisa,
        "categorias": categorias,
        "num": num,
        "log": request.user.is_authenticated,
        "username": request.user
    }
    final_status2 = final_status(request)
    context.update(final_status2)
    clear_status(request)
    return render(request, "loja/loja.html", context)

def place_order(request):
    if request.user.is_authenticated:
        try:
            produtos_ids = request.session["carrinho"]
            total = request.session["total_final"]
            produtos_2 = Produtos.objects.filter(id__in=produtos_ids)
            quantidades = str(request.session["quantidades"])
            quantidades2 = quantidades.replace(" ", "")
            quantidades3 = quantidades2.replace(",", "")
            quantidades4 = quantidades3.replace("[", "")
            quantidades5 = quantidades4.replace("]", "")
            print(quantidades5)
            nome = request.user.first_name + " " + request.user.last_name
            cpf = request.user.userprofile.cpf
            endereço = request.user.userprofile.endereço
            pedido = Pedidos.objects.create(Nome_do_cliente=nome, Quantidades=quantidades5, Preço_total=total, Cpf_cliente=cpf, Endereço_cliente=endereço, Status='Pedido Feito')
            pedido.Items.add(*produtos_2)
        except KeyError:
            return render(request, "loja/erro.html")
        request.session["total"] = 0.0
        request.session["carrinho"] = []
        request.session["quantidades"] = []
        request.session["frete"] = []
        request.session["total_final"] = []
        status_code(request, 7)
        return HttpResponseRedirect(reverse("index"))
    else:
        status_code(request, 6)
        return HttpResponseRedirect(reverse("carrinho"))

def cupom_desconto(request):
    try:
        cupom = request.POST["cupom"]
        desconto = Descontos.objects.get(Cupom=cupom)
    except KeyError:
        return render(request, "loja/erro.html")
    except Descontos.DoesNotExist:
        status_code(request, 9)
        return HttpResponseRedirect(reverse("carrinho"))
    request.session["desconto"] = desconto.Porcentagem_desconto
    return HttpResponseRedirect(reverse("carrinho"))

def check_cep(request):
    if request.user.is_authenticated:
        try:
            cep = request.POST["cep"]
            cep2 = cep.replace("-","")
            endereço = pycep_correios.consultar_cep(cep2)
        except KeyError:
            return render(request, "loja/erro.html")
        except TypeError:
            return render(request, "loja/erro.html")
        except CEPInvalido:
            return render(request, "loja/erro.html")
        except ExcecaoPyCEPCorreios:
            return render(request, "loja/erro.html")
        if endereço['cidade'] != 'Campinas':
            status_code(request, 8)
            return HttpResponseRedirect(reverse("carrinho"))
        else:
            request.user.userprofile.cep = cep2
            request.user.userprofile.save()
            request.session["frete"] = 20
            return HttpResponseRedirect(reverse("carrinho"))
    else:
        status_code(request, 6)
        return HttpResponseRedirect(reverse("carrinho"))

def endereço(request):
    if request.session["frete"] != 0:
        try:
            cep = request.user.userprofile.cep
            endereço = pycep_correios.consultar_cep(cep)
        except KeyError:
            return render(request, "loja/erro.html")
        except TypeError:
            return render(request, "loja/erro.html")
        except CEPInvalido:
            return render(request, "loja/erro.html")
        except ExcecaoPyCEPCorreios:
            return render(request, "loja/erro.html")
        if endereço['cidade'] == 'Campinas':
            context = {
                "rua": endereço['end'],
                "cep": endereço['cep'],
                "bairro": endereço['bairro'],
                "cidade": endereço["cidade"],
                "uf": endereço["uf"],
                "log": request.user.is_authenticated,
                "username": request.user
            }
            final_status2 = final_status(request)
            context.update(final_status2)
            clear_status(request)
            return render(request, "loja/endereço.html", context)
        else:
            status_code(request, 8)
            return HttpResponseRedirect(reverse("carrinho"))
    else:
        status_code(request, 8)
        return HttpResponseRedirect(reverse("carrinho"))

def salvar_endereço(request):
    try:
        cep = request.POST["cep"]
        rua = request.POST["rua"]
        número = request.POST["número"]
        bairro = request.POST["bairro"]
        cidade = request.POST["cidade"]
        uf = request.POST["uf"]
        endereço = rua + ", " + número + " - " + bairro + " - " + cep + " - " + cidade + "/" + uf
    except KeyError:
        return render(request, "loja/erro.html")
    except TypeError:
        return render(request, "loja/erro.html")
    if cidade != "Campinas":
        status_code(request, 8)
        print(cidade)
        return HttpResponseRedirect(reverse("carrinho"))
    else:
        request.user.userprofile.endereço = endereço
        request.user.userprofile.save()
        return place_order(request)
