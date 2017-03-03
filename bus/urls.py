from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.post_list),
    url(r'^post/(?P<pk>[^/]+)/$', views.todos_veiculos),
    url(r'^reclamacoes/$',views.reclamacoes),
    url(r'^linhas/$',views.linhas),
    url(r'^linhas/(?P<pk>[0-9]+)/$', views.veiculo_especifico),
    url(r'^linhasestaticas/$',views.linhas_estaticas),
    url(r'^todasaslinhasestaticas/$',views.todas_linhas_estaticas),
    url(r'^linha/zona/(?P<pk>[^/]+)/$', views.linhas_por_zona),
    url(r'^distanciaonibus/$',views.distancia_onibus_user)
]