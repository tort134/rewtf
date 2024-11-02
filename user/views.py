from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import *
from .models import Request, Profile
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль')
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form': form})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            district = form.cleaned_data.get('district')
            profile, created = Profile.objects.get_or_create(user=user)
            profile.district = district
            profile.save()

            messages.success(request, 'Вы успешно зарегистрированы! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'user/register.html', {'form': form})

def profile(request):
    status = request.GET.get('status')

    if status:
        user_requests = Request.objects.filter(user=request.user, status=status)
    else:
        user_requests = Request.objects.filter(user=request.user)

    return render(request, 'user/profile.html', {
        'user_requests': user_requests,
        'selected_status': status
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('profile')
    else:
        form = ChangePasswordForm()

    return render(request, 'user/change_password.html', {'form': form})

def update_district(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = DistrictForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регион успешно изменён!')
            return redirect('profile')  # Измените это на URL вашей страницы профиля
    else:
        form = DistrictForm(instance=profile)

    return render(request, 'user/update_district.html', {'form': form})

def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.user = request.user
            request_instance.save()
            return redirect('profile')
    else:
        form = RequestForm()

    return render(request, 'user/create_request.html', {
        'form': form
    })

def delete_request(request, request_id):
    request_instance = get_object_or_404(Request, id=request_id, user=request.user)

    if request_instance.status == 'new':
        request_instance.delete()
        messages.success(request, 'Заявка успешно удалена.')
    else:
        messages.error(request, 'Ошибка: заявку можно удалить только в статусе "Новая".')

    return redirect('profile')

def update_request_status(request, request_id):
    request_instance = get_object_or_404(Request, id=request_id, user=request.user)

    if request.method == 'POST':
        form = UpdateStatusForm(request.POST, request.FILES, instance=request_instance)  # Добавлено request.FILES
        if form.is_valid():
            request_instance.status = form.cleaned_data['status']
            request_instance.comment = form.cleaned_data.get('comment', request_instance.comment)
            if form.cleaned_data.get('photo'):
                request_instance.photo = form.cleaned_data['photo']
            request_instance.save()
            messages.success(request, 'Статус заявки успешно изменён.')
            return redirect('profile')
    else:
        form = UpdateStatusForm(instance=request_instance)

    return render(request, 'user/update_request_status.html', {
        'form': form,
        'request': request_instance
    })

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно добавлена.')
            return redirect('manage_categories')  # Название URL для управления категориями
    else:
        form = CategoryForm()

    return render(request, 'user/add_category.html', {'form': form})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Категория успешно удалена.')
        return redirect('manage_categories')

def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'user/manage_categories.html', {'categories': categories})
