from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from .forms import UserForm, ProfileForm, GroupForm

def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('access_denied')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Create your views here.

def logIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=username, password=pwd)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Identifiants incorrects")
    return render(request, 'login.html')

def ask_logout(request):
    return render(request, 'mng_users/logout_confirm.html')

def logOut(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('ask_logout')

def access_denied(request):
    return render(request, 'mng_users/access_denied.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'mng_users/profile.html', {'form': form})

# Gestion des utilisateurs
@login_required
@staff_required
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'mng_users/user_list.html', {'users': users})

@login_required
@staff_required
def user_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Utilisateur créé avec succès.")
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'mng_users/user_form.html', {'form': form, 'title': "Ajouter un utilisateur"})

@login_required
@staff_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Utilisateur mis à jour.")
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'mng_users/user_form.html', {'form': form, 'title': "Modifier l'utilisateur"})

@login_required
@staff_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "Vous ne pouvez pas vous supprimer vous-même.")
    else:
        user.delete()
        messages.success(request, "Utilisateur supprimé.")
    return redirect('user_list')

@login_required
@staff_required
def user_toggle_status(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "Vous ne pouvez pas changer votre propre statut.")
    else:
        user.is_active = not user.is_active
        user.save()
        status = "activé" if user.is_active else "bloqué"
        messages.success(request, f"Utilisateur {status}.")
    return redirect('user_list')

# Gestion des groupes
@login_required
@staff_required
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'mng_users/group_list.html', {'groups': groups})

@login_required
@staff_required
def group_add(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Groupe créé avec succès.")
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'mng_users/group_form.html', {'form': form, 'title': "Ajouter un groupe"})

@login_required
@staff_required
def group_edit(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Groupe mis à jour.")
            return redirect('group_list')
    else:
        form = GroupForm(instance=group)
    return render(request, 'mng_users/group_form.html', {'form': form, 'title': "Modifier le groupe"})