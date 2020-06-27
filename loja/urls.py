from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logingin", views.auth_logingin, name="logingin"),
    path("logout", views.auth_logout, name="logout1"),
    path("perfil", views.my_profile, name="perfil"),
    path("loja/add/<int:produto_id>", views.add_carrinho, name="add_carrinho"),
    path("loja/carrinho", views.view_cart, name="carrinho"),
    path("loja/", views.loja_principal, name="loja"),
    path("loja/<ordem>", views.loja_principal, name="loja_ordem"),
    path("loja/categoria/<categoria>", views.loja_categoria, name="categoria"),
    path("loja/produto/<int:produto_id>", views.loja_produto, name="produto"),
    path("quemsomos", views.quemsomos, name="quemsomos"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('contas/', include('django.contrib.auth.urls')),
    path('contas/mudar_senha/', auth_views.PasswordResetView.as_view(), name='forgot'),
    path('contas/senha_mudada/sucesso', auth_views.PasswordResetCompleteView.as_view(template_name='registro/password_reset_complete.html')),
    url(r'^contas/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordChangeView.as_view(template_name='registro/password_reset_confirm.html')),
    path('contas/mudar_senha/sucesso', auth_views.PasswordResetView.as_view(template_name='registro/password_reset_done.html')),
    path("registering", views.auth_registering, name="registering")
]
