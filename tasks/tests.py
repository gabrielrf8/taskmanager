from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Tarefa


class TarefaCRUDTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        self.tarefa = Tarefa.objects.create(
            usuario=self.user,
            titulo='Tarefa de teste',
            descricao='Descrição de teste',
            prioridade='media'
        )

    def test_create_tarefa(self):
        """CREATE — cria uma nova tarefa via POST."""
        response = self.client.post(reverse('criar_tarefa'), {
            'titulo': 'Nova tarefa',
            'descricao': 'Descrição',
            'prioridade': 'alta',
            'concluida': False,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tarefa.objects.filter(titulo='Nova tarefa').exists())

    def test_read_lista(self):
        """READ — lista de tarefas retorna 200."""
        response = self.client.get(reverse('lista_tarefas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tarefa de teste')

    def test_read_detalhe(self):
        """READ — detalhe de tarefa retorna 200."""
        response = self.client.get(reverse('detalhe_tarefa', args=[self.tarefa.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_tarefa(self):
        """UPDATE — edita uma tarefa existente."""
        response = self.client.post(reverse('editar_tarefa', args=[self.tarefa.pk]), {
            'titulo': 'Tarefa editada',
            'descricao': 'Nova descrição',
            'prioridade': 'alta',
            'concluida': True,
        })
        self.assertEqual(response.status_code, 302)
        self.tarefa.refresh_from_db()
        self.assertEqual(self.tarefa.titulo, 'Tarefa editada')
        self.assertTrue(self.tarefa.concluida)

    def test_delete_tarefa(self):
        """DELETE — deleta uma tarefa via POST."""
        response = self.client.post(reverse('deletar_tarefa', args=[self.tarefa.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tarefa.objects.filter(pk=self.tarefa.pk).exists())

    def test_redirect_sem_login(self):
        """Acesso sem login redireciona para /login/."""
        self.client.logout()
        response = self.client.get(reverse('lista_tarefas'))
        self.assertRedirects(response, '/login/?next=/', fetch_redirect_response=False)
