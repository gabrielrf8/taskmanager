from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Tarefa
from .forms import TarefaForm


def login_view(request):
    """Página de login com GitHub."""
    if request.user.is_authenticated:
        return redirect('lista_tarefas')
    error = request.GET.get('error')
    return render(request, 'tasks/login.html', {'error': error})


@login_required
def lista_tarefas(request):
    """READ — Lista todas as tarefas do usuário logado."""
    tarefas = Tarefa.objects.filter(usuario=request.user)
    total = tarefas.count()
    concluidas = tarefas.filter(concluida=True).count()
    pendentes = total - concluidas
    return render(request, 'tasks/lista.html', {
        'tarefas': tarefas,
        'total': total,
        'concluidas': concluidas,
        'pendentes': pendentes,
    })


@login_required
def criar_tarefa(request):
    """CREATE — Cria uma nova tarefa."""
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.usuario = request.user
            tarefa.save()
            messages.success(request, 'Tarefa criada com sucesso!')
            return redirect('lista_tarefas')
    else:
        form = TarefaForm()
    return render(request, 'tasks/form.html', {'form': form, 'titulo': 'Nova Tarefa'})


@login_required
def detalhe_tarefa(request, pk):
    """READ — Exibe detalhes de uma tarefa."""
    tarefa = get_object_or_404(Tarefa, pk=pk, usuario=request.user)
    return render(request, 'tasks/detalhe.html', {'tarefa': tarefa})


@login_required
def editar_tarefa(request, pk):
    """UPDATE — Edita uma tarefa existente."""
    tarefa = get_object_or_404(Tarefa, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarefa atualizada com sucesso!')
            return redirect('lista_tarefas')
    else:
        form = TarefaForm(instance=tarefa)
    return render(request, 'tasks/form.html', {'form': form, 'titulo': 'Editar Tarefa', 'tarefa': tarefa})


@login_required
def deletar_tarefa(request, pk):
    """DELETE — Deleta uma tarefa após confirmação."""
    tarefa = get_object_or_404(Tarefa, pk=pk, usuario=request.user)
    if request.method == 'POST':
        tarefa.delete()
        messages.success(request, 'Tarefa deletada com sucesso!')
        return redirect('lista_tarefas')
    return render(request, 'tasks/confirmar_delete.html', {'tarefa': tarefa})
