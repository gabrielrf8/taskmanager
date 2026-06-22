from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tarefas, name='lista_tarefas'),
    path('login/', views.login_view, name='login'),
    path('nova/', views.criar_tarefa, name='criar_tarefa'),
    path('<int:pk>/', views.detalhe_tarefa, name='detalhe_tarefa'),
    path('<int:pk>/editar/', views.editar_tarefa, name='editar_tarefa'),
    path('<int:pk>/deletar/', views.deletar_tarefa, name='deletar_tarefa'),
]
