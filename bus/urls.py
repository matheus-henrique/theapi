from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.post_list),
    url(r'^post/(?P<pk>[^/]+)/$', views.todos_veiculos),
    url(r'^reclamacoes/$',views.reclamacoes),
    url(r'^linhas/$',views.linhas),
    url(r'^linhas/(?P<pk>[0-9]+)/$', views.veiculo_especifico),
]